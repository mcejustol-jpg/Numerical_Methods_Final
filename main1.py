import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import math
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
from tkinter import simpledialog

# Set modern matplotlib style
style.use('seaborn-v0_8-darkgrid')

#######################
# COLORING & THEMES

class Theme:
    LIGHT = {
        'bg': '#f8f9fa',
        'fg': '#2c3e50',
        'accent': '#3498db',
        'accent_light': '#ecf0f1',
        'success': '#27ae60',
        'warning': '#f39c12',
        'error': '#e74c3c',
        'frame_bg': '#ffffff',
        'frame_border': '#bdc3c7',
        'hover': '#5dade2'
    }
    DARK = {
        'bg': '#0f1117',
        'fg': '#e6e6e6',
        'accent': '#8be9fd',
        'accent_light': '#282a36',
        'success': '#50fa7b',
        'warning': '#ffb86c',
        'error': '#ff5555',
        'frame_bg': '#161821',
        'frame_border': '#44475a',
        'hover': '#6272a4'
    }

######################
# SAFE FUNCTION PARSER

def normalize_expression(expr):
    expr = expr.strip()
    if '=' in expr:
        parts = expr.split('=')
        left = parts[0].strip()
        right = '='.join(parts[1:]).strip()
        expr = f"({left}) - ({right})"

    expr = expr.replace('^', '**')
    expr = expr.replace('X', 'x')

    # Implicit multiplication support for expressions like 3x, 2(x+1), or x(x+2)
    expr = re.sub(r'(?<=\d)(?=[x\(])', '*', expr)
    expr = re.sub(r'(?<=[x\)])(?=\()', '*', expr)

    return expr


def parse_function(expr):
    expr = normalize_expression(expr)
    def f(x):
        try:
            return eval(expr, {
                "x": x,
                "np": np,
                "math": math,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "log10": np.log10,
                "sqrt": np.sqrt,
                "pi": np.pi,
                "e": np.e,
                "abs": abs
            })
        except:
            return float('nan')
    return f


def refine_root(f, a, b, tol=1e-8, max_iter=60):
    fa = f(a)
    fb = f(b)
    if np.isnan(fa) or np.isnan(fb) or fa * fb > 0:
        return None

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        if np.isnan(fc):
            return None
        if abs(fc) < tol or abs(b - a) < tol:
            return c
        if fa * fc <= 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return (a + b) / 2


def parse_matrix(str_data):
    rows = [r for r in str_data.strip().split("\n") if r.strip() != ""]

    if len(rows) == 0:
        raise ValueError("Empty matrix")

    matrix = []
    for r in rows:
        values = r.strip().split()
        if len(values) == 0:
            continue
        matrix.append([float(v) for v in values])

    row_len = len(matrix[0])
    for row in matrix:
        if len(row) != row_len:
            raise ValueError("Inconsistent matrix size")

    return matrix


def matrix_to_string(A):
    lines = []
    for row in A:
        lines.append("".join(f"{val:10.4f}" for val in row))
    return "\n".join(lines)


def matrix_size(A):
    return f"{len(A)} x {len(A[0])}"


def add(A, B):
    r = len(A)
    c = len(A[0])
    return [[A[i][j] + B[i][j] for j in range(c)] for i in range(r)]


def multiply(A, B):
    r = len(A)
    c = len(B[0])
    C = [[0.0 for _ in range(c)] for _ in range(r)]
    for i in range(r):
        for j in range(c):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C


def matrix_power(A, exponent):
    """Raise square matrix A to a positive integer exponent by repeated multiplication."""
    if exponent < 1 or int(exponent) != exponent:
        raise ValueError("Exponent must be a positive integer")
    exponent = int(exponent)
    result = A
    for _ in range(1, exponent):
        result = multiply(result, A)
    return result


def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def minor(A, row, col):
    n = len(A)
    return [
        [A[i][j] for j in range(n) if j != col]
        for i in range(n) if i != row
    ]


def determinant(A):
    if len(A) == 1:
        return A[0][0]

    det = 0.0
    for i in range(len(A)):
        det += ((-1) ** i) * A[0][i] * determinant(minor(A, 0, i))
    return det


def adjoint(A):
    n = len(A)
    return [
        [((-1) ** (i + j)) * determinant(minor(A, i, j)) for i in range(n)]
        for j in range(n)
    ]


def inverse(A):
    det = determinant(A)
    if abs(det) < 1e-12:
        raise ValueError("Singular matrix")

    n = len(A)
    adj = adjoint(A)
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]


def solve_equation(A, B):
    invA = inverse(A)
    return multiply(invA, B)


###################################
# FORMULA (ROOT FINDING + MATRIX) #
###################################

FORMULAS = {
    "Incremental": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INCREMENTAL SEARCH METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Formula:
    x₁ = x₀ + Δx

Root Condition:
    f(x₀) · f(x₁) < 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",

    "Bisection": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BISECTION METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Formula:
    xr = (xL + xU) / 2

Decision Rule:
    If f(xL)·f(xr) < 0:
        xU = xr
    Else:
        xL = xr

Approximate Error:
    Ea = |(xr(new)-xr(old))/xr(new)| ×100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",

    "Regula Falsi": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REGULA FALSI METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Formula:
    xr = xU - [f(xU)(xL-xU)]/[f(xL)-f(xU)]

Approximate Error:
    Ea = |(xr(new)-xr(old))/xr(new)| ×100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",

    "Newton-Raphson": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEWTON-RAPHSON METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Formula:
    xᵢ₊₁ = xᵢ - f(xᵢ)/f'(xᵢ)

Approximate Error:
    Ea = |(xᵢ₊₁-xᵢ)/xᵢ₊₁| ×100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",

    "Secant": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECANT METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Formula:
    xᵢ₊₁ = xᵢ - [f(xᵢ)(xᵢ-xᵢ₋₁)]/[f(xᵢ)-f(xᵢ₋₁)]

Approximate Error:
    Ea = |(xᵢ₊₁-xᵢ)/xᵢ₊₁| ×100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
}

MATRIX_OPERATIONS = [
    "Addition",
    "Multiplication",
    "Transpose",
    "Determinant",
    "Inverse",
    "Adjoint",
    "Power",
    "Equation"
]

##################
# CUSTOM WIDGETS #
##################

class StyledFrame(ttk.Frame):
    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style='TFrame')

class StyledButton(ttk.Button):
    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)

############
# MAIN APP #
############
class NumericalMethodsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Methods")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        self.current_root_marker = None
        self.iteration_points = []
        
        self.current_theme = Theme.LIGHT
        self.root.configure(bg=self.current_theme['bg'])
        
        self.create_header()
        self.create_main_content()



##########
# SET-UP #
##########
    def setup_styles(self):
        self.ttk_style = ttk.Style()

        self.ttk_style.configure('Header.TLabel', font=('Segoe UI', 20, 'bold'))
        self.ttk_style.configure('Subheader.TLabel', font=('Segoe UI', 12, 'bold'))
        self.ttk_style.configure('TLabel', font=('Segoe UI', 10))
        self.ttk_style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        self.ttk_style.configure('TEntry', padding=5)
        self.ttk_style.configure('TCombobox', padding=5)
        self.ttk_style.configure('Treeview', font=('Courier New', 9), rowheight=22)
        self.ttk_style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))


######################
# APPLYING THE THEME #
######################
    def apply_theme(self):
        theme = self.current_theme

        self.ttk_style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        self.ttk_style.configure('Header.TLabel', background=theme['bg'], foreground=theme['accent'])
        self.ttk_style.configure('Subheader.TLabel', background=theme['bg'], foreground=theme['fg'])
        self.ttk_style.configure('TFrame', background=theme['bg'])
        self.ttk_style.configure('TNotebook', background=theme['bg'])
        self.ttk_style.configure('TNotebook.Tab', background=theme['frame_bg'], foreground=theme['fg'], padding=[20, 10])
        self.ttk_style.configure('TEntry', fieldbackground=theme['frame_bg'], background=theme['frame_bg'], foreground=theme['fg'])
        self.ttk_style.configure('TCombobox', fieldbackground=theme['frame_bg'], background=theme['frame_bg'], foreground=theme['fg'])
        self.ttk_style.configure('TButton', background=theme['frame_bg'], foreground=theme['fg'])
        self.ttk_style.configure('Treeview', background=theme['frame_bg'], fieldbackground=theme['frame_bg'], foreground=theme['fg'])
        self.ttk_style.configure('Treeview.Heading', background=theme['frame_bg'], foreground=theme['fg'])
        self.ttk_style.map('Treeview', background=[('selected', theme['accent'])], foreground=[('selected', theme['bg'])])

##########
# HEADER #
##########
    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=0, pady=0)
        
    # Title
        title_label = ttk.Label(
            header_frame,
            text="NUMERICAL METHODS",
            style='Header.TLabel'
        )
        title_label.pack(side="left", padx=20, pady=15)
        
    #----spacer----#
        ttk.Frame(header_frame).pack(side="left", fill="x", expand=True)
        ttk.Separator(self.root, orient='horizontal').pack(fill="x")

##################
# TABBED CONTENT #
##################
    def create_main_content(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
    #roottttt new tabs
        self.root_tab = ttk.Frame(self.notebook)
        self.matrix_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.root_tab, text="Root Finding Methods")
        self.notebook.add(self.matrix_tab, text="Matrix Operations")
        
        self.setup_root_tab()
        self.setup_matrix_tab()

####################
# ROOT FINDING TAB #
####################
    def setup_root_tab(self):
       
    #controlsssss panelssss
        control_frame = ttk.LabelFrame(self.root_tab, text="Configuration", padding=15)
        control_frame.pack(fill="x", padx=10, pady=10)
    
        row1 = ttk.Frame(control_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="Equation f(x):", style='Subheader.TLabel').pack(side="left", padx=5)
        self.eq_entry = ttk.Entry(row1, width=35)
        self.eq_entry.insert(0, "x^3 - x - 2")
        self.eq_entry.pack(side="left", padx=5)
        
        ttk.Label(row1, text="Method:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.method_combo = ttk.Combobox(
            row1,
            values=["Incremental", "Bisection", "Regula Falsi", "Newton-Raphson", "Secant"],
            state="readonly",
            width=18
        )
        self.method_combo.current(1)
        self.method_combo.pack(side="left", padx=5)


        row2 = ttk.Frame(control_frame)
        row2.pack(fill="x", pady=5)
        
        ttk.Label(row2, text="Lower Bound (XL):", style='Subheader.TLabel').pack(side="left", padx=5)
        self.xl_entry = ttk.Entry(row2, width=12)
        self.xl_entry.insert(0, "1")
        self.xl_entry.pack(side="left", padx=5)
        
        ttk.Label(row2, text="Upper Bound (XU):", style='Subheader.TLabel').pack(side="left", padx=5)
        self.xu_entry = ttk.Entry(row2, width=12)
        self.xu_entry.insert(0, "2")
        self.xu_entry.pack(side="left", padx=5)
        
        ttk.Label(row2, text="Tolerance:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.tol_entry = ttk.Entry(row2, width=12)
        self.tol_entry.insert(0, "0.0001")
        self.tol_entry.pack(side="left", padx=5)
        
        #3rd row in which there a button
        row3 = ttk.Frame(control_frame)
        row3.pack(fill="x", pady=10)
        
        solve_btn = ttk.Button(row3, text="Solve", command=self.solve_root, width=15)
        solve_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(row3, text="Clear", command=self.clear_root_table, width=15)
        clear_btn.pack(side="left", padx=5)
   
    #content areea
        content_frame = ttk.Frame(self.root_tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    # Left side table
        left_frame = ttk.LabelFrame(content_frame, text="Iteration Results", padding=5)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
    # Treeview with scrollbars
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("i", "XL", "XR", "XU", "f(XL)", "f(XR)", "Error %", "Product", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        column_widths = {"i": 40, "XL": 90, "XR": 90, "XU": 90, "f(XL)": 80, 
                        "f(XR)": 80, "Error %": 80, "Product": 80, "Status": 80}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 80), anchor="center")
       
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        right_frame = ttk.LabelFrame(content_frame, text="Function Visualization", padding=5)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        self.fig = Figure(figsize=(6, 6), dpi=100, facecolor='#f8f9fa')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("f(x) Graph", fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()


###########
# SOLVING #
###########

    def solve_root(self):
        try:
            self.iteration_points.clear()
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            expr = self.eq_entry.get().strip()
            if not expr:
                messagebox.showwarning("Input Error", "Please enter an equation")
                return
            
            f = parse_function(expr)
            
            xl = float(self.xl_entry.get())
            xu = float(self.xu_entry.get())
            tol = float(self.tol_entry.get())
            
            if xl >= xu:
                messagebox.showerror("Input Error", "XL must be less than XU")
                return
            
            method = self.method_combo.get()
            
            if method == "Bisection":
                self.bisection(f, xl, xu, tol)
            elif method == "Regula Falsi":
                self.regula_falsi(f, xl, xu, tol)
            elif method == "Incremental":
                self.incremental(f, xl, xu)
            elif method == "Newton-Raphson":
                self.newton(f, xl, tol)
            elif method == "Secant":
                self.secant(f, xl, xu, tol)
            
            self.plot_graph(f, xl, xu)
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numerical values")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    ############## INCREMENTAL

    def incremental(self, f, xl, xu):
        step = max((xu - xl) / 200.0, 0.01)
        i = 1
        x = xl
        while x < xu:
            fx = f(x)
            fx2 = f(x + step)
            remark = "Possible Root Detected ✓" if fx * fx2 < 0 else "Go to Next Interval →"
            self.tree.insert("", "end", values=(
                i, f"{x:.6f}", f"{x+step:.6f}", "-", 
                f"{fx:.6f}", f"{fx2:.6f}", "-", 
                f"{fx*fx2:.6f}", remark
            ))
            x += step
            i += 1
    

    ############# BISECTION

    def bisection(self, f, xl, xu, tol):
        xr_old = xl
        for i in range(1, 100):
            xr = (xl + xu) / 2
            fxl = f(xl)
            fxr = f(xr)
            product = fxl * fxr
            ea = abs((xr - xr_old) / xr) * 100 if i > 1 else float('inf')
            remark = "Root in LEFT interval → Move XU = XR" if product < 0 else "Root in RIGHT interval → Move XL = XR"
            
            self.tree.insert("", "end", values=(
                i, f"{xl:.6f}", f"{xr:.6f}", f"{xu:.6f}",
                f"{fxl:.6f}", f"{fxr:.6f}",
                f"{ea:.6f}" if ea != float('inf') else "---",
                f"{product:.6f}", remark
            ))

            self.iteration_points.append((xr, fxr))
            self.plot_graph(f, xl, xu, xr)
            self.root.update_idletasks()
            
            if product < 0:
                xu = xr
            else:
                xl = xr
            
            if abs(fxr) < 1e-10 or ea < tol:
                refined = refine_root(f, xl, xu, tol=1e-10)
                if refined is not None:
                    xr = refined
                messagebox.showinfo("Success", f"Root found at x = {xr:.10f}\nError: {ea:.6f}%")
                break
            xr_old = xr


    ################# FAKE POSITION

    def regula_falsi(self, f, xl, xu, tol):
        xr_old = xl
        for i in range(1, 100):
            fxl = f(xl)
            fxu = f(xu)
            
            if abs(fxl - fxu) < 1e-10:
                messagebox.showerror("Error", "Cannot divide by zero in Regula Falsi")
                break
            
            xr = xu - (fxu * (xl - xu)) / (fxl - fxu)
            fxr = f(xr)
            product = fxl * fxr
            ea = abs((xr - xr_old) / xr) * 100 if i > 1 else float('inf')
            remark = "Root in LEFT interval → Move XU = XR" if product < 0 else "Root in RIGHT interval → Move XL = XR" 
            
            self.tree.insert("", "end", values=(
                i, f"{xl:.6f}", f"{xr:.6f}", f"{xu:.6f}",
                f"{fxl:.6f}", f"{fxr:.6f}",
                f"{ea:.6f}" if ea != float('inf') else "---",
                f"{product:.6f}", remark
            ))
            
            self.iteration_points.append((xr, fxr))
            self.plot_graph(f, xl, xu, xr)
            self.root.update_idletasks()

            if product < 0:
                xu = xr
            else:
                xl = xr
            
            if abs(fxr) < 1e-10 or ea < tol:
                refined = refine_root(f, xl, xu, tol=1e-10)
                if refined is not None:
                    xr = refined
                messagebox.showinfo("Success", f"Root found at x = {xr:.10f}\nError: {ea:.6f}%")
                break
            xr_old = xr
    

    ############ RAPHSON

    def newton(self, f, x0, tol):
        h = 1e-6
        for i in range(1, 100):
            df = (f(x0 + h) - f(x0)) / h
            
            if abs(df) < 1e-10:
                messagebox.showerror("Error", "Derivative too small - cannot converge")
                break
            
            x1 = x0 - f(x0) / df

            self.iteration_points.append((x1, f(x1)))
            self.plot_graph(f, x0, x1, x1)
            self.root.update_idletasks()

            ea = abs((x1 - x0) / x1) * 100 if x1 != 0 else 0
            
            self.tree.insert("", "end", values=(
                i, f"{x0:.6f}", f"{x1:.6f}", "-",
                f"{f(x0):.6f}", f"{f(x1):.6f}",
                f"{ea:.6f}", "-", "Go to Next Iteration →"
            ))
            
            if abs(f(x1)) < 1e-10 or ea < tol:
                messagebox.showinfo("Success", f"Root found at x = {x1:.10f}\nError: {ea:.6f}%")
                break
            x0 = x1


    ########## SECANT
    
    def secant(self, f, x0, x1, tol):
        for i in range(1, 100):
            fx0 = f(x0)
            fx1 = f(x1)
            
            if abs(fx1 - fx0) < 1e-10:
                messagebox.showerror("Error", "Function values too close - cannot converge")
                break
            
            x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)
            ea = abs((x2 - x1) / x2) * 100 if x2 != 0 else 0
            
            self.tree.insert("", "end", values=(
                i, f"{x0:.6f}", f"{x1:.6f}", f"{x2:.6f}",
                f"{fx0:.6f}", f"{fx1:.6f}",
                f"{ea:.6f}", "-", "Go to Next Iteration →"
            ))
            
            if abs(f(x2)) < 1e-10 or ea < tol:
                messagebox.showinfo("Success", f"Root found at x = {x2:.10f}\nError: {ea:.6f}%")
                break
            x0, x1 = x1, x2

    def clear_root_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def plot_graph(self, f, xl, xu, xr=None):
        self.ax.clear()

    #zoom
        base_margin = max((xu - xl) * 0.8, 1)

        if xr is not None:
            zoom_factor = max(base_margin * 0.3, 0.2)
            x_center = xr
        else:
            zoom_factor = base_margin
            x_center = (xl + xu) / 2

        x_min = x_center - zoom_factor
        x_max = x_center + zoom_factor

        x = np.linspace(x_min, x_max, 800)

        y = np.array([f(val) if np.isfinite(f(val)) else np.nan for val in x])

        self.ax.plot(x, y, linewidth=2.5, label="f(x)")

        if xr is not None:
            self.ax.scatter([xr], [0], color="green", s=120, zorder=5, label="Current XR")
            self.ax.scatter([xr], [0], color="green", s=250, alpha=0.25, zorder=4)
            self.ax.axvline(xr, linestyle=":", color="green", alpha=0.7)

        #AXES & ROOT LINE
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.axvline(xl, linestyle="--", color="black", alpha=0.7, label="XL")
        self.ax.axvline(xu, linestyle="--", color="red", alpha=0.7, label="XU")

        roots = []
        for i in range(len(x) - 1):
            if np.isnan(y[i]) or np.isnan(y[i + 1]):
                continue
            if y[i] * y[i + 1] < 0:
                refined = refine_root(f, x[i], x[i + 1], tol=1e-10)
                if refined is not None:
                    close = False
                    for existing in roots:
                        if abs(existing - refined) < 1e-6:
                            close = True
                            break
                    if not close:
                        roots.append(refined)

        if roots:
            self.ax.scatter(roots, [0] * len(roots), color="green", s=80, label="Detected Roots")
            self.ax.scatter(roots, [0] * len(roots), color="black", s=30, zorder=5)

        valid_y = y[np.isfinite(y)]
        if len(valid_y) > 0:
            y_center = np.mean(valid_y)
            y_range = np.max(valid_y) - np.min(valid_y)
            if y_range > 50:
                self.ax.set_ylim(y_center - 25, y_center + 25)
            else:
                self.ax.set_ylim(np.min(valid_y) - 1, np.max(valid_y) + 1)

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_title("Root Visualization")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, alpha=0.4)
        self.ax.minorticks_on()
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def setup_matrix_tab(self):
        #control panel
        control_frame = ttk.LabelFrame(self.matrix_tab, text="Matrix Operations", padding=15)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        #operator for selction
        row1 = ttk.Frame(control_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="Operation:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.matrix_combo = ttk.Combobox(row1, values=MATRIX_OPERATIONS, state="readonly", width=25)
        self.matrix_combo.current(0)
        self.matrix_combo.pack(side="left", padx=5)
        
        # exponent selector for Power operation (created but hidden until needed)
        self.matrix_power_label = ttk.Label(row1, text="Power:", style='Subheader.TLabel')
        self.matrix_power_combo = ttk.Combobox(row1, values=["2", "3", "4"], state="readonly", width=5)
        self.matrix_power_combo.current(0)
        # don't pack yet; shown only when "Power" is selected
        
        compute_btn = ttk.Button(row1, text="✓ Compute", command=self.compute_matrix, width=15)
        compute_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(row1, text="🔄 Clear", command=self.clear_matrix, width=15)
        clear_btn.pack(side="left", padx=5)
        
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(fill="x", pady=5)

        # bind operation change to show/hide exponent selector
        self.matrix_combo.bind("<<ComboboxSelected>>", lambda e: self.on_matrix_op_change())
        # set initial visibility
        self.on_matrix_op_change()

        ttk.Label(size_frame, text="Target:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.matrix_target_combo = ttk.Combobox(size_frame, values=["A", "B"], state="readonly", width=5)
        self.matrix_target_combo.current(0)
        self.matrix_target_combo.pack(side="left", padx=5)

        ttk.Label(size_frame, text="Rows:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.matrix_rows_entry = ttk.Entry(size_frame, width=4)
        self.matrix_rows_entry.insert(0, "2")
        self.matrix_rows_entry.pack(side="left", padx=2)

        ttk.Label(size_frame, text="Cols:", style='Subheader.TLabel').pack(side="left", padx=5)
        self.matrix_cols_entry = ttk.Entry(size_frame, width=4)
        self.matrix_cols_entry.insert(0, "2")
        self.matrix_cols_entry.pack(side="left", padx=2)

        resize_btn = ttk.Button(size_frame, text="Set Size", command=self.resize_matrix, width=12)
        resize_btn.pack(side="left", padx=10)

    #matrix input
        input_frame = ttk.LabelFrame(self.matrix_tab, text="Matrix Input", padding=10)
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        

    #left side
        left_input = ttk.Frame(input_frame)
        left_input.pack(side="left", fill="both", expand=True, padx=5)
        
        ttk.Label(left_input, text="Matrix A :", 
                 style='Subheader.TLabel').pack(anchor="w", pady=5)
        self.matrix_a = tk.Text(left_input, height=10, width=40, wrap=tk.WORD,
                               font=('Courier New', 10))
        self.matrix_a.pack(fill="both", expand=True)
        self.matrix_a.insert("1.0", "1 2\n3 4")
        self.matrix_a.bind("<KeyRelease>", self.update_matrix_size_labels)
        self.matrix_a_size_label = ttk.Label(left_input, text="Matrix A Size: 2 x 2", style='Subheader.TLabel')
        self.matrix_a_size_label.pack(anchor="w", pady=5)
        

    #rightside
        right_input = ttk.Frame(input_frame)
        right_input.pack(side="right", fill="both", expand=True, padx=5)
        
        ttk.Label(right_input, text="Matrix B (if needed):", 
                 style='Subheader.TLabel').pack(anchor="w", pady=5)
        self.matrix_b = tk.Text(right_input, height=10, width=40, wrap=tk.WORD,
                               font=('Courier New', 10))
        self.matrix_b.pack(fill="both", expand=True)
        self.matrix_b.insert("1.0", "5 6\n7 8")
        self.matrix_b.bind("<KeyRelease>", self.update_matrix_size_labels)
        self.matrix_b_size_label = ttk.Label(right_input, text="Matrix B Size: 2 x 2", style='Subheader.TLabel')
        self.matrix_b_size_label.pack(anchor="w", pady=5)
        

    #result
        result_frame = ttk.LabelFrame(self.matrix_tab, text="Result", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.matrix_result = tk.Text(result_frame, height=12, width=100,
                                    font=('Courier New', 10), wrap=tk.WORD)
        
        
    #scrollbar sa result
        scrollbar = ttk.Scrollbar(result_frame, command=self.matrix_result.yview)
        scrollbar.pack(side="right", fill="y")
        self.matrix_result.pack(side="left", fill="both", expand=True)
        self.matrix_result.config(yscrollcommand=scrollbar.set)
        self.update_matrix_size_labels()

    ################### MATRIX SIZE HELPERS

    def matrix_size_from_text(self, text):
        if not text.strip():
            return "Empty"
        try:
            return matrix_size(parse_matrix(text))
        except Exception:
            return "Invalid"

    def update_matrix_size_labels(self, event=None):
        self.matrix_a_size_label.config(
            text=f"Matrix A Size: {self.matrix_size_from_text(self.matrix_a.get('1.0', 'end'))}"
        )
        self.matrix_b_size_label.config(
            text=f"Matrix B Size: {self.matrix_size_from_text(self.matrix_b.get('1.0', 'end'))}"
        )

    def on_matrix_op_change(self):
        """Show exponent selector when Power is selected; otherwise hide it.
        Also force target to A and disable target selection when powering."""
        op = self.matrix_combo.get()
        if op == "Power":
            try:
                self.matrix_power_label.pack(side="left", padx=6)
                self.matrix_power_combo.pack(side="left", padx=2)
            except Exception:
                pass
            if hasattr(self, 'matrix_target_combo'):
                try:
                    self.matrix_target_combo.set("A")
                    self.matrix_target_combo.config(state='disabled')
                except Exception:
                    pass
        else:
            try:
                self.matrix_power_label.pack_forget()
                self.matrix_power_combo.pack_forget()
            except Exception:
                pass
            if hasattr(self, 'matrix_target_combo'):
                try:
                    self.matrix_target_combo.config(state='readonly')
                except Exception:
                    pass

    def fill_matrix_widget(self, widget, rows, cols):
        text = widget.get("1.0", "end").strip()
        try:
            old_mat = parse_matrix(text)
        except Exception:
            old_mat = [[0.0 for _ in range(cols)] for _ in range(rows)]

        new_mat = [[0.0 for _ in range(cols)] for _ in range(rows)]
        for i in range(min(rows, len(old_mat))):
            for j in range(min(cols, len(old_mat[0]))):
                new_mat[i][j] = old_mat[i][j]

        widget.delete("1.0", "end")
        widget.insert("1.0", matrix_to_string(new_mat))

    def resize_matrix(self):
        try:
            rows = int(self.matrix_rows_entry.get())
            cols = int(self.matrix_cols_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Rows and columns must be positive integers")
            return

        target = self.matrix_target_combo.get()
        if target == "A":
            self.fill_matrix_widget(self.matrix_a, rows, cols)
        else:
            self.fill_matrix_widget(self.matrix_b, rows, cols)

        self.update_matrix_size_labels()

    ################### COMPUTING MATRIX

    def compute_matrix(self):

        try:
            A_text = self.matrix_a.get("1.0", "end").strip()
            B_text = self.matrix_b.get("1.0", "end").strip()
            op = self.matrix_combo.get()

            if not A_text:
                messagebox.showwarning("Input Error", "Enter Matrix A")
                return

            A = parse_matrix(A_text)

            self.matrix_result.delete("1.0", "end")

            result = None

            if op == "Addition":
                if not B_text:
                    messagebox.showwarning("Input Error", "Enter Matrix B for addition")
                    return
                B = parse_matrix(B_text)

                if len(A) != len(B) or len(A[0]) != len(B[0]):
                    raise ValueError("Matrices must have same dimensions")

                result = add(A, B)

            elif op == "Multiplication":
                if not B_text:
                    messagebox.showwarning("Input Error", "Enter Matrix B for multiplication")
                    return
                B = parse_matrix(B_text)

                if len(A[0]) != len(B):
                    raise ValueError("Invalid dimensions for multiplication")

                result = multiply(A, B)

            elif op == "Transpose":
                result = transpose(A)

            elif op == "Determinant":
                if len(A) != len(A[0]):
                    raise ValueError("Square matrix required")
                det = determinant(A)
                self.matrix_result.insert("end", f"Determinant = {det:.4f}")
                messagebox.showinfo("Success", "Operation completed!")
                return

            elif op == "Inverse":
                if len(A) != len(A[0]):
                    raise ValueError("Square matrix required")
                result = inverse(A)

            elif op == "Adjoint":
                if len(A) != len(A[0]):
                    raise ValueError("Square matrix required")
                result = adjoint(A)

            elif op == "Power":
                if len(A) != len(A[0]):
                    raise ValueError("Square matrix required")
                # get selected exponent (default to 2)
                pow_widget = getattr(self, 'matrix_power_combo', None)
                if pow_widget is None:
                    exponent = 2
                else:
                    try:
                        exponent = int(pow_widget.get() or "2")
                    except Exception:
                        exponent = 2

                result = matrix_power(A, exponent)

            elif op == "Equation":
                if not B_text:
                    messagebox.showwarning("Input Error", "Enter Matrix B for equation solver")
                    return
                B = parse_matrix(B_text)

                if len(A) != len(A[0]) or len(A[0]) != len(B):
                    raise ValueError("A must be square and B must have compatible rows")

                result = solve_equation(A, B)

            # DISPLAY
            if isinstance(result, str):
                self.matrix_result.insert("end", result)
            else:
                self.matrix_result.insert("end", matrix_to_string(result))

            messagebox.showinfo("Success", "Operation completed!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    ################### CLEARING MATRIX

    def clear_matrix(self):
        self.matrix_a.delete("1.0", "end")
        self.matrix_b.delete("1.0", "end")
        self.matrix_result.delete("1.0", "end")
        self.matrix_a.insert("1.0", "1 2\n3 4")
        self.matrix_b.insert("1.0", "5 6\n7 8")
        self.update_matrix_size_labels()


################### RUN APPLICATION
if __name__ == "__main__":
    root = tk.Tk()
    app = NumericalMethodsApp(root)
    root.mainloop()
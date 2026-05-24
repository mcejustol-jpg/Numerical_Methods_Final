NUMERICAL METHODS APPLICATION - COMPREHENSIVE VIDEO SCRIPT (PYTHON ONLY)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

PYTHON - COMPLETE BREAKDOWN
═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 1: INTRODUCTION AND OVERVIEW (0:00 - 1:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Welcome to the Numerical Methods application. This Python program demonstrates
five different algorithms for finding roots of equations, and eight matrix 
operations. Built with Tkinter for the interface, NumPy for calculations, and 
Matplotlib for visualization.

The application is divided into two main tabs: 'Root Finding Methods' and 
'Matrix Operations'. 

But before we dive into the code and how everything works, let me explain what 
this application actually solves. Root finding is one of the most fundamental 
problems in numerical analysis. In the real world, engineers might need to find 
where a bridge will fail under stress. Economists might need to find the market 
price where supply equals demand. Scientists need to find exact temperatures where 
chemical reactions occur. Programmers need to find where functions cross zero in 
graphics calculations.

This application doesn't just show you the answer—it shows you step-by-step HOW 
the computer finds the answer. Each iteration is displayed in a table, and a live 
graph updates to show the algorithm converging to the solution.

Let's explore what each section does."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 2: IMPORTS AND DEPENDENCIES (1:00 - 1:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"At the very top of the code, we import everything we need:

tkinter - This is Python's standard library for creating graphical user interfaces. 
We import the main tk module, plus ttk for modern styled widgets, messagebox for 
pop-up dialogs, and filedialog for file operations.

numpy - This is the numerical computing library. We use it for mathematical 
functions like sine, cosine, exp, log, and sqrt. NumPy also provides the pi and e 
constants.

math - Python's built-in math module, imported just in case.

re - The regular expressions module, used for pattern matching when we process 
user equations.

matplotlib - The plotting library. We use FigureCanvasTkAgg to embed matplotlib 
plots inside Tkinter windows, Figure to create the plot, and style to apply 
a modern dark grid theme.

simpledialog - For creating custom input dialogs.

These imports give us everything we need to build a fully-featured numerical 
methods application with a professional interface and publication-quality graphs."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 3: THE THEME SYSTEM (1:45 - 2:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"At the beginning of the code, we define a Theme class with two color schemes: 
LIGHT and DARK.

Each theme is a dictionary containing colors for:

'bg' - the background color of the entire window
'fg' - the foreground or text color
'accent' - the primary accent color for highlights
'accent_light' - a lighter version for secondary highlights
'success' - bright green for success messages
'warning' - orange for warnings
'error' - red for error messages
'frame_bg' - the background for frames and panels
'frame_border' - the color of borders
'hover' - the color when you hover over buttons

The LIGHT theme uses soft grays and blues, while the DARK theme uses deep blacks 
and purples. This theme system allows users to switch between themes without 
rewriting any code—we just swap the dictionary and reapply all colors.

Having this structure makes the application professional and accessible. Users 
can choose the theme that works best for their eyes, whether they're working in 
bright daylight or late at night."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 4: THE HEART OF THE SYSTEM - FUNCTION PARSER (2:45 - 4:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The normalize_expression function is critical. It converts user-friendly math 
notation into Python code that actually runs.

Here's what it does step by step:

STEP 1: Clean up whitespace
It removes spaces at the beginning and end using strip().

STEP 2: Handle equations
If someone types an equation like 'x + 2 = 5', the function recognizes the equals 
sign and converts it to: '(x + 2) - (5)'

Why? Because we want to solve for where this expression equals zero. By rearranging 
it this way, we can now find the root at x = 3.

STEP 3: Convert mathematical symbols
The caret symbol '^' becomes '**' because that's Python's exponentiation operator.
The capital 'X' becomes lowercase 'x' for consistency.

STEP 4: Add implicit multiplication
This is clever. When you write '3x', humans know this means 3 times x. But Python 
needs an explicit '*' operator. Using regular expressions, the code finds:
- A digit followed by 'x' or '(' and inserts a multiplication sign: 3x → 3*x
- A closing parenthesis followed by an opening parenthesis: (x)(2) → (x)*(2)

So a user can type: '2(x+1) + 3x - x^2' and it becomes: 
'2*(x+1) + 3*x - x**2'

Now the parse_function function takes this normalized expression and creates 
an actual Python function using eval(). It provides a safe namespace containing 
only approved math functions: sin, cos, tan, exp, log, sqrt, and the constants 
pi and e.

If something goes wrong during evaluation, it returns NaN instead of crashing. 
This makes the application robust and user-friendly.

The refine_root helper function then uses bisection internally to polish the 
final answer to extremely high precision—10 decimal places—for maximum accuracy."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 5: ROOT FINDING TAB - INTERFACE DESIGN (4:30 - 5:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"When you open the Root Finding tab, you see a carefully designed interface.

At the very top is a CONFIGURATION PANEL with three rows of controls:

ROW 1:
- A label 'Equation f(x):'
- A text entry field where you type your equation
- Default equation is 'x^3 - x - 2'
- A label 'Method:'
- A dropdown list with five options: Incremental, Bisection, Regula Falsi, 
  Newton-Raphson, and Secant
- Bisection is selected by default because it's the most reliable

ROW 2:
- A label 'Lower Bound (XL):'
- Input field with default value '1'
- A label 'Upper Bound (XU):'
- Input field with default value '2'
- A label 'Tolerance:'
- Input field with default value '0.0001'

These three values define how the algorithm will search for the root.

ROW 3:
- A green 'Solve' button that runs the calculation
- A blue 'Clear' button that resets everything

Below the controls is the main content area, split into two sections:

LEFT SIDE - ITERATION RESULTS TABLE:
This is a Treeview widget showing all the iterations. The columns are:
i          - iteration number (1, 2, 3, ...)
XL         - the lower boundary
XR         - the current root estimate
XU         - the upper boundary
f(XL)      - function value at lower boundary
f(XR)      - function value at root estimate
Error %    - approximate error percentage
Product    - the product f(XL) × f(XR), used to determine which side has the root
Status     - a text description of what's happening

Each row represents one iteration of the algorithm. You can scroll through to see 
how the algorithm progressed.

RIGHT SIDE - LIVE GRAPH VISUALIZATION:
This shows a matplotlib plot with several elements:
- The function curve in blue
- A horizontal line at y=0 (the x-axis)
- A vertical dashed black line at x=XL
- A vertical dashed red line at x=XU
- A bright green dot showing the current root estimate
- Other green dots showing all detected roots in the visible range
- A grid for easy reading

The graph uses smart zooming: if we have a current root estimate, it zooms in 
around that point. Otherwise, it shows the full interval with some margin."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 6: THE SOLVE ROOT FUNCTION (5:45 - 7:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"When you click the Solve button, the solve_root function is called. Here's what 
it does:

STEP 1: Clear previous results
Delete all rows from the iteration table so we start fresh.
Clear the list of iteration points used for graphing.

STEP 2: Get user input
Read the equation string from the text entry field.
Read the selected method from the dropdown.
Read XL, XU, and tolerance from their input fields.

STEP 3: Validate input
Check that the equation is not empty. If it is, show a warning dialog.
Check that XL is less than XU. If not, show an error.
Try to convert the text fields to floating-point numbers. If that fails, 
show an error about invalid input.

STEP 4: Parse the equation
Call parse_function to convert the text equation into an actual Python function.

STEP 5: Call the appropriate algorithm
Use an if-elif statement to check which method was selected, then call the 
corresponding function:
- If 'Bisection' is selected, call self.bisection(f, xl, xu, tol)
- If 'Regula Falsi' is selected, call self.regula_falsi(f, xl, xu, tol)
- And so on for each method

STEP 6: Draw the final graph
After the method completes, call plot_graph to show the final visualization.

STEP 7: Error handling
Wrap everything in try-except blocks. If a ValueError occurs (bad numbers), 
show a specific error message. If any other exception occurs, show a generic 
error message with details."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 7: INCREMENTAL SEARCH METHOD (7:00 - 8:15)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The incremental function is the simplest root-finding method.

The idea is straightforward: we walk through the interval from XL to XU, checking 
if the function changes sign.

Here's the algorithm:

STEP 1: Calculate step size
divide the interval (XU - XL) by 200, giving us 200 small steps. If this produces 
a step smaller than 0.01, use 0.01 instead. This ensures we don't take steps 
that are too tiny.

STEP 2: Walk through the interval
Start at x = XL
While x < XU:
  - Calculate f(x)
  - Calculate f(x + step)
  - If f(x) × f(x+step) is negative (less than 0), the function changed sign, 
    so there's a root between these two points. Mark it as 'Possible Root Detected ✓'
  - Otherwise, mark it as 'Go to Next Interval →'
  - Insert all this data into the results table
  - Move to the next step: x = x + step

This method is very simple—it doesn't use any calculus or fancy math. It just 
looks for sign changes. 

Advantages:
- Always finds all roots in the interval
- Never diverges

Disadvantages:
- Slow compared to other methods
- Doesn't tell you how close you are to the root
- Doesn't narrow down the interval automatically

This method is useful for getting a rough idea of where all the roots are. Then 
you can use a faster method on the intervals you find."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 8: BISECTION METHOD (8:15 - 10:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The bisection method is one of the most reliable root-finding algorithms.

Think of it like a game: I'm thinking of a number between 1 and 100. You get to 
guess, and I'll tell you 'too high' or 'too low'. A smart strategy is to always 
guess the middle number. That way, you eliminate half the possible numbers with 
each guess.

Bisection works the same way:

STEP 1: Check that a root exists
Calculate f(XL) and f(XU).
If f(XL) × f(XU) is positive (same sign), there's probably no root in this 
interval. Return an error.

STEP 2: Enter the main loop (up to 100 iterations)
Calculate the midpoint: xr = (xl + xu) / 2

STEP 3: Evaluate the function at the midpoint
Calculate f(xr)

STEP 4: Determine which half contains the root
Calculate the product: product = f(xl) × f(xr)
If product < 0: the root is in the LEFT half [xl, xr]
  So set xu = xr (the upper boundary moves to the midpoint)
Else: the root is in the RIGHT half [xr, xu]
  So set xl = xr (the lower boundary moves to the midpoint)

STEP 5: Calculate the approximate error
For iterations after the first:
Ea = |(xr_new - xr_old) / xr_new| × 100%

This tells us how much our estimate changed from the previous iteration. If it's 
small, we're converging.

STEP 6: Store results
Insert the iteration number, xl, xr, xu, f(xl), f(xr), error, product, and 
a status message into the results table.

Add the point (xr, f(xr)) to the iteration points list for visualization.

Update the graph in real-time using plot_graph.

Force the GUI to update immediately using self.root.update_idletasks().

STEP 7: Check stopping criteria
If |f(xr)| < 1e-10, we're extremely close to the root. Stop.
If error < tolerance, we're within the user's accuracy requirement. Stop.

If we're stopping, refine the root one more time for maximum precision, then 
show a success dialog.

Otherwise, set xr_old = xr and repeat from STEP 2.

Why Bisection is Great:
- Guaranteed to converge if a root exists
- Predictable: takes about log₂(interval/tolerance) iterations
- Doesn't need the derivative
- Very stable

Why Bisection is Slow:
- Takes many iterations compared to methods like Newton-Raphson
- Each iteration only cuts the interval in half"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 9: REGULA FALSI METHOD (10:00 - 11:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Regula Falsi, also called the Method of False Position, is similar to bisection 
but smarter about where to pick the next point.

Instead of always taking the midpoint, it takes the x-intercept of the line 
connecting the two points (xl, f(xl)) and (xu, f(xu)).

Think about it: if you draw a straight line between these two points, where does 
that line cross the x-axis (where y=0)? That's probably closer to the actual root 
than the simple midpoint.

STEP 1: Check that a root exists
Same as bisection: f(xl) × f(xu) must be negative.

STEP 2: Calculate the weighted midpoint using the line formula
The line passing through (xl, f(xl)) and (xu, f(xu)) has slope:
slope = [f(xu) - f(xl)] / (xu - xl)

Using point-slope form and solving for where y=0:
xr = xu - [f(xu) × (xl - xu)] / [f(xl) - f(xu)]

This is the x-intercept of the line—a weighted estimate of where the root is.

STEP 3: Evaluate and proceed
Same as bisection:
- Calculate f(xr)
- Calculate product = f(xl) × f(xr)
- If negative, move xu = xr; otherwise move xl = xr
- Calculate error
- Insert into table
- Update graph
- Check stopping criteria

The main difference from bisection is this formula for xr. It often converges 
faster because it makes an intelligent guess based on the function values, not 
just the geometric midpoint.

However, Regula Falsi can sometimes get stuck if the function has unusual shapes. 
The line interpolation might not be accurate for curved functions."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 10: NEWTON-RAPHSON METHOD (11:30 - 13:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Newton-Raphson is a powerful method that converges much faster than bisection 
or Regula Falsi.

The key insight is using the derivative of the function to predict where the 
root is.

GEOMETRIC INTUITION:
Imagine you're at point (x0, f(x0)) on a curve. The derivative f'(x0) tells you 
the slope of the curve at that point. Draw a tangent line at this point. Where 
does that tangent line cross the x-axis? That's your next guess for the root.

MATHEMATICAL FORMULA:
The derivative f'(x0) represents how steep the curve is. If the slope is steep, 
the root is probably close. If the slope is shallow, the root is probably far away.

Newton-Raphson formula:
x_{i+1} = x_i - f(x_i) / f'(x_i)

IMPLEMENTATION STEPS:

STEP 1: Calculate the derivative numerically
We don't have a formula for f'(x), so we approximate it using a small step h:
f'(x) ≈ [f(x + h) - f(x)] / h

The code uses h = 1e-6, which is small enough to be accurate but large enough 
to avoid floating-point errors.

STEP 2: Apply Newton-Raphson formula
Starting with x0:
x1 = x0 - f(x0) / f'(x0)

STEP 3: Calculate error
ea = |(x1 - x0) / x1| × 100%

STEP 4: Store results and update graph
Insert iteration data into the table.
Add (x1, f(x1)) to the iteration points.
Update the graph showing convergence.

STEP 5: Check stopping criteria
If |f(x1)| < 1e-10 or error < tolerance, stop.
Otherwise, set x0 = x1 and repeat.

WHY NEWTON-RAPHSON IS POWERFUL:
Convergence is quadratic—meaning the number of correct digits roughly doubles 
with each iteration. You often get the answer in just 3-5 iterations.

WHY NEWTON-RAPHSON CAN FAIL:
If the derivative f'(x) becomes very small or zero, you're dividing by zero or 
a tiny number. This causes divergence or no convergence.

The code checks: if |f'(x)| < 1e-10, show an error message and stop.

OVERALL:
Newton-Raphson is extremely fast and works beautifully for well-behaved functions. 
It's often the go-to method in practice. But you need to be careful about the 
derivative being near zero."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 11: SECANT METHOD (13:30 - 15:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The Secant Method is like Newton-Raphson's friendlier cousin. It's almost as fast 
as Newton-Raphson but doesn't require calculating derivatives.

CORE IDEA:
Instead of using the tangent line at one point (Newton-Raphson), use the secant 
line connecting two previous points.

A secant line is just a straight line connecting two points on the curve. Where 
does this line cross the x-axis? That's your next guess.

MATHEMATICAL FORMULA:
Given two previous points x0 and x1, the secant line has slope:
slope = [f(x1) - f(x0)] / (x1 - x0)

Using this slope to find where y=0:
x2 = x1 - [f(x1) × (x1 - x0)] / [f(x1) - f(x0)]

IMPLEMENTATION STEPS:

STEP 1: Start with two initial guesses
x0 = lower bound (XL)
x1 = upper bound (XU)

STEP 2: Calculate next point using the secant formula
x2 = x1 - [f(x1) × (x1 - x0)] / [f(x1) - f(x0)]

STEP 3: Calculate error
ea = |(x2 - x1) / x2| × 100%

STEP 4: Store and visualize
Insert iteration data into the table.
Update the graph.

STEP 5: Check convergence
If |f(x2)| < 1e-10 or error < tolerance, stop and show success.
Otherwise, continue.

STEP 6: Update for next iteration
x0 = x1
x1 = x2

Then repeat from STEP 2.

WHY THE SECANT METHOD IS USEFUL:
- Almost as fast as Newton-Raphson (superlinear convergence)
- Doesn't need the derivative, so no division-by-zero issues
- Only needs two starting points, not a complicated formula
- Very practical and widely used

WHY IT'S DIFFERENT:
- Doesn't converge quite as fast as Newton-Raphson
- Requires two starting points instead of one
- More sensitive to the quality of initial guesses

OVERALL:
The Secant Method is like the 'Goldilocks' method—not too fast, not too slow, 
and not too fussy about initial conditions. It's a great choice when Newton-Raphson 
is problematic."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 12: LIVE GRAPH VISUALIZATION (15:00 - 16:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The plot_graph function creates and updates the live visualization. This is 
crucial for understanding how algorithms converge.

STEP 1: Clear the previous plot
self.ax.clear() removes everything from the graph so we start fresh.

STEP 2: Calculate the viewing window
The code uses smart zooming:

If we have a current root estimate xr:
  - Zoom into a small region around xr
  - Use zoom_factor = 30% of the original interval
  - Center the view on xr
  - This lets us see exactly where the algorithm is converging

If we don't have a root estimate (first call):
  - Show the full interval [xl, xu]
  - Add 80% margin on each side for context
  - This shows the user the full search space

STEP 3: Generate points to plot
Create 800 x-values using np.linspace(x_min, x_max, 800)
For each x-value, calculate y = f(x)
Use np.array() and list comprehension to create the y-values
Skip points where f(x) is NaN or infinite using np.isfinite()

STEP 4: Plot the function curve
self.ax.plot(x, y, linewidth=2.5, label="f(x)")
This draws the function curve in blue with a thick line.

STEP 5: Mark the current root estimate
If xr exists:
  self.ax.scatter([xr], [0], color="green", s=120, zorder=5, label="Current XR")
  This shows a bright green dot at (xr, 0)
  s=120 is the size, zorder=5 puts it on top

  self.ax.scatter([xr], [0], color="green", s=250, alpha=0.25, zorder=4)
  This adds a larger, semi-transparent halo around the dot

  self.ax.axvline(xr, linestyle=":", color="green", alpha=0.7)
  This draws a vertical dotted line from xr down to the x-axis

STEP 6: Draw the reference axes
self.ax.axhline(0, color="black", linewidth=1)        # The x-axis
self.ax.axvline(0, color="black", linewidth=1)        # The y-axis
self.ax.axvline(xl, linestyle="--", color="black", alpha=0.7, label="XL")  # Lower bound
self.ax.axvline(xu, linestyle="--", color="red", alpha=0.7, label="XU")    # Upper bound

STEP 7: Auto-detect all roots in the visible range
Loop through all plotted points looking for sign changes:
  If y[i] and y[i+1] have opposite signs, there's a root between them
  Use refine_root to find it precisely
  Check if we've already marked this root (within 1e-6)
  If not, add it to the roots list

STEP 8: Plot all detected roots
self.ax.scatter(roots, [0]*len(roots), color="green", s=80, label="Detected Roots")
self.ax.scatter(roots, [0]*len(roots), color="black", s=30, zorder=5)

This shows all detected roots as small dots on the x-axis, with black centers for contrast.

STEP 9: Auto-scale the y-axis intelligently
Get all finite y-values
Calculate the mean and range
If the range is huge (> 50), zoom to mean ± 25
Otherwise, show from min-1 to max+1

This prevents the graph from being useless when the function has extreme values.

STEP 10: Set final properties
self.ax.set_xlim(x_min, x_max)        # Set x-axis range
self.ax.set_title("Root Visualization")
self.ax.set_xlabel("x")
self.ax.set_ylabel("f(x)")
self.ax.grid(True, alpha=0.4)
self.ax.minorticks_on()
self.ax.legend()
self.fig.tight_layout()

STEP 11: Update the display
self.canvas.draw() tells tkinter to redraw the graph on screen.

The result: A beautiful, animated visualization showing the algorithm converging 
to the root!"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 13: MATRIX OPERATIONS TAB - SETUP (16:30 - 17:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Now let's move to the Matrix Operations tab.

The setup_matrix_tab function creates the interface for all matrix operations.

TOP CONTROL PANEL:
- A dropdown to select operation: Addition, Multiplication, Transpose, Determinant, 
  Inverse, Adjoint, Power, Equation
- Default is Addition
- A hidden 'Power' selector that only shows when Power operation is chosen
- Buttons for Compute and Clear

BELOW THAT - SIZE CONTROL:
- A dropdown to choose Target: Matrix A or B
- Input fields for Rows and Columns
- A 'Set Size' button to resize the selected matrix

MIDDLE SECTION - MATRIX INPUT:
- LEFT SIDE: A large text area labeled 'Matrix A'
  Default: 1 2
           3 4
  Below it: A label showing the current size 'Matrix A Size: 2 x 2'
  The text area has a keyboard event binding that updates the size label as 
  you type

- RIGHT SIDE: A large text area labeled 'Matrix B (if needed)'
  Default: 5 6
           7 8
  Same size label below

BOTTOM SECTION - RESULTS:
- A large text area labeled 'Result'
- A scrollbar for long results
- This is where we display the output of matrix operations

The on_matrix_op_change function is bound to the operation dropdown. When you 
select 'Power', it shows the Power selector. When you select anything else, 
it hides it."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 14: MATRIX PARSING AND VALIDATION (17:45 - 19:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The parse_matrix function converts text input into a usable matrix.

INPUT: A string like:
1 2
3 4

PROCESS:

STEP 1: Split by newlines
rows = [r for r in str_data.strip().split("\n") if r.strip() != ""]

This splits the text into individual lines and removes empty lines.

STEP 2: Check if matrix is empty
if len(rows) == 0:
    raise ValueError("Empty matrix")

STEP 3: Parse each row
Initialize an empty matrix list.
For each row string:
  - Strip whitespace
  - Split by spaces to get individual values
  - Skip if the row is empty
  - Convert each value to float
  - Add the row to the matrix

For example, "1 2" becomes [1.0, 2.0]

STEP 4: Validate dimensions
Get the number of columns from the first row: row_len = len(matrix[0])
Check that ALL rows have exactly this many columns
If any row has a different number of columns, raise an error

This ensures we have a valid rectangular matrix.

OUTPUT: A list of lists:
[[1.0, 2.0],
 [3.0, 4.0]]

The matrix_to_string function does the reverse—converts a matrix back to 
formatted text for display:

For each row:
  For each element:
    Format as a 10-character field with 4 decimal places
Join all rows with newlines

The result is nicely aligned numbers that look professional.

The matrix_size function simply returns a string like '2 x 2' by checking 
the number of rows and columns."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 15: BASIC MATRIX OPERATIONS (19:00 - 20:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Let's look at the actual matrix operations:

ADDITION - add(A, B):
Requires: Both matrices must have the same dimensions
Formula: C[i][j] = A[i][j] + B[i][j]

Implementation:
r = len(A)          # number of rows
c = len(A[0])       # number of columns
return [[A[i][j] + B[i][j] for j in range(c)] for i in range(r)]

This uses nested list comprehensions to create a new matrix where each element 
is the sum of the corresponding elements.

MULTIPLICATION - multiply(A, B):
Requires: A's columns must equal B's rows
Formula: C[i][j] = Σ(A[i][k] × B[k][j]) for all k

Implementation:
r = len(A)          # A has r rows
c = len(B[0])       # B has c columns
C = [[0.0 for _ in range(c)] for _ in range(r)]  # Create result matrix

for i in range(r):          # For each row of A
    for j in range(c):      # For each column of B
        for k in range(len(B)):  # Sum over the shared dimension
            C[i][j] += A[i][k] * B[k][j]

This triple-nested loop computes the dot product for each position.

TRANSPOSE - transpose(A):
Flips rows and columns.
If A is m×n, result is n×m.

Formula: T[j][i] = A[i][j]

Implementation:
return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

This creates a new matrix where we iterate through columns of the original 
and use them as rows in the transposed matrix.

MATRIX POWER - matrix_power(A, exponent):
Raises a square matrix to a positive integer power.

Validation:
- Matrix must be square
- Exponent must be a positive integer

Implementation:
result = A
for _ in range(1, exponent):
    result = multiply(result, A)

So A^2 = A × A, and A^3 = A × A × A, etc."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 16: ADVANCED MATRIX OPERATIONS - PART A (20:30 - 22:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Now for the more complex operations:

DETERMINANT - determinant(A):
The determinant is a single number that tells you important information about 
a matrix.

For a 2×2 matrix:
[a b]
[c d]

det = (a×d) - (b×c)

For larger matrices, the code uses recursive cofactor expansion:

def determinant(A):
    if len(A) == 1:
        return A[0][0]  # Base case: 1×1 matrix
    
    det = 0.0
    for i in range(len(A)):
        # For each element in the first row
        # Calculate cofactor: (-1)^i × A[0][i] × determinant(minor)
        det += ((-1) ** i) * A[0][i] * determinant(minor(A, 0, i))
    
    return det

What's a minor? It's the determinant of a smaller matrix created by deleting 
a row and column.

The minor function:
def minor(A, row, col):
    n = len(A)
    return [
        [A[i][j] for j in range(n) if j != col]
        for i in range(n) if i != row
    ]

It creates a new matrix by removing the specified row and column.

For example, for a 3×3 matrix, removing row 0 and column 1 gives a 2×2 matrix.

This recursive approach works but gets slow for large matrices. It's perfectly 
fine for educational purposes and small matrices.

WHY THE DETERMINANT MATTERS:
- If det(A) = 0, the matrix is singular (can't be inverted)
- If det(A) ≠ 0, the matrix is regular (invertible)
- The absolute value of the determinant relates to scaling area/volume
- Used to solve systems of linear equations using Cramer's rule"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 17: ADVANCED MATRIX OPERATIONS - PART B (22:00 - 23:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"ADJOINT - adjoint(A):
The adjoint matrix is used to calculate the inverse.

Definition: The adjoint is the transpose of the cofactor matrix.

Cofactor: For position [i][j], calculate (-1)^(i+j) × det(minor(A, i, j))

Implementation:
def adjoint(A):
    n = len(A)
    return [
        [((-1) ** (i + j)) * determinant(minor(A, i, j)) for i in range(n)]
        for j in range(n)
    ]

Wait, notice the indices are swapped! The inner loop iterates i (rows), and the 
outer loop iterates j (columns). This is actually the transpose operation—the 
return statement is already transposed!

So this function calculates the matrix of cofactors and transposes it in one step.

INVERSE - inverse(A):
The inverse of a matrix A is another matrix A^(-1) such that A × A^(-1) = I 
(the identity matrix).

Formula: A^(-1) = adjoint(A) / det(A)

Implementation:
def inverse(A):
    det = determinant(A)
    if abs(det) < 1e-12:
        raise ValueError("Singular matrix")  # Can't invert
    
    n = len(A)
    adj = adjoint(A)
    return [[adj[i][j] / det for j in range(n)] for i in range(n)]

Steps:
1. Calculate the determinant
2. Check if det ≈ 0 (singular). If so, raise an error.
3. Calculate the adjoint matrix
4. Divide every element by the determinant
5. Return the result

SOLVING LINEAR EQUATIONS - solve_equation(A, B):
The system A × X = B can be solved as X = A^(-1) × B

Implementation:
def solve_equation(A, B):
    invA = inverse(A)
    return multiply(invA, B)

This is straightforward: compute the inverse and multiply.

Real-world example:
2x + 3y = 8
4x + y = 10

Written in matrix form:
[2 3] × [x]   [8]
[4 1]   [y] = [10]

So A = [[2,3], [4,1]], B = [[8], [10]]
Then X = A^(-1) × B = [[x], [y]]"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 18: MATRIX COMPUTATION ENGINE (23:45 - 25:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The compute_matrix function is the central dispatcher for all matrix operations.

STEP 1: Get inputs
A_text = self.matrix_a.get("1.0", "end").strip()   # All text from matrix A
B_text = self.matrix_b.get("1.0", "end").strip()   # All text from matrix B
op = self.matrix_combo.get()                        # Selected operation

STEP 2: Check if matrix A is provided
if not A_text:
    messagebox.showwarning("Input Error", "Enter Matrix A")
    return

STEP 3: Parse matrix A
A = parse_matrix(A_text)

STEP 4: Clear previous result
self.matrix_result.delete("1.0", "end")

STEP 5: Initialize result
result = None

STEP 6: Execute the appropriate operation using a switch-like structure

if op == "Addition":
    Check that matrix B exists
    Parse matrix B
    Check dimensions match
    result = add(A, B)

elif op == "Multiplication":
    Check that matrix B exists
    Parse matrix B
    Check A's columns == B's rows
    result = multiply(A, B)

elif op == "Transpose":
    No validation needed for transpose
    result = transpose(A)

elif op == "Determinant":
    Check matrix is square
    det = determinant(A)
    Display: "Determinant = 15.4356"
    Return (no result matrix to display)

elif op == "Inverse":
    Check matrix is square
    Call inverse(A) which checks for singular matrix
    result = inverse(A)

elif op == "Adjoint":
    Check matrix is square
    result = adjoint(A)

elif op == "Power":
    Check matrix is square
    Get the exponent from power_combo (default 2)
    result = matrix_power(A, exponent)

elif op == "Equation":
    Check that matrix B exists
    Parse matrix B
    Check A is square and B has compatible dimensions
    result = solve_equation(A, B)

STEP 7: Display result
if isinstance(result, str):
    self.matrix_result.insert("end", result)
else:
    self.matrix_result.insert("end", matrix_to_string(result))

STEP 8: Show success
messagebox.showinfo("Success", "Operation completed!")

STEP 9: Error handling
Wrap everything in try-except:
- ValueError for dimension mismatches
- Other exceptions for parsing or computation errors
- Show error dialog with details"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 19: THE MAIN APPLICATION CLASS (25:30 - 26:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The NumericalMethodsApp class is the heart of the GUI application.

__init__ method:
This runs when you create the application.

self.root = root                    # Store reference to the tk window
self.root.title("Numerical Methods")     # Set window title
self.root.geometry("1600x900")      # Set size to 1600×900 pixels
self.root.minsize(1200, 700)        # Don't allow smaller than 1200×700
self.current_root_marker = None     # No current root estimate yet
self.iteration_points = []          # List of points plotted

self.current_theme = Theme.LIGHT    # Start with light theme
self.root.configure(bg=self.current_theme['bg'])  # Set window background

Then it creates the interface:
self.create_header()          # Build the title bar
self.create_main_content()    # Build the tabs

setup_styles method:
This configures how all GUI elements look.

It creates a ttk.Style() object which lets you define custom styles for:
- Headers: Large bold font (Segoe UI, 20 pt, bold)
- Subheaders: Medium bold (Segoe UI, 12 pt, bold)
- Regular labels: (Segoe UI, 10 pt)
- Buttons: (Segoe UI, 10 pt, bold) with padding
- Text entries and dropdowns: padding of 5 pixels
- Tables: Courier New (monospace) 9pt for proper alignment

apply_theme method:
After setup_styles, this applies the actual colors.

It modifies all the style configurations to use colors from self.current_theme.

For example:
self.ttk_style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
self.ttk_style.configure('Header.TLabel', background=theme['bg'], 
                        foreground=theme['accent'])

This makes all labels use the theme's background and text colors.

create_header method:
Creates the title bar at the top.

header_frame = ttk.Frame(self.root)
header_frame.pack(fill="x", padx=0, pady=0)

title_label = ttk.Label(header_frame, text="NUMERICAL METHODS", 
                       style='Header.TLabel')
title_label.pack(side="left", padx=20, pady=15)

ttk.Frame(header_frame).pack(side="left", fill="x", expand=True)  # Spacer
ttk.Separator(self.root, orient='horizontal').pack(fill="x")      # Line

This creates a header with the title on the left and a horizontal line below."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 20: UTILITY AND HELPER FUNCTIONS (26:45 - 27:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Several helper functions make the interface work smoothly:

clear_root_table method:
for row in self.tree.get_children():
    self.tree.delete(row)

This deletes all rows from the iteration table when you click Clear.

matrix_size_from_text method:
def matrix_size_from_text(self, text):
    if not text.strip():
        return "Empty"
    try:
        return matrix_size(parse_matrix(text))
    except Exception:
        return "Invalid"

This tries to parse text and return the size. If it fails, returns "Invalid".
Useful for displaying live validation as the user types.

update_matrix_size_labels method:
Called automatically when the user types in either matrix text area (via a 
<<KeyRelease>> event binding).

Updates the labels below each text area to show the current matrix dimensions.

on_matrix_op_change method:
Called whenever the user changes the selected operation.

If Power is selected:
    Show the power selector (exponent dropdown)
    Disable the target selector (force it to be A)

Else:
    Hide the power selector
    Enable the target selector

resize_matrix method:
Let's user change matrix dimensions.

Reads Rows and Cols input
Validates they're positive integers
Gets the Target (A or B)
Calls fill_matrix_widget to resize and preserve existing values

fill_matrix_widget method:
Resizes a matrix to new dimensions while preserving existing values.

If new size is smaller, keep only the values that fit
If new size is larger, fill new positions with 0.0

This is intelligent—it doesn't just clear everything, it tries to preserve data."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 21: COMPLETE WORKFLOW EXAMPLES (27:45 - 29:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Let's walk through two complete examples:

EXAMPLE 1: FINDING A ROOT

User enters:
- Equation: x^3 - x - 2
- Method: Bisection
- Lower Bound: 1
- Upper Bound: 2
- Tolerance: 0.0001
- Clicks Solve

What happens:

1. normalize_expression converts 'x^3 - x - 2' to 'x**3 - x - 2'
2. parse_function creates a function that evaluates this
3. Test: f(1) = 1 - 1 - 2 = -2 (negative)
4. Test: f(2) = 8 - 2 - 2 = 4 (positive)
5. Sign change found! Root exists in [1, 2]

6. Bisection begins:
   Iteration 1: xr = 1.5, f(1.5) ≈ -0.125 → negative, so root is in [1.5, 2]
   Iteration 2: xr = 1.75, f(1.75) ≈ 1.609 → positive, so root is in [1.5, 1.75]
   ... (continues narrowing down)
   Iteration 11: xr ≈ 1.521, error = 0.00009% < tolerance
   
7. Success message: "Root found at x = 1.5214..."
8. Graph shows the curve with the green dot at x ≈ 1.521

EXAMPLE 2: MULTIPLYING MATRICES

User enters:
- Matrix A: 1 2    →   [[1, 2],
             3 4   →    [3, 4]]

- Matrix B: 5 6    →   [[5, 6],
             7 8   →    [7, 8]]

- Operation: Multiplication
- Clicks Compute

What happens:

1. Parse A and B: dimensions OK (2×2)
2. Check: A's columns (2) == B's rows (2) ✓
3. Multiply:
   C[0][0] = (1×5) + (2×7) = 5 + 14 = 19
   C[0][1] = (1×6) + (2×8) = 6 + 16 = 22
   C[1][0] = (3×5) + (4×7) = 15 + 28 = 43
   C[1][1] = (3×6) + (4×8) = 18 + 32 = 50

4. Result displayed:
      19.0000  22.0000
      43.0000  50.0000

5. Success message shown"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 22: KEY TECHNICAL FEATURES (29:00 - 30:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Several technical features make this application robust and professional:

IMPLICIT MULTIPLICATION:
Users can type '2x' instead of '2*x'
Uses regex pattern matching: re.sub(r'(?<=\d)(?=[x\(])', '*', expr)
Makes the interface much more user-friendly

NUMERICAL STABILITY:
Uses refine_root to polish answers to 10 decimal places
Checks for NaN and infinity values
Handles edge cases like zero denominators gracefully

REAL-TIME UPDATES:
Calls self.root.update_idletasks() after each iteration
Allows users to see convergence happening in real-time
Makes the visualization truly dynamic

MATPLOTLIB INTEGRATION:
FigureCanvasTkAgg embeds matplotlib into Tkinter
Updates with self.canvas.draw()
Smart zooming logic to keep the graph useful
Auto-detection of roots in the visible range

COMPREHENSIVE ERROR HANDLING:
All user input is validated
Dimension checking for matrix operations
Division-by-zero protection in formulas
Singular matrix detection
Informative error messages guide users

PRECISION FORMATTING:
Matrix output formatted with 4 decimal places
Fixed-width fields for alignment
Readable iteration table with proper column widths

THEME SYSTEM:
Color dictionaries for easy customization
Light and dark themes included
Adaptable to user preferences"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 23: CONCLUSION AND SUMMARY (30:00 - 31:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"In this comprehensive walkthrough, we've explored every aspect of the Numerical 
Methods Python application.

We started with the parsing system that converts natural math notation into 
executable code. We examined five different root-finding algorithms, each with 
different strengths:

- Incremental: Simple, reliable, slow
- Bisection: Guaranteed convergence, moderate speed
- Regula Falsi: Faster than bisection when it works
- Newton-Raphson: Quadratic convergence, very fast, can fail
- Secant: Almost as fast as Newton-Raphson, more stable

We explored eight matrix operations using pure Python without external libraries, 
implementing everything from scratch: addition, multiplication, transpose, 
determinant, inverse, adjoint, power, and equation solving.

We covered the GUI architecture using Tkinter, the live visualization with 
Matplotlib, and the robust error handling that makes the application professional 
and user-friendly.

This application demonstrates several important programming principles:

1. Separation of Concerns: Math functions are separate from GUI code
2. Error Handling: Comprehensive try-catch blocks prevent crashes
3. User Experience: Real-time feedback, clear error messages, validation
4. Scalability: Easy to add new methods or operations
5. Maintainability: Well-organized structure, meaningful variable names

Whether you're a student learning numerical methods, an engineer solving real 
problems, or a programmer interested in GUI development, this application serves 
as an educational tool and a practical utility.

The code is well-structured, extensively commented in our walkthrough, and 
demonstrates best practices in Python application development.

Thank you for watching this complete breakdown of the Numerical Methods 
application. Whether you use this code as a learning resource, adapt it for 
your own projects, or simply appreciate the mathematics behind root-finding 
algorithms, I hope you've found this educational and inspiring.

If you have questions about specific functions, methods, or mathematical 
concepts, feel free to ask in the comments. Happy coding!"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 24: APPENDIX - TIME BREAKDOWN (31:00 - END)
════���══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

[DETAILED TIMING GUIDE FOR VIDEO EDITING]

Introduction and Overview: 1:00
Imports and Dependencies: 0:45
Theme System: 1:00
Function Parser: 1:45
Root Finding Tab Interface: 1:15
Solve Root Function: 1:15
Incremental Search Method: 1:15
Bisection Method: 1:45
Regula Falsi Method: 1:30
Newton-Raphson Method: 2:00
Secant Method: 1:30
Live Graph Visualization: 1:30
Matrix Operations Tab Setup: 1:15
Matrix Parsing and Validation: 1:15
Basic Matrix Operations: 1:30
Advanced Matrix Operations - Part A: 1:30
Advanced Matrix Operations - Part B: 1:45
Matrix Computation Engine: 1:45
Main Application Class: 1:15
Utility and Helper Functions: 1:00
Complete Workflow Examples: 1:15
Key Technical Features: 1:00
Conclusion and Summary: 1:00

TOTAL: ~31 minutes of comprehensive content

RECOMMENDED VIDEO EDITING ADDITIONS:
- Code highlighting for syntax clarity
- Animated transitions between sections
- On-screen callouts for important concepts
- Live demonstrations of the application
- Screen recordings of algorithms in action
- Animated graphs showing convergence
- Split-screen comparisons of different methods
- Interactive elements showing mathematical concepts

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

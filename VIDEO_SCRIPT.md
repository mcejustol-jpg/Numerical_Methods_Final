NUMERICAL METHODS APPLICATION - VIDEO SCRIPT
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

PYTHON
═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 1: INTRODUCTION (0:00 - 0:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Welcome to the Numerical Methods application. This Python program demonstrates
five different algorithms for finding roots of equations, and eight matrix 
operations. Built with Tkinter for the interface, NumPy for calculations, and 
Matplotlib for visualization.

The application is divided into two main tabs: 'Root Finding Methods' and 
'Matrix Operations'. Let's explore what each section does."

═════════════════════════════════════════════════════════════════════════════════════════════════════���═════════════════════════════════
SECTION 2: FUNCTION PARSER & THEME SYSTEM (0:30 - 1:15)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The application starts with a Theme class that defines light and dark color 
schemes for styling. The heart of the root-finding system is the 
parse_function method, which converts user-entered mathematical expressions—
like 'x^3 - x - 2'—into executable Python functions.

Notice the normalize_expression function handles equation rearrangement, converts 
carets to double asterisks for exponentiation, and supports implicit multiplication. 
For example, '3x' becomes '3*x', and '2(x+1)' becomes '2*(x+1)'.

This is critical because it allows users to type math naturally, without worrying 
about Python syntax."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 3: ROOT FINDING TAB - INTERFACE (1:15 - 2:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The Root Finding tab has a configuration panel at the top. Here you enter 
an equation, select from five methods: Incremental, Bisection, Regula Falsi, 
Newton-Raphson, and Secant.

You specify your lower bound (XL), upper bound (XU), and a tolerance threshold—
how close to zero you want to get before stopping.
	
Below the controls is an iteration results table showing each step, and to the 
right, a live graph visualization that updates with each iteration. The table 
includes columns for iteration number, bounds, function values, approximate error 
percentage, the product of function values, and status remarks."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 4: ROOT FINDING METHODS - PART A (2:00 - 3:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Let's examine the five root-finding algorithms:

INCREMENTAL SEARCH: Walks through the interval in small steps, checking where 
the function changes sign. When f(x₀) times f(x₁) is negative, a root is detected.
The step size is calculated as: step = (xu - xl) / 200
This method is simple but not the fastest.

BISECTION METHOD: Divides the interval in half repeatedly. If the product of 
function values at the bounds is negative, the root must be in one half. The 
method tracks approximate error using:
	Ea = |(xr_new - xr_old) / xr_new| × 100%
It guarantees convergence as long as a root exists in the initial interval."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 5: ROOT FINDING METHODS - PART B (3:00 - 4:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"REGULA FALSI uses a weighted approach: instead of the midpoint, it calculates 
the x-intercept of the line connecting the two bounds. This often converges faster 
than bisection.

Formula: xr = xu - [f(xu)(xl-xu)] / [f(xl) - f(xu)]

The method then checks the sign product to determine which half contains the root.

NEWTON-RAPHSON is more sophisticated. It uses the derivative of the function 
to calculate the next approximation. The derivative is estimated numerically 
using a small step h:

f'(x) ≈ [f(x+h) - f(x)] / h

Then: x_{i+1} = x_i - f(x_i) / f'(x_i)

This converges much faster but can fail if the derivative becomes too small."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 6: ROOT FINDING METHODS - PART C (4:00 - 4:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Finally, the SECANT METHOD is similar to Newton-Raphson, but it approximates 
the derivative using two previous points instead of calculating it directly:

x_{i+1} = x_i - [f(x_i)(x_i - x_{i-1})] / [f(x_i) - f(x_{i-1})]

This is advantageous because you don't need the exact derivative function. It's 
faster than bisection but slightly slower than Newton-Raphson.

All methods update the graph in real-time and display a success message when 
a root is found within the tolerance. The refine_root helper function uses 
bisection internally to polish the final answer for maximum accuracy."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 7: GRAPH VISUALIZATION IN PYTHON (4:45 - 5:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The plot_graph function creates a dynamic visualization using Matplotlib. It:

1. Clears the previous plot
2. Calculates the zoom level based on whether we have a current root estimate
3. Generates 800 x-values in the visible range
4. Evaluates the function at each point
5. Plots the curve in blue with a 2.5-pixel linewidth
6. Adds reference lines: y=0 (black), x=xl (dashed black), x=xu (dashed red)
7. Plots the current root estimate xr as a green scatter point with a halo effect
8. Auto-detects and marks all roots in the visible range using sign changes

The graph auto-scales the y-axis to keep the visible function region centered, 
preventing the view from getting cluttered when the function has extreme values."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 8: MATRIX OPERATIONS (5:30 - 6:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The Matrix Operations tab provides eight operations:

ADDITION and MULTIPLICATION perform standard linear algebra operations.
Addition is element-wise: C[i][j] = A[i][j] + B[i][j]
Multiplication uses the triple-nested loop: C[i][j] = Σ(A[i][k] * B[k][j])

TRANSPOSE flips rows and columns: the element at position [i][j] moves to [j][i]

DETERMINANT calculates the single scalar value using recursive cofactor expansion:
det(A) = Σ((-1)^i × A[0][i] × det(minor(A, 0, i)))

INVERSE uses the adjoint matrix divided by the determinant:
A⁻¹ = adjoint(A) / det(A)
with error checking for singular matrices where determinant ≈ 0

ADJOINT computes the matrix of cofactors and transposes it.

POWER raises a square matrix to a positive integer exponent through repeated 
multiplication.

EQUATION solves the system A·X = B by computing X = A⁻¹·B"

════════════════════════════════════════════════════════════════════════════════════════════���══════════════════════════════════════════
SECTION 9: MATRIX INPUT & COMPUTATION (6:45 - 7:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Users input matrices as plain text—rows separated by newlines, values by spaces.
For example:
	1 2
	3 4

The parse_matrix function handles this by:
1. Splitting text by newlines
2. Splitting each line by whitespace
3. Converting strings to floats
4. Validating all rows have the same column count

The matrix_size_from_text helper displays matrix dimensions in real-time as the 
user types. When you compute, results appear in a formatted output area with 
proper alignment and precision.

All operations include comprehensive error handling—checking if matrices are 
square when required, if dimensions are compatible for multiplication, and if 
the operation is mathematically valid."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 10: KEY FEATURES & CONCLUSION (7:30 - 8:15)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Key features of this Python version:

• Dynamic function parsing with implicit multiplication support
• Real-time graph visualization with smart zooming around root estimates
• Dual-tab interface for clean organization
• Comprehensive error handling with user-friendly message boxes
• Light and dark theme support through the Theme class
• Iteration tracking and approximate error calculation
• Live graph updates showing algorithm convergence
• Numerical stability through refine_root polishing

The application leverages NumPy for vectorized calculations, Tkinter for the 
native GUI, and Matplotlib for publication-quality graphs. This is a complete 
educational tool for understanding how numerical methods converge on solutions, 
making abstract mathematics tangible and interactive.

Thank you for watching!"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════




MATLAB
═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 1: INTRODUCTION (0:00 - 0:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"This is the MATLAB version of the Numerical Methods application. Built using 
MATLAB's App Designer, it provides the same functionality as the Python version—
five root-finding algorithms and matrix operations—but with MATLAB's native 
GUI framework and computation engine.

The MATLAB version runs as a compiled app and demonstrates how the same 
mathematical concepts translate across different programming languages."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 2: GUI CONSTRUCTION - MAIN WINDOW (0:30 - 1:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The application starts by creating a figure window—1600 by 900 pixels. Then 
a tab group is added to organize two tabs: 'Root Finding Methods' and 
'Matrix Operations'.

In MATLAB, uifigure creates modern-looking windows, and uitabgroup organizes 
content into tabs. Each UI element is positioned absolutely using pixel coordinates, 
giving precise control over layout.

Root Tab contains:
• An equation input field with default equation x^3 + 3x^2 - 4x - 12
• A dropdown to select which method to use
• Numeric input fields for Lower Bound, Upper Bound, and Tolerance
• Solve and Clear buttons
• A results table (uitable) with scrolling capability
• A visualization axes object for plotting the function and roots

The Matrix Tab contains similar components but focused on matrix input and 
selection of operations."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 3: FUNCTION PARSER IN MATLAB (1:30 - 2:15)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The parseFunction nested function is critical for handling user input. It:

1. Converts the expression to lowercase for consistency
2. Removes all spaces to avoid parsing issues
3. Replaces the caret symbol ^ with .^ for element-wise power operations
4. Uses regular expressions to insert multiplication operators

For example:
	'3x' becomes '3.*x'
	'(x)(2)' becomes '(x).*(2)'
	'2(x+1)' becomes '2.*(x+1)'

Finally, it converts the string to a function handle using str2func, creating 
an anonymous function @(x) that MATLAB can evaluate numerically over arrays.

This allows the same mathematical expression to work for both single values 
and vector inputs for plotting."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 4: ROOT FINDING METHODS IN MATLAB (2:15 - 3:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The solveRoot callback function is triggered when you click Solve. It:

1. Parses the equation into a function handle using parseFunction
2. Extracts parameters: xl, xu, tolerance from the input fields
3. Initializes the results table
4. Calls the appropriate method using a switch statement

INCREMENTAL METHOD:
Iterates from xl to xu in 0.1 steps. For each position, checks if f(x) and 
f(x+step) have opposite signs—indicating a root is nearby. Displays all intervals 
in the results table.

BISECTION METHOD:
For each iteration:
• Calculates midpoint: xr = (xl + xu) / 2
• Evaluates function at xl and xr
• If their product is negative, updates xu = xr (root in left half)
• Otherwise, updates xl = xr (root in right half)
• Calculates approximate error: Ea = |(xr_new - xr_old) / xr| × 100%
• Updates the graph in real time using drawnow
• Inserts a new row into the results table with all iteration data
• Stops when error drops below tolerance or absolute function value < 1e-10"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 5: MORE ROOT FINDING METHODS (3:45 - 5:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"REGULA FALSI METHOD:
Unlike bisection's midpoint, this uses the x-intercept of the secant line 
connecting the two bounds. This weighted approach often converges faster:

xr = xu - [f(xu)(xl - xu)] / [f(xl) - f(xu)]

The method then checks the sign product to determine which half contains the root, 
similar to bisection.

NEWTON-RAPHSON METHOD:
Estimates the derivative numerically with a small step h = 1e-6:

f'(x) ≈ [f(x+h) - f(x)] / h

Then applies the Newton-Raphson formula:

x_{i+1} = x_i - f(x_i) / f'(x_i)

This converges quadratically—very fast—but can diverge if the derivative becomes 
too close to zero.

SECANT METHOD:
Approximates the derivative using two previous points instead of calculating it:

x_{i+1} = x_i - [f(x_i)(x_i - x_{i-1})] / [f(x_i) - f(x_{i-1})]

This avoids computing derivatives directly, making it more stable than Newton-Raphson 
in some cases.

All methods insert their iteration data into the results table and call plotGraph 
to visualize progress in real time."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 6: GRAPH VISUALIZATION (5:00 - 5:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The plotGraph function creates a dynamic visualization using MATLAB's plotting 
capabilities. It:

1. Clears the previous plot using cla
2. Generates 1000 x-values between xl-5 and xu+5 using linspace
3. Evaluates the function at each point using the function handle
4. Plots the curve in blue with appropriate line properties
5. Adds reference lines:
   • y=0 (horizontal line, black)
   • x=xl (vertical line, green dashed)
   • x=xu (vertical line, red dashed)
6. Plots the current root estimate xr as a green scatter point
7. Sets axis labels and title
8. Uses grid on for readability

The graph updates with each iteration using drawnow, providing immediate visual 
feedback showing the algorithm converging toward the actual root. This real-time 
visualization is invaluable for understanding how each method approaches the 
solution and how quickly it converges."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 7: MATRIX OPERATIONS IN MATLAB (5:45 - 7:00)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"The Matrix tab provides eight operations, accessible through a dropdown menu 
and two text areas for Matrix A and B input. The computeMatrix function handles 
the switch statement:

ADDITION: R = A + B (element-wise addition)

MULTIPLICATION: R = A * B (matrix multiplication, not element-wise—MATLAB's 
default * operator does true matrix multiplication)

TRANSPOSE: R = A' (MATLAB's simple and elegant transpose operator)

DETERMINANT: R = det(A) (built-in function, returns a scalar)

INVERSE: R = inv(A) (built-in inverse function, with error handling for 
singular matrices)

ADJOINT: R = det(A) * inv(A) (mathematical definition of adjoint)

POWER: R = A^2 (matrix squared, equivalent to A * A, not element-wise)

EQUATION: R = A \ B (MATLAB's backslash operator solves A·X = B directly using 
LU decomposition, more numerically stable than X = inv(A)*B)

Results are displayed using the disp function, which formats output nicely in 
the text area."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 8: MATRIX INPUT PARSING (7:00 - 7:45)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Users input matrices as multi-line text. The parseMatrix function:

1. Takes the text from the input area
2. Splits it by newlines using splitlines or similar string operations
3. For each line, splits by whitespace
4. Converts strings to numbers using str2num
5. Validates dimensions

For example:
	User types:
	1 2
	3 4
	
	Becomes the 2×2 matrix:
	[1  2]
	[3  4]

Results are displayed using evalc and disp, which capture the console output 
formatting and display it in the result text area. This is a clean way to format 
numerical results and matrices in MATLAB, preserving alignment and precision."

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
SECTION 9: ERROR HANDLING & CONCLUSION (7:45 - 8:30)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

"Both the Root Finding and Matrix tabs use try-catch blocks for robust error 
handling. Common error scenarios include:

• Invalid equation syntax that can't be parsed
• Non-numeric input in fields requiring numbers
• Singular matrices (determinant ≈ 0) when trying to compute inverse
• Dimension mismatches for matrix operations
• Division by zero in method-specific calculations

When an error occurs, the uialert function displays a user-friendly error dialog 
explaining what went wrong, rather than crashing the application.

This MATLAB version leverages MATLAB's strengths: built-in numerical functions 
optimized for speed, native plotting with instant updates, and a clean GUI 
framework through App Designer.

In summary, both versions—Python and MATLAB—teach the same numerical methods 
concepts but use their respective language strengths. The Python version offers 
flexibility and open-source tools, while MATLAB excels in numerical computation 
and visualization built specifically for mathematics.

Both implementations demonstrate that numerical methods are language-agnostic—
the mathematics remains the same whether you code in Python, MATLAB, C++, or 
any other language.

Thank you for exploring this Numerical Methods application!"

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

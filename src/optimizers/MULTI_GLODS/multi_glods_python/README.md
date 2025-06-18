# multi_glods_python

Python-based MultiGLODS optimizer compatible with the [AntennaCAT](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool) optimizer suite.  Now featuring AntennaCAT hooks for GUI integration and user input handling.

The [multi_glods_python](https://github.com/jonathan46000/multi_glods_python) by [jonathan46000](https://github.com/jonathan46000), is a Python translation of MATLAB MultiGLODS 0.1 (with random search method only). Please see the [MultiGLODS](#multiglods) and [Translation of MultiGLODS to Python](#translation-of-multiglods-to-python) sections for more information about the translation of the code and the original publication.


## Table of Contents
* [MultiGLODS](#multiglods)
* [Translation of MultiGLODS to Python](#translation-of-multiglods-to-python)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Initialization](#initialization) 
    * [State Machine-based Structure](#state-machine-based-structure)
    * [Constraint Handling](#constraint-handling)
    * [Boundary Types](#boundary-types)
    * [Objective Function Handling](#objective-function-handling)
      * [Creating a Custom Objective Function](#creating-a-custom-objective-function)
      * [Internal Objective Function Example](internal-objective-function-example)
* [Example Implementations](#example-implementations)
    * [Basic Example](#basic-example)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Related Publications and Repositories](#related-publications-and-repositories)
* [Licensing](#licensing)  


## MultiGLODS

The Multiobjective Optimization Global and Local Optimization using Direct Search (MultiGLODS) [1] is an algorithm created by Dr. Ana Luise Custódio (Nova School of Science and Technology, Lisbon) and J. F. A. Madeira (ISEL and IDMEC-IST, Lisbon). It is a derivative-free optimizer generalized for calculating the Pareto fronts of multiobjective multimodal derivative-free optimization problems. It builds off their GLODS algorithm in [2]. 

Some key points of this algorithm are:

* "The proposed algorithm alternates between initializing new searches, using a multistart strategy, and exploring promising subregions, resorting to directional direct search. Components of the objective function are not aggregated and new points are accepted using the concept of Pareto dominance. The initialized searches are not all conducted until the end, merging when they start to be close to each other. The convergence of the method is analyzed under the common assumptions of directional direct search. Numerical experiments show its ability to generate approximations to the different Pareto fronts of a given problem." [1]

* "Points sufficiently close to each other are compared and only nondominated points will remain active. In the end of the optimization process, the set of all active points will define the approximations to the Pareto fronts of the problem (local and global)." [1]


## Translation of MultiGLODS to Python
From the main branch [multi_glods_python README:](https://github.com/jonathan46000/multi_glods_python/blob/main/README.md)

The original MultiGLODS 0.1 is written in MATLAB by Dr. Ana Luise Custódio and 
J. F. A. Madeira at the Nova School of Science and Technology and at ISEL and IDMEC-IST, Lisbon
respectively.  Please use the following references and complementary material:

A. L. Custódio and J. F. A. Madeira, MultiGLODS: Global and Local Multiobjective 
Optimization using Direct Search, Journal of Global Optimization, 72 (2018), 323 - 345 PDF

This Python project, moves MultiGLODS to a state based design so that the objective function calls
are de-embedded from loops and could be executed as callbacks with minor modification. The translation
to Python allows the algorithm to be run without using MATLAB licensed software and allows for interoperability
with AntennaCAT software written by Lauren Linkous at VCU. Much of the code is a direct translation and 
as such is GPL 3.0 like MultiGLODS before it. Please include the license with any derivative work, and 
please be sure to credit the original creators. 

Due to the translation the majority of code is written in the procedural style characteristic of most
MATLAB code; however, it has been wrapped in a class in multi_glods.py with two example use cases in `main_test.py` 
and `main_test_graph.py`


Several changes have been made to the original direct translation:
* ctl['objective_iter'] was added in multiglods_ctl.py as a way to count how many times the objective function has been called. 
* This ctr['objective_iter'] variable is then used in multiglods_ctl.py in run_update() to check if the objective function calls
have exceded a maximum iterations. 
* Also, the objective function call returns the F value and a boolean for if the objective function was executed without error

## Requirements

This project requires numpy, pandas, and matplotlib for the full demos. To run the optimizer without visualization, only numpy and pandas are requirements

Use 'pip install -r requirements.txt' to install the following dependencies:

```python
contourpy==1.2.1
cycler==0.12.1
fonttools==4.51.0
importlib_resources==6.4.0
kiwisolver==1.4.5
matplotlib==3.8.4
numpy==1.26.4
packaging==24.0
pandas==2.2.3
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2025.1
six==1.16.0
tzdata==2025.1
zipp==3.18.1

```

Optionally, requirements can be installed manually with:

```python
pip install  matplotlib, numpy, pandas

```
This is an example for if you've had a difficult time with the requirements.txt file. Sometimes libraries are packaged together.


## Implementation

### Initialization 

```python
    # Constant variables
    TOL = 10 ** -6      # Convergence Tolerance (This is a radius 
                            # based tolerance, not target based tolerance)
    MAXIT = 10000       # Maximum allowed iterations  

    # Objective function dependent variables
    LB = func_configs.LB              # Lower boundaries, [[0.21, 0, 0.1]]
    UB = func_configs.UB              # Upper boundaries, [[1, 1, 0.5]]
    IN_VARS = func_configs.IN_VARS    # Number of input variables (x-values)   
    OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
    TARGETS = func_configs.TARGETS    # Target values for output

    # Objective function dependent variables
    func_F = func_configs.OBJECTIVE_FUNC  # objective function
    constr_F = func_configs.CONSTR_FUNC   # constraint function


    # optimizer specific vars
    BP = 0.5            # Beta Par
    GP = 1              # Gamma Par
    SF = 2              # Search Frequency


    # optimizer setting values
    parent = None                 # Optional parent class for optimizer
                                    # (Used for passing debug messages or
                                    # other information that will appear 
                                    # in GUI panels)

    best_eval = 1

    suppress_output = True   # Suppress the console output of multiglods



    allow_update = True      # Allow objective call to update state 
                            # (Can be set on each iteration to allow 
                            # for when control flow can be returned 
                            # to multiglods)   



    # instantiation of multiglods optimizer 
    # Constant variables
    opt_params = {'BP': [BP],               # Beta Par
                'GP': [GP],                 # Gamma Par
                'SF': [SF] }                # Search Frequency

    opt_df = pd.DataFrame(opt_params)
    myGlods = multi_glods(LB, UB, TARGETS, TOL, MAXIT,
                            func_F, constr_F,
                            opt_df,
                            parent=parent)   


    # arguments should take the form: 
    # multi_glods([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj,
    # bool, class obj) 
    #  
    # opt_df contains class-specific tuning parameters
    # BP: float
    # GP: int
    # SF: int
    #

```

### State Machine-based Structure

This optimizer uses a state machine structure to control the movement of the particles, call to the objective function, and the evaluation of current positions. The state machine implementation preserves the initial algorithm while making it possible to integrate other programs, classes, or functions as the objective function.

A controller with a `while loop` to check the completion status of the optimizer drives the process. Completion status is determined by at least 1) a set MAX number of iterations, and 2) the convergence to a given target using the L2 norm.  Iterations are counted by calls to the objective function. 

Within this `while loop` are three function calls to control the optimizer class:
* **complete**: the `complete function` checks the status of the optimizer and if it has met the convergence or stop conditions.
* **step**: the `step function` takes a boolean variable (suppress_output) as an input to control detailed printout on current particle (or agent) status. This function moves the optimizer one step forward.  
* **call_objective**: the `call_objective function` takes a boolean variable (allow_update) to control if the objective function is able to be called. In most implementations, this value will always be true. However, there may be cases where the controller or a program running the state machine needs to assert control over this function without stopping the loop.

Additionally, **get_convergence_data** can be used to preview the current status of the optimizer, including the current best evaluation and the iterations.

The code below is an example of this process:

```python
    while not myOptimizer.complete():
        # step through optimizer processing
        # this will update particle or agent locations
        myOptimizer.step(suppress_output)
        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        myOptimizer.call_objective(allow_update)
        # check the current progress of the optimizer
        # iter: the number of objective function calls
        # eval: current 'best' evaluation of the optimizer
        iter, eval = myOptimizer.get_convergence_data()
        if (eval < best_eval) and (eval != 0):
            best_eval = eval
        
        # optional. if the optimizer is not printing out detailed 
        # reports, preview by checking the iteration and best evaluation

        if suppress_output:
            if iter%100 ==0: #print out every 100th iteration update
                print("Iteration")
                print(iter)
                print("Best Eval")
                print(best_eval)
```


### Constraint Handling
Users must create their own constraint function for their problems, if there are constraints beyond the problem bounds.  This is then passed into the constructor. If the default constraint function is used, it always returns true (which means there are no constraints).

### Boundary Types
This version of MultiGLODS uses random bounds to enforces boundaries on the problem space. Particles that leave the bounds will respawn in a random location.

Potentially other boundary types may be implemented, but experimentation is needed. 

### Objective Function Handling
The optimizer minimizes the absolute value of the difference of the target outputs and the evaluated outputs. Future versions may include options for function minimization when target values are absent. 

#### Creating a Custom Objective Function

Custom objective functions can be used by creating a directory with the following files:
* configs_F.py
* constr_F.py
* func_F.py

`configs_F.py` contains lower bounds, upper bounds, the number of input variables, the number of output variables, the target values, and a global minimum if known. This file is used primarily for unit testing and evaluation of accuracy. If these values are not known, or are dynamic, then they can be included experimentally in the controller that runs the optimizer's state machine. 

`constr_F.py` contains a function called `constr_F` that takes in an array, `X`, of particle positions to determine if the particle or agent is in a valid or invalid location. 

`func_F.py` contains the objective function, `func_F`, which takes two inputs. The first input, `X`, is the array of particle or agent positions. The second input, `NO_OF_OUTS`, is the integer number of output variables, which is used to set the array size. In included objective functions, the default value is hardcoded to work with the specific objective function.

Below are examples of the format for these files.

`configs_F.py`:
```python
OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "one_dim_x_test.func_F" #format: FUNCTION NAME.FUNCTION
CONSTR_FUNC_NAME = "one_dim_x_test.constr_F" #format: FUNCTION NAME.FUNCTION

# problem dependent variables
LB = [[0]]             # Lower boundaries
UB = [[1]]             # Upper boundaries
IN_VARS = 1            # Number of input variables (x-values)
OUT_VARS = 1           # Number of output variables (y-values) 
TARGETS = [0]          # Target values for output
GLOBAL_MIN = []        # Global minima sample, if they exist. 

```

`constr_F.py`, with no constraints:
```python
def constr_F(x):
    F = True
    return F
```

`constr_F.py`, with constraints:
```python
def constr_F(X):
    F = True
    # objective function/problem constraints
    if (X[2] > X[0]/2) or (X[2] < 0.1):
        F = False
    return F
```

`func_F.py`:
```python
import numpy as np
import time

def func_F(X, NO_OF_OUTS=1):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        x = X[0]
        F = np.sin(5 * x**3) + np.cos(5 * x) * (1 - np.tanh(x ** 2))
    except Exception as e:
        print(e)
        noErrors = False

    return [F], noErrors
```


#### Internal Objective Function Example

There are three functions included in the repository:
1) Himmelblau's function, which takes 2 inputs and has 1 output
2) A multi-objective function with 3 inputs and 2 outputs (see lundquist_3_var)
3) A single-objective function with 1 input and 1 output (see one_dim_x_test)

Each function has four files in a directory:
   1) configs_F.py - contains imports for the objective function and constraints, CONSTANT assignments for functions and labeling, boundary ranges, the number of input variables, the number of output values, and the target values for the output
   2) constr_F.py - contains a function with the problem constraints, both for the function and for error handling in the case of under/overflow. 
   3) func_F.py - contains a function with the objective function.
   4) graph.py - contains a script to graph the function for visualization.

Other multi-objective functions can be applied to this project by following the same format (and several have been collected into a compatible library, and will be released in a separate repo)

<p align="center">
        <img src="media/himmelblau_plots.png" alt="Himmelblau’s function" height="250">
</p>
   <p align="center">Plotted Himmelblau’s Function with 3D Plot on the Left, and a 2D Contour on the Right</p>

```math
f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2
```

| Global Minima | Boundary | Constraints |
|----------|----------|----------|
| f(3, 2) = 0                 | $-5 \leq x,y \leq 5$  |   | 
| f(-2.805118, 3.121212) = 0  | $-5 \leq x,y \leq 5$  |   | 
| f(-3.779310, -3.283186) = 0 | $-5 \leq x,y \leq 5$  |   | 
| f(3.584428, -1.848126) = 0  | $-5 \leq x,y \leq 5$   |   | 

<p align="center">
        <img src="media/obj_func_pareto.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Multi-Objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
\text{minimize}: 
\begin{cases}
f_{1}(\mathbf{x}) = (x_1-0.5)^2 + (x_2-0.1)^2 \\
f_{2}(\mathbf{x}) = (x_3-0.2)^4
\end{cases}
```

| Num. Input Variables| Boundary | Constraints |
|----------|----------|----------|
| 3      | $0.21\leq x_1\leq 1$ <br> $0\leq x_2\leq 1$ <br> $0.1 \leq x_3\leq 0.5$  | $x_3\gt \frac{x_1}{2}$ or $x_3\lt 0.1$| 

<p align="center">
        <img src="media/1D_test_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Single Input, Single-objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
f(\mathbf{x}) = sin(5 * x^3) + cos(5 * x) * (1 - tanh(x^2))
```
| Num. Input Variables| Boundary | Constraints |
|----------|----------|----------|
| 1      | $0\leq x\leq 1$  | $0\leq x\leq 1$| |

Local minima at $(0.444453, -0.0630916)$

Global minima at $(0.974857, -0.954872)$


## Example Implementations

### Basic Example
`main_test.py` provides a sample use case of the optimizer with tunable parameters.

### Realtime Graph

<p align="center">
        <img src="/media/himmelblau_search.gif" alt="gif of optimization model development through iterations" height="325">
</p>
<p align="center"> MultiGLODS Optimization on Himmelblau's Function. Left, the Search Location. Right, the Current Global Best Fitness Compared to Target</p>

<br>
<br>
<p align="center">
        <img src="/media/1D_test_search.gif" alt="gif of optimization development through iterations" height="325">
</p>
<p align="center">MultiGLODS Optimization on a Single Objective Function with 1 Inputs and 1 Output. Left, the Search Location. Right, the Current Global Best Fitness Compared to Target</p>

<br>
<br>

<p align="center">
        <img src="/media/multi_obj_search.gif" alt="gif of optimization model development through iterations" height="325">
</p>
<p align="center">MultiGLODS Optimization on a Multi Objective Function with 3 Inputs and 2 Outputs. Left, the Search Location. Right, the Current Global Best Fitness Compared to Target</p>

<br>
<br>

`main_test_graph.py` provides an example using a parent class, and the self.suppress_output flag to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step.

The figure above shows samples of the MultiGLODS optimizer searching each of the three included example objective functions. In all figures in this section, the left plot shows the current search location(s), and the right shows the history of the global best fitness values (the black circles) in relation to the target (the red star). The three graphs present a similar process for different dimensions of objective functions.

NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.


## References

[1] A. L. Custódio and J. F. A. Madeira, “MultiGLODS: global and local multiobjective optimization using direct search,” Journal of Global Optimization, vol. 72, no. 2, pp. 323–345, Feb. 2018, doi: https://doi.org/10.1007/s10898-018-0618-1.

[2] A. L. Custódio and J. F. A. Madeira, “GLODS: Global and Local Optimization using Direct Search,” Journal of Global Optimization, vol. 62, no. 1, pp. 1–28, Aug. 2014, doi: https://doi.org/10.1007/s10898-014-0224-9.


## Related Publications and Repositories
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT. Publications featuring the code as part of AntennaCAT will be added as they become public.

When citing the algorithm itself, please refer to the original publication for MultiGLODS by the original authors:

 A. L. Custódio and J. F. A. Madeira, MultiGLODS: Global and Local Multiobjective 
Optimization using Direct Search, Journal of Global Optimization, 72 (2018), 323 - 345 PDF


## Licensing

Unlike other optimizers in the AntennaCAT suite, which were released under GPL-2.0, this work is licensed under GPL-3.0 per the license used by the original authors of the MultiGLODS algorithm. 




# bayesian_optimization_python
Repository for demoing the effect of various surrogate models on Bayesian Optimization accuracy. 

The class format is based off of the [adaptive timestep PSO optimizer](https://github.com/jonathan46000/pso_python) by [jonathan46000](https://github.com/jonathan46000) for data collection baseline. This repo does not feature any PSO optimization. Instead, the format has been used to retain modularity with other optimizers.

The surrogate models are designed to interface with the optimizers in the AntennaCAT suite, but have not been exhaustively tested as of June. 2024 while they are in parallel development. See [References](#references) for the running list of references as optimizers and surrogate models are added/edited, and features are updated.

Now featuring AntennaCAT hooks for GUI integration and user input handling.

## Table of Contents
* [Bayesian Search](#bayesian-search)
* [Surrogate Models](#surrogate-models)
    * [Radial Basis Function Network](#radial-basis-function-network)
    * [Gaussian Process](#gaussian-process)
    * [Kriging](#kriging)
    * [Polynomial Regression](#polynomial-regression)
    * [Polynomial Chaos Expansion](#polynomial-chaos-expansion)
    * [K-Nearest Neighbors Regression](#k-nearest-neighbors-regression)
    * [Decision Tree Regression](#decision-tree-regression)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Constraint Handling](#constraint-handling)
    * [Multi-Objective Optimization](#multi-objective-optimization)
    * [Objective Function Handling](#objective-function-handling)
      * [Internal Objective Function Examples](#internal-objective-function-examples)
* [Example Implementations](#example-implementations)
    * [Basic Example](#basic-example)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Publications and Integration](#publications-and-integration)
* [Licensing](#licensing)  

## Bayesian Search

Bayesian search, or Bayesian optimization, uses probabilistic models to efficiently optimize functions that are computationally expensive or resource intensive to evaluate. It iteratively updates a Bayesian model of the objective function based on sampled evaluations (of the objective function). 

## Surrogate Models
A surrogate model in optimization serves as a proxy for the actual objective function, which may be costly or impractical to evaluate directly. It approximates the behavior of the objective function using a simpler, computationally efficient model, such as the Gaussian Process (GP) model included in this repository. This surrogate model is iteratively updated based on evaluations of the actual objective function, improving its accuracy over time. It allows optimization algorithms to make informed decisions about where to explore next in the search space, balancing between exploiting known good regions and exploring potentially better ones. Surrogate models are fundamental in speeding up optimization processes by reducing the number of expensive evaluations needed to find optimal solutions.

For comparison and experimental purproses, there is a small library of surrogate models included in this repository that can be used with the included Bayesian optimizer. They are:


### Radial Basis Function Network
A Radial Basis Function Network (RBFN) is a type of artificial neural network that uses radial basis functions as activation functions. It consists of three layers: an input layer, a hidden layer with a non-linear RBF activation function (typically Gaussian), and a linear output layer. The simple approach in this repo uses numpy and basic matrix math rather than a ML specific library. RBFNs are commonly used for function approximation, time-series prediction, and classification tasks. They are valued for their simplicity, ease of training, and ability to model complex, non-linear relationships with a smaller number of neurons compared to other neural network architectures (which means a smaller matrix).


### Gaussian Process

A Gaussian process (GP) is a probabilistic model used primarily in machine learning and optimization. It defines a distribution over functions, where each point in the function's domain is assigned a Gaussian distribution. GPs are characterized by their mean function (typically assumed to be zero) and covariance function (kernel), which determines the relationships between different points. GPs are flexible and powerful tools for regression and uncertainty quantification, allowing predictions not only of the function values but also of the uncertainty associated with those predictions. 


### Kriging

Kriging, like Gaussian processes, is a technique used for interpolation and approximation of data points. Kriging models the spatial correlation between data points to predict values at unsampled locations. It uses a linear combination of data points with weights determined by spatial covariance functions (kriging models) to estimate values and quantify prediction uncertainty. Kriging is advantageous in fields like spatial statistics, where it provides accurate predictions and uncertainty estimates based on known data points' spatial relationships. 

Kriging is a specialized form of Gaussian process regression tailored for spatial datasets, emphasizing the spatial autocorrelation structure to improve prediction accuracy in geospatial applications and beyond.


### Polynomial Regression

Polynomial regression is a form of regression analysis where the relationship between the independent variable x and the dependent variable y is modeled as an n-th degree polynomial function. Unlike linear regression, which assumes a linear relationship, polynomial regression can capture non-linear relationships between variables. 



### Polynomial Chaos Expansion

Polynomial Chaos Expansion (PCE) is a method used in uncertainty quantification and sensitivity analysis. It expresses a stochastic model's output as a series expansion in terms of orthogonal polynomials, typically Hermite, Legendre, or other families depending on the underlying probability distribution. Each polynomial corresponds to a different order of the stochastic variables, capturing the variability and uncertainty in the model's parameters or inputs. PCE provides a way to efficiently compute statistical moments, such as mean and variance, and quantify how uncertainties in input parameters propagate through the model to affect output variability


### K-Nearest Neighbors Regression

As part of a Bayesian optimizer, the K-Nearest Neighbors (KNN) model predicts the objective function's value at a new point based on the values of its k nearest neighbors in the training data. By using the distances and weights of these neighbors, it estimates the function value, guiding the optimizer to explore promising regions of the search space. KNN is valued for its simplicity and non-parametric nature, making it flexible for various optimization problems. However, it may struggle with high-dimensional data. It does not do well on the Himmelblau function as the parameters are currently set.

### Decision Tree Regression

Decision Tree Regression is a predictive modeling technique used for continuous target variables. It works by recursively splitting the data into subsets based on the feature that minimizes the mean squared error (MSE) at each split. Each internal node represents a feature, and each leaf node represents a predicted value, usually the mean of the target values in that region. This method captures non-linear relationships and is easy to interpret. However, it can overfit the training data, so techniques like pruning or using ensemble methods (e.g., Random Forests) are often employed to enhance its performance and generalization ability.



## Requirements

This project requires numpy and matplotlib. 

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
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
six==1.16.0
zipp==3.18.1

```

## Implementation
### Constraint Handling
In this example, proposed points are generated within the provided bounds of the problem, so there is no extra constraint handling added. 


### Multi-Objective Optimization
The no preference method of multi-objective optimization, but a Pareto Front is not calculated. Instead, the best choice (smallest norm of output vectors) is listed as the output.

### Objective Function Handling
The optimizer minimizes the absolute value of the difference from the target outputs and the evaluated outputs. Future versions may include options for function minimization absent target values. 


#### Internal Objective Function Examples

There are three functions included in the repository:
1) Himmelblau's function, which takes 2 inputs and has 1 output
2) A multi-objective function with 3 inputs and 2 outputs (see lundquist_3_var)
3) A single-objective function with 1 input and 1 output (see one_dim_x_test)

Each function has four files in a directory:
   1) configs_F.py - contains imports for the objective function and constraints, CONSTANT assignments for functions and labeling, boundary ranges, the number of input variables, the number of output values, and the target values for the output
   2) constr_F.py - contains a function with the problem constraints, both for the function and for error handling in the case of under/overflow. 
   3) func_F.py - contains a function with the objective function.
   4) graph.py - contains a script to graph the function for visualization.



<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/himmelblau_plots.png" alt="Himmelblau function" height="250">
</p>
   <p align="center">Plotted Himmelblau Function with 3D Plot on the Left, and a 2D Contour on the Right</p>

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
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/lundquist_3var_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
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
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/1D_test_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
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
main_test.py provides a sample use case of the optimizer with tunable parameters.

### Realtime Graph

<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_progress.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Himmelblau. Left to Right: Objective function ground truth, areas of interest to the optimizer, and surrogate model development process.</p>

<br>
<br>
<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_1X.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Single Input, Single Objective Function. Left, Gaussian Process Regression Model. Right: Aquisition Function.</p>

<br>
<br>

<p align="center">
        <img src="https://github.com/LC-Linkous/bayesian_optimization_python/blob/main/media/surrogate_model_multi_obj.gif" alt="gif of surrogate model development through iterations" height="325">
</p>
<p align="center">Bayesian Optimization with a Gaussian Proccess Using Multi-Objective Function. Left, Objective Function Output and Sampling. Right, Surrogate Model GP Mean Fitting and Sample Points.</p>

<br>
<br>

main_test_graph.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step.

The figure above shows a low-resolution version of the optimization for example. In this first figure, the Far left plot is the objective ground truth function with sample locations in red. The center plot is the expected improvement, which highlights areas of interest to the optimizer. The far right plot is the current shape of the surrogate model, with sampled points from the ground truth in red. The other two graphs present a similar process for different dimensions of objective functions.


NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.

## References

[1] Wikipedia Contributors, “Himmelblau’s function,” Wikipedia, Dec. 29, 2023. https://en.wikipedia.org/wiki/Himmelblau%27s_function 

[2] Wikipedia Contributors, “Bayesian optimization,” Wikipedia, Jul. 05, 2019. https://en.wikipedia.org/wiki/Bayesian_optimization

[3] W. Wang, “Bayesian Optimization Concept Explained in Layman Terms,” Medium, Mar. 22, 2022. https://towardsdatascience.com/bayesian-optimization-concept-explained-in-layman-terms-1d2bcdeaf12f

[4] C. Brecque, “The intuitions behind Bayesian Optimization with Gaussian Processes,” Medium, Apr. 02, 2021. https://towardsdatascience.com/the-intuitions-behind-bayesian-optimization-with-gaussian-processes-7e00fcc898a0

[5] “Introduction to Bayesian Optimization (BO) — limbo 0.1 documentation,” resibots.eu. https://resibots.eu/limbo/guides/bo.html 

[6] “Radial Basis Function Networks (RBFNs) with Python 3: A Comprehensive Guide – Innovate Yourself,” Nov. 03, 2023. https://innovationyourself.com/radial-basis-function-networks-rbfn/ 

[7] Everton Gomede, PhD, “Radial Basis Functions Neural Networks: Unlocking the Power of Nonlinearity,” Medium, Jun. 06, 2023. https://medium.com/@evertongomede/radial-basis-functions-neural-networks-unlocking-the-power-of-nonlinearity-c67f6240a5bb

[8] J. Luo, W. Xu and J. Chen, "A Novel Radial Basis Function (RBF) Network for Bayesian Optimization," 2021 IEEE 7th International Conference on Cloud Computing and Intelligent Systems (CCIS), Xi'an, China, 2021, pp. 250-254, doi: 10.1109/CCIS53392.2021.9754629.

[9] Wikipedia Contributors, “Kriging,” Wikipedia, Oct. 16, 2018. https://en.wikipedia.org/wiki/Kriging


[10] “Polynomial kernel,” Wikipedia, Oct. 02, 2019. https://en.wikipedia.org/wiki/Polynomial_kernel

[11] A. Radhakrishnan, M. Luyten, G. Stefanakis, and C. Cai, “Lecture 3: Kernel Regression,” 2022. Available: https://web.mit.edu/modernml/course/lectures/MLClassLecture3.pdf

[12] “Polynomial chaos,” Wikipedia, Mar. 19, 2024. https://en.wikipedia.org/wiki/Polynomial_chaos 

[13] “Polynomial Chaos Expansion — Uncertainty Quantification,” dictionary.helmholtz-uq.de. https://dictionary.helmholtz-uq.de/content/PCE.html (accessed Jun. 28, 2024).

[14] T. Srivastava, “Introduction to KNN, K-Nearest Neighbors : Simplified,” Analytics Vidhya, Mar. 07, 2019. https://www.analyticsvidhya.com/blog/2018/03/introduction-k-neighbours-algorithm-clustering/

[15] Wikipedia Contributors, “k-nearest neighbors algorithm,” Wikipedia, Mar. 19, 2019. https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
 
[16] “Python | Decision Tree Regression using sklearn,” GeeksforGeeks, Oct. 04, 2018. https://www.geeksforgeeks.org/python-decision-tree-regression-using-sklearn/

[17] “Decision Tree Regression,” Saedsayad.com, 2019. https://www.saedsayad.com/decision_tree_reg.htm

[18] Wikipedia Contributors, “Decision tree learning,” Wikipedia, Jun. 12, 2019. https://en.wikipedia.org/wiki/Decision_tree_learning



## Publications and Integration
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT.

Publications featuring the code in this repo will be added as they become public.


## Licensing

The code in this repository has been released under GPL-2.0



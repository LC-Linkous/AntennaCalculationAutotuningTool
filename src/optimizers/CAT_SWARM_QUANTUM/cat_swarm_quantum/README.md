# cat_swarm_quantum

A 'quantum' cat swarm optimizer written in Python using quantum inspired methods (non-qiskit). Modified from the [adaptive timestep PSO optimizer](https://github.com/jonathan46000/pso_python) by [jonathan46000](https://github.com/jonathan46000) to keep a consistent format between optimizers in AntennaCAT.


Now featuring AntennaCAT hooks for GUI integration and user input handling.

This branch of the repository is part of a series of replication studies. It is not intended to be the 'best' implementation, or the most recent advancement of the algorithm. This method has been chosen to replicate a specific snapshot of literature.


## Table of Contents
* [Cat Swarm Optimization](#cat-swarm-optimization)
* [Quantum Inspired Optimization](#quantum-inspired-optimization)
* [Quantum Cat Swarm Optimization](#quantum-cat-swarm-optimization)
    * [Quantum Seeking Mode](#quantum-seeking-mode)
       * [Mean Best Position](#mean-best-position)
       * [Position Update](#position-update)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Constraint Handling](#constraint-handling)
    * [Boundary Types](#boundary-types)
    * [Multi-Object Optimization](#multi-object-optimization)
    * [Objective Function Handling](#objective-function-handling)
      * [Internal Objective Function Example](internal-objective-function-example)
* [Examples](#example-implementations)
    * [Basic Swarm Example](#basic-swarm-example)
    * [Detailed Messages](#detailed-messages)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Publications and Integration](#publications-and-integration)
* [Licensing](#licensing)  

## Cat Swarm Optimization

Cat Swarm Optimization (CSO) is a nature-inspired optimization algorithm based on the behaviors of cats. It was introduced in "Cat Swarm Optimization" [1] in 2006. This algorithm resembles the traditional Particle Swarm Optimization (PSO) algorithm as it has location and velocity aspects, but the agents/particles in this algorithm have two options for movement in the update step. These two options are modeled off of two primary behaviors of cats: seeking and tracing. These modes represent the exploration and exploitation phases in optimization, respectively.

CSO divides the population of candidate solutions (cats) into two groups: one group for the seeking mode and another for the tracing mode. Each cat can switch between these modes according to a specified probability. 

1) Seeking Mode:

The seeking mode is responsible for exploring the search space to discover new and potentially better solutions. In this mode, cats simulate a behavior where they observe their surroundings and make decisions to move to new positions based on several possible moves. This helps the algorithm avoid getting stuck in local optima.

2) Tracing Mode:

The tracing mode is responsible for exploiting the search space by following the best solutions found so far. In this mode, cats simulate a behavior where they move towards a promising position, akin to a cat chasing prey. This helps refine solutions and converge towards the global optimum.


## Quantum Inspired Optimization

Quantum(-inspired) Particle Swarm Optimization (QPSO) was introduced in 2004 [2] [3]. Paraphrased from [2], in PSO the location and velocity vectors are used to determine the trajectory of the particle, which because in Newtonian mechanics a particle moves along a determined trajectory. However, in quantum mechanics, the location and velocity vectors cannot be determined/known simultaneously due to uncertainty principle (Werner Heisenberg, 1927). The takeaway being, quantum-inspired algorithms take concepts from quantum mechanics, such as superposition and entanglement, and apply them in classical computation to solve optimization problems more effectively (depending on the problem type). 

These two concepts are applied, generally speaking, as follows:


1) Superposition

**Quantum Concept**: In quantum mechanics, a particle canexist in a superposition of multiple states simultaneously. For example, a quantum bit (qubit) can be in a state ∣0⟩∣0⟩, ∣1⟩∣1⟩, or any linear combination ∣ψ⟩=α∣0⟩+β∣1⟩∣ψ⟩=α∣0⟩+β∣1⟩, where α and β are complex numbers.

**Classical Adaptation**: In quantum-inspired algorithms, superposition can be interpreted as a probability distribution over multiple states. Instead of particles having a single position, they are represented by a probability distribution, reflecting the potential to be in various positions simultaneously.

**Example in QPSO**: In the Quantum-inspired Particle Swarm Optimization (QPSO), a particle’s position is often updated using a probability distribution derived from both personal best and global best positions, rather than a deterministic position update. This allows particles to explore the search space more effectively.


2) Entanglement

**Quantum Concept**: Entanglement is a phenomenon where particles become interconnected such that the state of one particle directly affects the state of another, no matter the distance between them. This creates a strong correlation between the particles.

**Classical Adaptation**: In quantum-inspired algorithms, entanglement can be represented as a dependency or correlation between particles. When one particle updates its position, it influences the position updates of other particles, promoting cooperative behavior among the particles in the swarm.

**Example in QPSO**: In QPSO, the positions of particles might be updated using a combination of their personal best position and the global best position, creating a form of "entanglement" where particles are influenced by the best solutions found by the swarm, thus maintaining a level of coordination and cooperation.



## Quantum Cat Swarm Optimization

Unlike traditional PSO, quantum-inspired swarm optimization algorithms don't use paired position and velocity vectors. Instead, they generally update particle positions directly based on a probability distribution based on the mean best position and a logarithmic factor, which has roots in the quantum mechanics principles mentioned previously. The QPSO update rule leverages quantum-inspired probabilistic movements to balance exploration and exploitation. By combining the best aspects of personal and global experiences and adding a stochastic component, QPSO can effectively search complex optimization landscapes. 


### Quantum Seeking Mode

*  Generates several copies of the cat's position using a quantum-inspired update rule, which involves:
  * Calculating a mean best position, $mb$, as a combination of the global best position, $g$, and the current cat's position, $p$.
  * Introducing a probabilistic factor, $u$, to generate new positions.
  * Evaluates the fitness of these new positions and selects the best one.

#### Mean Best Position
 
Mean Best Position ($mb$) is a weighted average of the personal best position ($p$) and the global best position ($g$). It is calculated as:

```math
mb=\beta \cdot p+(1−\beta) \cdot g

```

Where:

* $\beta$ is a parameter controlling the influence between the personal and global best positions.

#### Position Update

 In QPSO, instead of updating the velocity and then the position, we directly update the position using quantum mechanics-inspired rules. The update rule is:

```math
x_i(t+1) = mb \pm \beta \cdot \lvert p - g \rvert \cdot \log(1/u)
```

Where:

* $mb$ is the mean best position
* $\beta$ is a user-defined parameter influencing convergence behavior.
* $p$ is the personal best position of the particle.
* $g$ is the global best position of the swarm.
* $u$ is a uniformly distributed random number in the range (0, 1).
* The logarithmic term $log(1/u)$ comes from the distribution properties of quantum systems.
* $\beta \cdot \lvert p−g \rvert $ scales the exploration step based on the distance between the personal and global best positions.
* $log(1/u)$ introduces a random factor with a bias towards smaller values (since $u$ is between 0 and 1, $log(1/u)$ is negative, making $−log⁡(1/u)$ positive).


The QPSO update rule is based on the quantum mechanics principle where particles have a probability distribution of being in different positions. The position update rule can be seen as a way to explore the search space more effectively through 2 key factors:

**Diverse Exploration**: The term $log⁡(1/u_2)$ helps in creating a wide range of possible moves, allowing the particles to explore the search space extensively. The logarithmic function is chosen because it provides a heavy-tailed distribution, meaning particles can make both small and large jumps, avoiding local minima and encouraging global exploration.

**Balanced Exploitation**: The combination of $mb$, $p$, and $g$ ensures that the particles are guided towards promising regions of the search space, leveraging both individual experience (personal_best) and collective knowledge (global_best).



### Quantum Tracing Mode

Update the cat’s position towards the global best position using the quantum-inspired probabilistic update rule, in this case the random vector $u$.



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
Users must create their own constraint function for their problems, if there are constraints beyond the problem bounds.  This is then passed into the constructor. If the default constraint function is used, it always returns true (which means there are no constraints).

### Boundary Types
This optimizer has 4 different types of bounds, Random (Particles that leave the area respawn), Reflection (Particles that hit the bounds reflect), Absorb (Particles that hit the bounds lose velocity in that direction), Invisible (Out of bound particles are no longer evaluated).

Some updates have not incorporated appropriate handling for all boundary conditions. This bug is known and is being worked on. The most consistent boundary type at the moment is Random.  If constraints are violated, but bounds are not, currently random bound rules are used to deal with this problem. 

### Multi-Object Optimization
The no preference method of multi-objective optimization, but a Pareto Front is not calculated. Instead, the best choice (smallest norm of output vectors) is listed as the output.

### Objective Function Handling
The optimizer minimizes the absolute value of the difference from the target outputs and the evaluated outputs. Future versions may include options for function minimization absent target values. 

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
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/cat_swarm_quantum/media/himmelblau_plots.png" alt="Himmelblau function" height="250">
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
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/cat_swarm_quantum/media/obj_func_pareto.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
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
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/cat_swarm_quantum/media/1D_test_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
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

### Basic Swarm Example
main_test.py provides a sample use case of the optimizer. 

### Detailed Messages
main_test_details.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. This implementation sets up the hooks for integration with AntennaCAT to provide the user feedback of warnings and errors.

### Realtime Graph

<p align="center">
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/cat_swarm_quantum/media/qcat_swarm.gif" alt="Example Quantum Cat Swarm Optimization" height="200">
</p>

main_test_graph.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step. 

NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.

## References

[1] S.-C. Chu, P. Tsai, and J.-S. Pan, “Cat Swarm Optimization,” Lecture Notes in Computer Science, pp. 854–858, 2006, doi: https://doi.org/10.1007/978-3-540-36668-3_94.


[2] Jun Sun, Bin Feng and Wenbo Xu, "Particle swarm optimization with particles having quantum behavior," Proceedings of the 2004 Congress on Evolutionary Computation (IEEE Cat. No.04TH8753), Portland, OR, USA, 2004, pp. 325-331 Vol.1, doi: 10.1109/CEC.2004.1330875.

[3] Jun Sun, Wenbo Xu and Bin Feng, "A global search strategy of quantum-behaved particle swarm optimization," IEEE Conference on Cybernetics and Intelligent Systems, 2004., Singapore, 2004, pp. 111-116 vol.1, doi: 10.1109/ICCIS.2004.1460396.

[4] X. Nie, W. Wang, and H. Nie, “Chaos Quantum-Behaved Cat Swarm Optimization Algorithm and Its Application in the PV MPPT,” Computational Intelligence and Neuroscience, vol. 2017, pp. 1–11, Jan. 2017, doi: https://doi.org/10.1155/2017/1583847.

[5] A. M. Ahmed, T. A. Rashid, and S. Ab. M. Saeed, “Cat Swarm Optimization Algorithm: A Survey and Performance Evaluation,” Computational Intelligence and Neuroscience, vol. 2020, pp. 1–20, Jan. 2020, doi: https://doi.org/10.1155/2020/4854895.

## Publications and Integration
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT.

Publications featuring the code in this repo will be added as they become public.

## Licensing

The code in this repository has been released under GPL-2.0



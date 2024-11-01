# AntennaCAT


<p align="center">
 <img src="https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/blob/main/media/antennaCAT-icons/transparent-antennaCAT-logo.png" height="400" >
</p>


Antenna Calculation and Autotuning (AntennaCAT) is a comprehensive implementation of machine learning to automate, evaluate, and optimize the antenna design process using EM simulation software. It utilizes a combined antenna designer and internal calculator to accelerate the CAD condsturction and EM simulation of several common topologies, while eliminating model disparity for automated data collection.

## Wiki and Documentation

See the [Release Schedule](#release-schedule) below for code roll out updates.

As we prepare for the first code release, we're sharing information on the Wiki of how to download, setup and use AntennaCAT.

You can [Start Here](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki) for general project information.

Pages are being updated daily, so check back in a few days if the information you're looking for hasn't been posted yet.



## Release Schedule 

Where are we so far? (Oct. 21, 2024)

* The dissertation based on the AntennaCAT software has been released at https://scholarscompass.vcu.edu/etd/7841/
* The Individual optimizers have been released for unit testing
* The objective function library has been posted
* The journal/magazine article for AntennaCAT is under review



What does that mean for the code release?
* The code will be released independent from the journal/magazine publication, still targeting before the end of 2024 (read: before mid-November).
* Post release 1, updates and code examples will be found at https://lc-linkous.github.io/projects/antennaCAT 
* Documentation of usage examples will be posted in the Wiki on this page. The full explanation of all of the details that did not fit in the dissertation will begin appearing, but this may take some time


Stages of major revision roll out:
* AntennaCAT v. 2024.1
  * All of the core antennaCAT features - a stable first release so collaborators can find bugs while I document the newer updates. This release includes the calculator, a couple of the replication studies, the load/detect script features, optimizers WITHOUT the hyperparameter suggestion network. This version will be fully integrated with Ansys HFSS, with the template framework for the other EM simulation software included. Why not all of them hooked up? Licensing issue being handled over the academic Winter break. 

* AntennaCAT v. 2025.1
  * (or maybe 2024.2, the difference is 3 free weekends to document code)
  * The rest of the replication study set. The hyperparameter suggestion network added in and documented.
  * Start phasing in the other EM simulation softwares.  

* AntennaCAT v. 2025.2
  * The first round of bending and custom layers added back in. This works differently for different EM simulation software, so the templates are more intricate for these steps
  * At this point, that's 99.9% of the functionality released open-source. Major revisions after this point will be due to feature additions not originally planned.
 

 


## Publications and Repositories

1. L. Linkous, “Machine Learning Assisted Optimization for Calculation and Automated Tuning of Antennas,” VCU Scholars Compass, 2024. https://scholarscompass.vcu.edu/etd/7841/ (accessed Oct. 21, 2024).

2. L. Linkous, J. Lundquist, M. Suche and E. Topsakal, "Machine Learning Assisted Hyperparameter Tuning for Optimization," 2024 IEEE INC-USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Florence, Italy, 2024, pp. 107-108, doi: 10.23919/INC-USNC-URSI61303.2024.10632482.

3. L. Linkous, E. Karincic, J. Lundquist, and E. Topsakal, “Automated Antenna Calculation, Design and Tuning Tool for HFSS,” 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), 2023.

4. L. Linkous, J. Lundquist, and E. Topsakal, “AntennaCAT: Automated Antenna Design and Tuning Tool,” 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), 2023. (Accepted)

5. L. Linkous, (LC-Linkous) (2022) AntennaCAT (Version 3.0) [source code] https://github.com/LC-Linkous/AntennaCalculationAutotuningTool 

6. L. Linkous, (LC-Linkous) (2022) GeneticCAT (Version 3.0) [source code] https://github.com/LC-Linkous/GeneticCAT  

7. E. Karincic, (Dollarhyde) (2022) Antenna Calculator (Version 2.0) [source code]. https://github.com/Dollarhyde/AntennaCalculator 


Individual Optimizer Repositories:

| Base Optimizer | Alternate Version | Quantum-Inspired Optimizer | Surrogate Model Version |
| ------------- | ------------- | ------------- |------------- |
| [pso_python](https://github.com/LC-Linkous/pso_python) | [pso_basic](https://github.com/LC-Linkous/pso_python/tree/pso_basic) | [pso_quantum](https://github.com/LC-Linkous/pso_python/tree/pso_quantum)  | |
| [cat_swarm_python](https://github.com/LC-Linkous/cat_swarm_python) | [sand_cat_python](https://github.com/LC-Linkous/cat_swarm_python/tree/sand_cat_python)| [cat_swarm_quantum](https://github.com/LC-Linkous/cat_swarm_python/tree/cat_swarm_quantum) | |
| [chicken_swarm_python](https://github.com/LC-Linkous/chicken_swarm_python) | - | [chicken_swarm_quantum](https://github.com/LC-Linkous/chicken_swarm_python/tree/chicken_swarm_quantum)  | |
| [sweep_python](https://github.com/LC-Linkous/sweep_python)  | *alternates in base repo | -  | - |
| [bayesian optimization_python](https://github.com/LC-Linkous/bayesian_optimization_python)  | -| - | *interchangable surrogate models <br> included in base repo |
| [multi_glods_python](https://github.com/LC-Linkous/multi_glods_python)| - | - | |


The [Objective Function Test Suite](https://github.com/LC-Linkous/objective_function_suite) is now public

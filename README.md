# AntennaCAT

<p align="center">
 <img src="./src/media/antennaCAT-icons/transparent-antennaCAT-logo.png" height="200" >
</p>

Antenna Calculation and Autotuning Tool (AntennaCAT) is a comprehensive implementation of machine learning to automate, evaluate, and optimize the antenna design process using EM simulation software. It utilizes a combined antenna designer and internal calculator to accelerate the CAD construction and EM simulation of several common topologies, while eliminating model disparity for automated data collection.

## Table of contents
* [Wiki and Documentation](#wiki-and-documentation)
* [Current Release](#current-release)
* [Release Schedule](#release-schedule)
* [Requirements](#requirements)
* [Organization](#organization)
* [Running](#running)
* [Related Publications and Repositories](#related-publications-and-repositories)

## Wiki and Documentation

See the [Release Schedule](#release-schedule) below for code roll out updates.

As we prepare for the first code release, we're sharing information on the Wiki of how to download, set up and use AntennaCAT.

You can [Start Here](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki) for general project information.

Pages are being updated daily, so check back in a few days if the information you're looking for hasn't been posted yet.

## Current Release

First 2025 code drop! AntennaCAT 2025.0 is live!

What's happening now?
* Minor restructuring to get the save&load functionality switched over from a txt file to JSON. This was a requested feature, so it's been bumped up in priority. It's also a good time to clean up the 'file load' functions.
* Graphics library update for better previews and live parameter editing
* Streamlining the optimizer class initializations for more modularity + the surrogate model integration

Why are we not matching the literature exactly? 
* The driving goal behind the development of this software is for it to be useful and to encourage experimentation. Holding back features/functionality to be truer to the publications goes against that. 

Why not release it all at once?
* The goal of several major releases close together is to have some roll-back points as collaborators join in and want to implement their own features. We won't wait to release what's already been implemented in recent publications, but there will be links to these 'check points' should anyone wish to download an earlier version.

## Release Schedule 

**Where are we so far?** (Feb. 2025)
* AntennaCAT 2025.0 is live!

We are in the quick release stage for several major features. See the [Past Releases section on the Documentation Wiki page](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki/Documentation#past-releases) for the list of all releases. 2025.0, 2025.1, and 2025.2 and their corresponding lit will be listed in the Wiki.


What does that mean for code releases?
* The code will always be released independently from the journal/magazine publication. While publications are awesome and we want to share what we're up to, sometimes we might move a little faster than planned. Or slower, because code takes time.

* Post release 1, updates and code examples will be found at https://lc-linkous.github.io/projects/antennaCAT AND the [wiki](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki/)
* Documentation of usage examples will be posted in the Wiki on this page. The full explanation of all of the details that did not fit in the dissertation will begin appearing, but this may take some time

Stages of early 2025 major revision roll out:

* AntennaCAT v. 2025.0
  * The 12 topology replication set.  
  * All optimizers integrated fully with the GUI. 
  * This is the 'core' functionality of AntennaCAT without the add-ons. 
  * It sets us up for plugging in all of the developments from Summer 2024 onwards (2 conferences + dissertation)


 

## Recent Previous Releases

2024.0:
* This version is close to the early 2023 lit. All core AntennaCAT features - a stable first release so collaborators can find bugs while I document the newer updates. This release includes the calculator, several replication studies, the load/detect script features, optimizers WITHOUT the hyperparameter suggestion network. This version will be fully integrated with Ansys HFSS, with the template framework for the other EM simulation software included. Why not all of them hooked up? Licensing issue being handled over the academic Winter break so we can test on non-code development systems. 
* The dissertation based on the AntennaCAT software has been released at https://scholarscompass.vcu.edu/etd/7841/
* The individual optimizers have been released for unit testing
* The objective function library has been posted
* The [Wiki](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki) is being updated daily 
* Core features:
  * the [AntennaCalculator](https://github.com/Dollarhyde/AntennaCalculator)
  * a couple of the replication studies (these are too useful to leave out)
  * material dictionary #1 with ~25 common materials
  * simulation setup
  * batch data collection
  * the optimizer set (without the ML additions and surrogate modeling)
  * load/detect script features
  * Ansys HFSS integration
  * ANCAT project creation, basic save functionality (a newer feature, but not worth removing)




## Requirements
Library requirements for locally run Python code are included in requirements.txt and can be 
installed using 'pip install -r requirements.txt'

AntennaCAT has been tested with Python 3.9 (primary development), and 3.12 (specifically 3.12.7) for the 2024.0 release. Versions of Python between 3.9 and 3.12 are probably fine, but have not been tested.

```python
cairocffi==0.9.0
cffi==1.17.1
contourpy==1.3.1
cycler==0.12.1
dxfgrabber==1.0.1
ezdxf==1.3.4
flexcache==0.3
flexparser==0.4
fonttools==4.55.0
kiwisolver==1.4.7
matplotlib==3.9.2
numpy==2.1.3
packaging==24.2
pandas==2.2.3
pcb-tools==0.1.6
pcb-tools-extension==0.9.3
pillow==11.0.0
Pint==0.24.4
platformdirs==4.3.6
pycparser==2.22
pyparsing==3.2.0
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
typing_extensions==4.12.2
tzdata==2024.2
wxPython==4.2.2
```

Optionally, requirements can be installed manually with:

pip install wxPython, matplotlib, pandas, numpy, ezdxf, Pint, pcb-tools, pcb-tools-extension 

## Organization

The simplified project structure is shown below.  Full file structure will be updated in the documentation for future collaboration efforts. 
```python
.
├── AntennaCalculationAndAutotuning
|
├── .src                                # directory for source code of AntennaCAT.
│   │
│   ├── ...                             # root of the project code.
│   │
│   └── main.py                         # main program file. The project entry point.
|
├── README.md                           # this README.
└── requirements.txt                    # project requirement minimum.
```

## Running

AntennaCAT and derivatives should be run from main.py, either in an IDE or with 'python main.py'. 

While there are unit testing artifacts in some code files, entry at other points in the program will cause some features to not work. 

It is recommended to run AntennaCAT in a virtual environment, but it is not a requirement. 



## Related Publications and Repositories

1. L. Linkous, “Machine Learning Assisted Optimization for Calculation and Automated Tuning of Antennas,” VCU Scholars Compass, 2024. https://scholarscompass.vcu.edu/etd/7841/ (accessed Oct. 21, 2024).

2. L. Linkous, J. Lundquist, M. Suche and E. Topsakal, "Machine Learning Assisted Hyperparameter Tuning for Optimization," 2024 IEEE INC-USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Florence, Italy, 2024, pp. 107-108, doi: 10.23919/INC-USNC-URSI61303.2024.10632482.

3. L. Linkous and E. Topsakal, "Machine Learning Assisted Optimization Methods for Automated Antenna Design," 2024 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2024, pp. 377-378, doi: 10.23919/USNC-URSINRSM60317.2024.10464597. [Online:] https://ieeexplore.ieee.org/abstract/document/10464597

4. L. Linkous, J. Lundquist and E. Topsakal, "AntennaCAT: Automated Antenna Design and Tuning Tool," 2023 IEEE USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Portland, OR, USA, 2023, pp. 89-90, doi: 10.23919/USNC-URSI54200.2023.10289238.  [Online:] https://ieeexplore.ieee.org/abstract/document/10289238

5. E. Karincic, E. Topsakal, and L. Linkous.  "Patch Antenna Calculations and Fabrication Made Simple for Cyber Security Research,"  2023 ASEE Annual Conference & Exposition, Baltimore , Maryland, 2023, June.  ASEE Conferences, 2023. [Online:] https://peer.asee.org/43974 

6. L. Linkous, E. Karincic, J. Lundquist and E. Topsakal, "Automated Antenna Calculation, Design and Tuning Tool for HFSS," 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2023, pp. 229-230, doi: 10.23919/USNC-URSINRSM57470.2023.10043119.  [Online:] https://ieeexplore.ieee.org/abstract/document/10043119

**Individual Optimizer Repositories:**

| Base Optimizer | Alternate Version | Quantum-Inspired Optimizer | Surrogate Model Version |
| ------------- | ------------- | ------------- |------------- |
| [pso_python](https://github.com/LC-Linkous/pso_python) | [pso_basic](https://github.com/LC-Linkous/pso_python/tree/pso_basic) | [pso_quantum](https://github.com/LC-Linkous/pso_python/tree/pso_quantum)  | |
| [cat_swarm_python](https://github.com/LC-Linkous/cat_swarm_python) | [sand_cat_python](https://github.com/LC-Linkous/cat_swarm_python/tree/sand_cat_python)| [cat_swarm_quantum](https://github.com/LC-Linkous/cat_swarm_python/tree/cat_swarm_quantum) | |
| [chicken_swarm_python](https://github.com/LC-Linkous/chicken_swarm_python) | - | [chicken_swarm_quantum](https://github.com/LC-Linkous/chicken_swarm_python/tree/chicken_swarm_quantum)  | |
| [sweep_python](https://github.com/LC-Linkous/sweep_python)  | *alternates in base repo | -  | - |
| [bayesian optimization_python](https://github.com/LC-Linkous/bayesian_optimization_python)  | -| - | *interchangeable surrogate models <br> included in base repo |
| [multi_glods_python](https://github.com/LC-Linkous/multi_glods_python)| - | - | |

The [Objective Function Test Suite](https://github.com/LC-Linkous/objective_function_suite)used to collect performance data on the individual optimizers is now public.




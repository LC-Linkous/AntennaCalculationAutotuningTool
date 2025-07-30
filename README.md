# AntennaCAT Development Branch
## {Refer to the MAIN BRANCH for the stable software release}

Ansys Electronic Desktop 2025 is out! And we are in the middle of testing integration with this release, and adding the core AntennaCAT 2025.2 features into the official release.

This branch is the `development branch` for AntennaCAT. Here you'll find some new features as we're updating to match both Windows and ANSYS HFSS updates. This code is mostly stable, but you may find a few bugs before the code is ready for the main AntennaCAT branch. Feel free to report those to us! 

To those who have reached out about features (current, planned, and a few bugs), we want to say THANK YOU!! Your input has been greatly appreciated, especially in the early stages of this project and its development.


## Current Features Being Implemented

**Current updates completed:**
* AntennaCAT 2021.1.1 pushed Jul 2025, new dev branch started for daily updates for next push
* 


**What's in the Queue:**
* Save & read for the 'Help Me Choose' fix to match the optimizer updates.
  * This needs the hooks updated to handle the new (full) dataframe structure update for saving and data pass through. 
  * Corrected parameter count after the dataframe change has started the re-integration
* Core 2025.2 features
  * Layers (needs to be re-tested with the new Ansys 2025 update)
  * DXF import (needs to be re-tested with new Ansys 2025 update + 3rd party DXF library change)


**2025.1.1 fixed bugs:**
* Fixed core bugs with Windows 10 & Windows 11, and compatibility with HFSS 2021, 2022, 2023, 2024, 2025. Combinations of the 2 OS versions, and 5 Ansys versions was causing issues with raw strings, paths, and text merging in files with newline (Maybe. Might have been co-bug).
* Save features now have values properly recorded & data types are preserved. Switch to dataframe helped with 95% of this for raw strings and paths.
* AntennaCAT now saves primary configuration data structures
* AntennaCAT now can open and set primary configuration data structures
* Numeric precision added for optimizers, uncluding surrogate models
* Numeric precision added for calculator
* Numeric precision added for batch sim
* Numeric precision has been tested for all optimizers. Imported report data does NOT have trunacation yet until report parsing is updated/streamlined
* Optimizers can now export their saved states as a seperate file for record purposes
* Importing optimier config has a pop up warning that it is disabled until the final save formats are established  (in final stage of testing to retain data types and pass surrogate model states)
* Some Settings Page config buttons disabled to make it clear what is being worked on vs. already implemented
* calculator return text is now in a 2 column format to make it easier to read
* optimizer parameters (lower and upper bounds) are now in a 2 column format to make it easier to read
* optimizer parameter name previews are tuncated at 25 characters to retain 2 column format. This does not impact the parameters as they are used in the optimizer, just the preview. 
* project configuration is now using multiple dataframes
* design configuration is now using multiple dataframes
* project configuration how has dataframe-based import and export
* design configuration now has data-frame based import and export
* simulation object can export in dictionary to dataframe format, but is NOT dataframe based
* number of licences has been forced typed as an INT in settings
* import of number of licences has been force typed as an INT on import
* controllable parameter count accuracy has been updated with the switch to dataframe from array. previously it counted the number of arrays within a 2-D array, now it counts the columns in the dataframe 
* button events for export now have proper null pass through so it can be triggered programatically for pass through. 
* Licence summary added on settings with references
* AntennaCAT welcome note added
* AntennaCAT versioning now uses a CONSTANT 
* optimizers have been updated and streamlined for the saving and export process, some unused variables have been removed. 
* All optimizers now have TARGET and THRESHOLD options for evaluation
* Extra break conditions have been added for the MultiGLODS optimizer so that a maximum limit of obective function calls have equal priority to the radii tolerance
* MultiGLODS Objective function evaluation to target tolerance now as a seperate value from the radii tolerance
* removed unused clean project, this is streamlined so that the .ancat file can be deleted. No collected data is deleted if the .ancat file is deleted, just project configs
* updated parsing for size on disk and user info
* studen license option can be remembered, but is not a default setting
* save overwrite for path set to correctly remember path string (extension of Windows issues)
* user information and comments are now properly saved and loaded (no more split strings or half-messages)
* deep copy used so that PC, DC, and SO read in objects are split properly in memory at creation
* updated Save button on Settings page to save ALL paths for project configs

# AntennaCAT

<p align="center">
 <img src="./src/media/antennaCAT-icons/transparent-antennaCAT-logo.png" height="200" >
</p>

Antenna Calculation and Autotuning Tool (AntennaCAT) is a comprehensive implementation of machine learning to automate, evaluate, and optimize the antenna design process using EM simulation software. It utilizes a combined antenna designer and internal calculator to accelerate the CAD construction and EM simulation of several common topologies, while eliminating model disparity for automated data collection.

AntennaCAT 2025.1.1 is live as of July 2025! We're excited to introduce some streamlined UI features, updated replication study templates, and some optimizer overhauls that include the ability to target threshold values instead of just targets! 

It's been a busy month with both the release of the [AntennaCAT article](https://ieeexplore.ieee.org/abstract/document/11063361) in the June edition of IEEE Antennas and Propagation Magazine and the release of Ansys Electronic Desktop 2025.... and a few Windows 10 to 11 update bugs. But we are quickly coming up on the planned AntennaCAT 2025.2! It will have some polished features and a few new ones. As we work these new (and some previously unplanned) features into the software based on feedback and bug reports, the [development branch](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/tree/dev) of this repo has been introduced for anyone that wants a preview.  

To those who have reached out about features (current, planned, and a few bugs), we want to say THANK YOU!! Your input has been greatly appreciated, especially in the early stages of this project and its development.

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

As we prepare for major code releases, we're sharing information on the Wiki of how to download, set up and use AntennaCAT.

You can [Start Here](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki) for general project information.

Pages are being updated daily, so check back in a few days if the information you're looking for hasn't been posted yet.

## Current Release

AntennaCAT 2025.1 is live!... and so is our first official minor release!

**Current updates completed:**
* Fixed core bugs with Windows 10 & Windows 11, and compatibility with HFSS 2021, 2022, 2023, 2024, 2025. Combinations of the 2 OS versions, and 5 Ansys versions were causing issues with raw strings, paths, and text merging in files with newline (Maybe. Might have been co-bug).
* Save features now have values properly recorded & data types are preserved. Switch to dataframe helped with 95% of this for raw strings and paths. (but not the interpretation, as expected) 
* AntennaCAT now saves primary configuration data structures
* AntennaCAT now can open and set primary configuration data structures
* Numeric precision added for optimizers, including surrogate models
* Numeric precision added for calculator
* Numeric precision added for batch sim
* Numeric precision has been tested for all optimizers. Imported report data does NOT have truncation yet until report parsing is updated/streamlined
* Optimizers can now export their saved states as a separate file for record purposes
* Importing optimizer config has a pop up warning that it is disabled until the final save formats are established  (in final stage of testing to retain data types and pass surrogate model states)
* Some Settings Page config buttons disabled to make it clear what is being worked on vs. already implemented
* Calculator return text is now in a 2-column format to make it easier to read
* Optimizer parameters (lower and upper bounds) are now in a 2-column format to make it easier to read
* Optimizer parameter name previews are truncated at 25 characters to retain 2-column format. This does not impact the parameters as they are used in the optimizer, just the preview. 
* Project configuration is now using multiple dataframes
* Design configuration is now using multiple dataframes
* Project configuration how has dataframe-based import and export
* Design configuration now has data-frame based import and export
* Simulation object can export in dictionary to dataframe format, but is NOT dataframe based
* Number of licenses has been forced typed as an INT in settings
* Import of number of licenses has been force typed as an INT on import
* Controllable parameter count accuracy has been updated with the switch to dataframe from array. previously it counted the number of arrays within a 2-D array, now it counts the columns in the dataframe 
* Button events for export now have proper null pass through so it can be triggered programmatically for pass through. 
* License summary added on settings with references
* AntennaCAT welcome note added
* AntennaCAT versioning now uses a CONSTANT 
* Optimizers have been updated and streamlined for the saving and export process, some unused variables have been removed. 
* All optimizers now have TARGET and THRESHOLD options for evaluation
* Extra break conditions have been added for the MultiGLODS optimizer so that a maximum limit of objective function calls have equal priority to the radii tolerance
* MultiGLODS Objective function evaluation to target tolerance now as a separate value from the radii tolerance
* removed unused clean project, this is streamlined so that the .ancat file can be deleted. No collected data is deleted if the .ancat file is deleted, just project configs
* Updated parsing for size on disk and user info
* Student license option can be remembered, but is not a default setting. (Remember to follow license requirements for research! We enjoy supporting student learning opportunities, but some licenses have requirements about using non-student license options for any official research)
* Save overwrite for path set to correctly remember path string (extension of Windows issues)
* User information and comments are now properly saved and loaded (no more split strings or half-messages)
* Deep copy used so that configuration and simulation scripts objects are split properly in memory at creation when opening saved files. (no more saved multi-object layer shared memory!)
* Updated Save button on Settings page to save ALL paths for project configs


**What's Popped up to the Top of the Queue?**
* Save & read for the 'Help Me Choose' fix to match the optimizer updates.
  * This needs the hooks updated to handle the new (full) dataframe structure update for saving and data pass through. 
  * Corrected parameter count after the dataframe change has started the re-integration
* Core 2025.2 features
  * Layers (needs to be re-tested with the new Ansys 2025 update)
  * DXF import (needs to be re-tested with new Ansys 2025 update + 3rd party DXF library change)
* Logging
  * To help with bug reporting, actual logging is being implemented to collect helpful reporting information


**Why are we not matching the literature exactly?** 
* The driving goal behind the development of this software is for it to be useful and to encourage experimentation. Holding back features/functionality to be truer to the publications goes against that. 
* Now that we have more users, we're getting feedback on how different versions of Windows and different setups work with AntennaCAT. 

**Why not release it all at once?**
* The goal of several major releases close together is to have some roll-back points as collaborators join in and want to implement their own features. We won't wait to release what's already been implemented in recent publications, but there will be links to these 'check points' should anyone wish to download an earlier version.

## Release Schedule 

**Where are we so far?** 
* AntennaCAT 2025.1.1 is live!

We are in the quick release stage for several major features. See the [Past Releases section on the Documentation Wiki page](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki/Documentation#past-releases) for the list of all releases. 2025.0, 2025.1, and 2025.2 and their corresponding lit will be listed in the Wiki.

What does that mean for code releases?
* The code will always be released independently from the journal/magazine publication. While publications are awesome and we want to share what we're up to, sometimes we might move a little faster than planned. Or slower, because code takes time.

* Post release 1, updates and code examples will be found at https://lc-linkous.github.io/projects/antennaCAT AND the [wiki](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki/)
* Documentation of usage examples will be posted in the Wiki on this page. The full explanation of all of the details that did not fit in the dissertation will begin appearing, but this may take some time

* The [development branch](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/tree/dev) is updating almost daily as we work to get caught up with the APM article release. The bugs causing the major hold up have been squashed!

Stages of early 2025 major revision roll out:

 * AntennaCAT v. 2025.1.1
  * Updates on Windows machines and Ansys licenses revealed some bugs... that revealed some more bugs.
  * AntennaCAT now works with W10, W11, and with Ansys HFSS 2021, 2022, 2023, 2024, and 2025
  
* AntennaCAT v. 2025.1
  * Replication set updates from user feedback.
  * Updated naming convention updates in the templates for the parameterized HFSS files
  * Surrogate model optimizers are integrated! Stress testing is ongoing to verify failed simulation recovery.
  * Loading projects now has larger text boxes to make it easier to input parameter names

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

1. L. Linkous, J. Lundquist, M. J. Suche and E. Topsakal, "AntennaCAT: Automated antenna design with machine learning-assisted optimization [Open Source]," in IEEE Antennas and Propagation Magazine, vol. 67, no. 3, pp. 87-96, June 2025, doi: 10.1109/MAP.2025.3560851.

2. L. Linkous, “Machine Learning Assisted Optimization for Calculation and Automated Tuning of Antennas,” VCU Scholars Compass, 2024. https://scholarscompass.vcu.edu/etd/7841/ (accessed Oct. 21, 2024).

3. L. Linkous, J. Lundquist, M. Suche and E. Topsakal, "Machine Learning Assisted Hyperparameter Tuning for Optimization," 2024 IEEE INC-USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Florence, Italy, 2024, pp. 107-108, doi: 10.23919/INC-USNC-URSI61303.2024.10632482.

4. L. Linkous and E. Topsakal, "Machine Learning Assisted Optimization Methods for Automated Antenna Design," 2024 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2024, pp. 377-378, doi: 10.23919/USNC-URSINRSM60317.2024.10464597. [Online:] https://ieeexplore.ieee.org/abstract/document/10464597

5. L. Linkous, J. Lundquist and E. Topsakal, "AntennaCAT: Automated Antenna Design and Tuning Tool," 2023 IEEE USNC-URSI Radio Science Meeting (Joint with AP-S Symposium), Portland, OR, USA, 2023, pp. 89-90, doi: 10.23919/USNC-URSI54200.2023.10289238.  [Online:] https://ieeexplore.ieee.org/abstract/document/10289238

6. E. Karincic, E. Topsakal, and L. Linkous.  "Patch Antenna Calculations and Fabrication Made Simple for Cyber Security Research,"  2023 ASEE Annual Conference & Exposition, Baltimore , Maryland, 2023, June.  ASEE Conferences, 2023. [Online:] https://peer.asee.org/43974 

7. L. Linkous, E. Karincic, J. Lundquist and E. Topsakal, "Automated Antenna Calculation, Design and Tuning Tool for HFSS," 2023 United States National Committee of URSI National Radio Science Meeting (USNC-URSI NRSM), Boulder, CO, USA, 2023, pp. 229-230, doi: 10.23919/USNC-URSINRSM57470.2023.10043119.  [Online:] https://ieeexplore.ieee.org/abstract/document/10043119

**Individual Optimizer Repositories:**

| Base Optimizer | Alternate Version | Quantum-Inspired Optimizer | Surrogate Model Version |
| ------------- | ------------- | ------------- |------------- |
| [pso_python](https://github.com/LC-Linkous/pso_python) | [pso_basic](https://github.com/LC-Linkous/pso_python/tree/pso_basic) | [pso_quantum](https://github.com/LC-Linkous/pso_quantum)  | all versions are options in [surrogate_model_optimization](https://github.com/LC-Linkous/surrogate_model_optimization)|
| [cat_swarm_python](https://github.com/LC-Linkous/cat_swarm_python) | [sand_cat_python](https://github.com/LC-Linkous/cat_swarm_python/tree/sand_cat_python)| [cat_swarm_quantum](https://github.com/LC-Linkous/cat_swarm_python/tree/cat_swarm_quantum) |all versions are options in [surrogate_model_optimization](https://github.com/LC-Linkous/surrogate_model_optimization) |
| [chicken_swarm_python](https://github.com/LC-Linkous/chicken_swarm_python) | [2015_improved_chicken_swarm](https://github.com/LC-Linkous/chicken_swarm_python/tree/improved_chicken_swarm) <br>2022 improved chicken swarm| [chicken_swarm_quantum](https://github.com/LC-Linkous/chicken_swarm_python/tree/chicken_swarm_quantum)  | all versions are options in [surrogate_model_optimization](https://github.com/LC-Linkous/surrogate_model_optimization)|
| [sweep_python](https://github.com/LC-Linkous/sweep_python)  | *alternates in base repo | -  | - |
| [bayesian optimization_python](https://github.com/LC-Linkous/bayesian_optimization_python)  | -| - | *interchangeable surrogate models <br> included in base repo |
| [multi_glods_python](https://github.com/LC-Linkous/multi_glods_python)| GLODS <br> DIRECT | - | multiGLODS option in [surrogate_model_optimization](https://github.com/LC-Linkous/surrogate_model_optimization)|


The [Objective Function Test Suite](https://github.com/LC-Linkous/objective_function_suite) used to collect performance data on the individual optimizers is now public.






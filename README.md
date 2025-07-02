# AntennaCAT Development Branch
## {Refer to the MAIN BRANCH for the stable software release}

<p align="center">
 <img src="./src/media/antennaCAT-icons/transparent-antennaCAT-logo.png" height="200" >
</p>

Antenna Calculation and Autotuning Tool (AntennaCAT) is a comprehensive implementation of machine learning to automate, evaluate, and optimize the antenna design process using EM simulation software. It utilizes a combined antenna designer and internal calculator to accelerate the CAD construction and EM simulation of several common topologies, while eliminating model disparity for automated data collection.

This branch is the `development branch` for AntennaCAT. Here you'll find some new features as we're updating to match both Windows and ANSYS HFSS updates. This code is mostly stable, but you may find a few bugs before the code is ready for the main AntennaCAT branch. Feel free to report those to us! 



To those who have reached out about features (current, planned, and a few bugs), we want to say THANK YOU!! Your input has been greatly appreciated, especially in the early stages of this project and its development.

## Table of contents
* [Wiki and Documentation](#wiki-and-documentation)
* [Current Features Being Implemented](#current-release)
* [Release Schedule](#release-schedule)
* [Requirements](#requirements)
* [Organization](#organization)
* [Running](#running)

## Wiki and Documentation

See the [Release Schedule](#release-schedule) below for code roll out updates.

As we prepare for the first code release, we're sharing information on the Wiki of how to download, set up and use AntennaCAT.

You can [Start Here](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki) for general project information.

Pages are being updated daily, so check back in a few days if the information you're looking for hasn't been posted yet.

## Current Features Being Implemented

* Current updates:
  * Windows 11 path fixes. Some raw strings that worked for file paths in W10 do not work for all W11 machines. Updating this.
  * Save features. Related to the paths and how some raw strings were parsed. Updating this.
  * Optimizer updates for specifying decimals and tolerance.
  * Extra break conditions for MultiGLODS 


* What's in the Queue:
  * Save & read for the 'Help Me Choose' fix to match the optimizer updates. (This needs the 'hooks' to be put back before we can update values automatically)


## Release Schedule 

* Next stable update: July 12th
  * Windows 11 bugs, saving, optimizer updates

* Pending Update: 
  * Core 2025.2 features as soon as the save files and paths are working on W10 and W11.



## Recent Previous Releases

We are in the quick release stage for several major features. See the [Past Releases section on the Documentation Wiki page](https://github.com/LC-Linkous/AntennaCalculationAutotuningTool/wiki/Documentation#past-releases) for the list of all releases. 2025.0, 2025.1, and 2025.2 and their corresponding lit will be listed in the Wiki.


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

* AntennaCAT v. 2025.0
  * The 12 topology replication set.  
  * All optimizers integrated fully with the GUI. 
  * This is the 'core' functionality of AntennaCAT without the add-ons. 
  * It sets us up for plugging in all of the developments from Summer 2024 onwards (2 conferences + dissertation)

* AntennaCAT v. 2025.1
  * Replication set updates from user feedback.
  * Updated naming convention updates in the templates for the paramaterized HFSS files
  * Surrogate model optimizers are integrated! Stress testing is ongoing to verify failed simulation recovery.
  * Loading projects now has larger text boxes to make it easier to input parameter names



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



Project configuration hierarchy

antennaCAT_config.py
* internal globals that are not user changed. Paths/configs controlled from here for debug will slowly be moved into saved config files in userconfig

project_config.py
* All file names, file paths, and default names. 
* This is the highest level of configuration and will not change while the program is running

design_config.py
* All design features. Material info, substrate layers, superstrate layers, conductor layers
* simulation info is contained here
    * simulation settings are generally static, but in some variations of tuning dynamic ranges are used
* generated code is also stored here


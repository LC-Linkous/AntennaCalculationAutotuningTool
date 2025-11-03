# AntennaCAT Development Branch
## {Refer to the MAIN BRANCH for the stable software release}

Ansys Electronic Desktop 2025 is out! And we are in the middle of testing integration with this release, and adding the core AntennaCAT 2025.2 features into the official release.

This branch is the `development branch` for AntennaCAT. Here you'll find some new features as we're updating to match both Windows and ANSYS HFSS updates. This code is mostly stable, but you may find a few bugs before the code is ready for the main AntennaCAT branch. Feel free to report those to us! 

To those who have reached out about features (current, planned, and a few bugs), we want to say THANK YOU!! Your input has been greatly appreciated, especially in the early stages of this project and its development.


## Current Features Being Implemented

**Current updates completed:**
* AntennaCAT 2021.1.2 prep for next push in progress, new dev branch started for updates for next revision


**What's in the Queue:**
* Re-test of all optimizers with the new logging format
  * While stable, we are confirming that all optimizers are still converging properly after the changes.
* Preparation for executable bundle
  * format fixes, import checks, version lineups, etc.
* Save & read for the 'Help Me Choose' fix to match the optimizer updates.
  * This needs the hooks updated to handle the new (full) dataframe structure update for saving and data pass through. 
  * Corrected parameter count after the dataframe change has started the re-integration
* Ansys features
  * IF/ELSE logic to the templates for importing custom sim setups
* Core 2025.2 features
  * Layers (needs to be re-tested with the new Ansys 2025 update)
  * DXF import (needs to be re-tested with new Ansys 2025 update + 3rd party DXF library change)


**2025.1.2 change log:**
(October&November 2025)
* Logging added to all files that previously printed out any kind of message
  * Classes that were pass through only do not log in order to cut down on duplicate messages in log file
* Improved status and detail messages in UI
  * This includes instructions for how to pause, stop, and run optimizers
  * Optimizer messages have been shortened and include new formatting
  * Status and Detail scroll windows are now READ ONLY to prevent accidental deleting of progress log (AntennaCAT does not read in text, so this is for user benefit only)
* Improved statemachine for IU driven optimization
  * Logging added to the state machine controlling the optimizer&simulation process as driven by the UI (start, stop, pause, etc.) now reports more accurately where in the process the user input and automation process crossover.
  * Likewise, extra checks added to the state machine now make it more resistant to error states caused by toggling run/stop/pause in previously unhandled combinations
* Clearer messages for optimizer status
  * Some messages that were duplicated by the additional states were removed to declutter the status scroll window
  * It is now more clear when the optimizer has converged, with explicit printouts after converging of the parameters and the optimized targets.  

**2025.1.1 change log:**
(July&August 2025)
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



# AntennaCAT Development Branch
## {Refer to the MAIN BRANCH for the stable software release}

Ansys Electronic Desktop 2025 is out! And we are in the middle of testing integration with this release, and adding the core AntennaCAT 2025.2 features into the official release.

This branch is the `development branch` for AntennaCAT. Here you'll find some new features as we're updating to match both Windows and ANSYS HFSS updates. This code is mostly stable, but you may find a few bugs before the code is ready for the main AntennaCAT branch. Feel free to report those to us! 

To those who have reached out about features (current, planned, and a few bugs), we want to say THANK YOU!! Your input has been greatly appreciated, especially in the early stages of this project and its development.


## Current Features Being Implemented

**Current updates completed:**
* AntennaCAT 2021.1.1 pushed Jul 2025, new dev branch started for daily updates for next revision


**What's in the Queue:**
* Save & read for the 'Help Me Choose' fix to match the optimizer updates.
  * This needs the hooks updated to handle the new (full) dataframe structure update for saving and data pass through. 
  * Corrected parameter count after the dataframe change has started the re-integration
* Core 2025.2 features
  * Layers (needs to be re-tested with the new Ansys 2025 update)
  * DXF import (needs to be re-tested with new Ansys 2025 update + 3rd party DXF library change)
* Logging
  * To help with bug reporting, actual logging is being implemented to collect helpful reporting information


**2025.1.1 fixed bugs:**
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



##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/COMSOL/templateGen_Design.py'
#   Class for COMSOL antenna template generator.
#
#   NOTE: Redoing with the updated ANSYS template to bring everything up to date
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


from datetime import datetime
import os.path
import math

import project.config.antennaCAT_config as c

class DesignTemplate:
    def __init__(self, projName, projDir):
        self.templateTxt = []
        self.projectName = projName
        self.projectPath = projDir + "/" + self.projectName

        
    def loadTemplate(self):
        pass

    def getTemplateScript(self):
        return self.templateTxt

    def clearTemplateText(self):
        #primarily for unit testing
        self.templateTxt.clear()
                
    def setLoadedTemplateScript(self, t):
        # only for loading in designs from file
        self.templateTxt = t

    def addCommentsToFile(self, c=None):
        now = datetime.now()
        tmpStr = ""

        self.templateTxt.append(tmpStr)
    
    def AddOpenExistingProjectBase(self):
        PROJECT_PATH = ""
        txt= ""
        self.templateTxt.append(txt)

    def deleteParticleGroup(self):
        # this also exists in the simulation template
        #make more general based on naming conventions
        tmpStr = ""
        self.templateTxt.append(tmpStr)
 
    def groupParticles(self, nameList):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def addFiniteBoundaryParticles(self, nameList):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def addRectangle(self, rectName, xLoc, yLoc, particleResolution, material):
        tmpStr = ""
        self.templateTxt.append(tmpStr)
    
    def resizeGroundplane(self, newL):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def updateProjectParametersWithList(self, paramList):
        pass
    
    def changeProjectParameter(self, paramName, paramVal="1"):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def patchStripFedScriptGenerator(self, w, l, d, sw, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        tmpStr = ""
        self.templateTxt.append(tmpStr)
    
    def patchProbeFedScriptGenerator(self, w, l, x0, y0, d, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def geneticPatchProbeFedScriptGeneratorBase(self, d, resolution= "1 mm", cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        tmpStr = ""
        self.templateTxt.append(tmpStr)

    def geneticPatchProbeFedScriptGeneratorParticles(self, particleList, numRows, numCols, particleResolution, cMaterial="copper"):
        tmpStr = ""
        self.templateTxt.append(tmpStr)
 
            

if __name__ == "__main__":
    import sys
    sys.path.insert(0, './')
    import src.helper_func.fileIO_helperFuncs as fIO

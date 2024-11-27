##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/CST/templateGen_Design.py'
#   Class for CST antenna template generator.
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
    

    AT = DesignTemplate(projDir="C:/Users/LCLin/Desktop/")
    AT.addCommentsToFile("test generation")
    #AT.patchStripFedScriptGenerator("15.73mm", "11.74mm", "1.6mm", "3mm", "copper", "copper", "FR4_epoxy")
    #AT.patchProbeFedScriptGenerator("25.36mm", "19.41mm",  "12.68mm", "7.45mm", "1.6mm",cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy")
    #AT.geneticPatchProbeFedScriptGeneratorBase("25.36mm", "19.41mm",  "12.68mm", "7.45mm", "1.6mm", ".2mm", "copper", "copper", "FR4_epoxy")
    AT.geneticPatchProbeFedScriptGeneratorBase("1.6mm", "1mm", "copper", "copper", "FR4_epoxy")
    template = AT.getTemplateScript()
    #print(template)
    noErrors = fIO.writeOut("C:/Users/LCLin/Desktop/test-probe-patch-script.py", template)

    #it takes about .5 seconds (at best) to draw each particle. so use only a fw for testing. or use higher resolution
    # exampleList = [[235.0, 209.0, 'square'], [223.0, 269.0, 'square'], [219.0, 235.0, 'square'], 
    #                 [222.0, 233.0, 'square'], [222.0, 198.0, 'square'], [232.0, 208.0, 'square'], 
    #                 [230.0, 201.0, 'square'], [232.0, 268.0, 'square'], [254.0, 238.0, 'square'], 
    #                 [228.0, 215.0, 'square'], [232.0, 229.0, 'square'], [225.0, 195.0, 'square']]

    #resolution 5
    exampleList = [[44, 44, 1], [44, 45, 1], [44, 46, 1], [44, 47, 1], [45, 44, 1], [45, 45, 1], [45, 46, 1], 
                [45, 47, 1], [46, 44, 1], [46, 45, 1], [46, 46, 1], [46, 47, 1], [47, 44, 1], [47, 45, 1], 
                [47, 46, 1], [47, 47, 1], [42, 43, 1], [47, 43, 1], [45, 48, 1], [38.0, 67.0, 1], [43, 45, 1],
                 [56.0, 60.0, 1], [44, 48, 1], [45, 42, 1], [49, 46, 1], [42, 44, 1], [56.0, 35.0, 1], 
                 [45, 43, 1], [40.0, 67.0, 1], [48, 44, 1], [42, 42, 1]]
    numRows = 450
    numCols = 450
    AT.geneticPatchProbeFedScriptGeneratorParticles(exampleList, numRows, numCols, 5)
    noErrors = fIO.writeOut("C:/Users/LCLin/Desktop/generated-particles-script.py", template)

    AT.clearTemplateText()
    AT.addCommentsToFile("test generation")
    print(template)
    AT.AddOpenExistingProjectBase()#fullPath="C:/Users/LCLin/Desktop//GeneratedHFSSProject.aedt")
    AT.deleteParticleGroup()
    AT.resizeGroundplane(newL=60)

    template = AT.getTemplateScript()
    #print(template)
    noErrors = fIO.writeOut("C:/Users/LCLin/Desktop/test-edit-probe-patch-script.py", template)
    print(noErrors)


    #TODO remove the simulation text at the end


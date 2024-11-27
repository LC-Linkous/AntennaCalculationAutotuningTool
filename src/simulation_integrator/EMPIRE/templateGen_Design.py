##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/EMPIRE/templateGen_Design.py'
#   Class for EMPIRE antenna template generator.
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
        tmpStr = "# ----------------------------------------------------\n " +\
                     "# ANSYS HFSS script generated by AntennaCAT version 2.0 \n" + \
                     "# " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "\n" \
                     "# ----------------------------------------------------\n" +\
                     "# " + str(c) + "\n" + \
                     "# ----------------------------------------------------\n"

        self.templateTxt.append(tmpStr)
    
    def addOpenExistingProjectBase(self):
        PROJECT_PATH = "\"" + self.projectPath + "\""
        txt="import ScriptEnv \n" +\
            "ScriptEnv.Initialize(\"Ansoft.ElectronicsDesktop\")\n"+\
            "oDesktop.RestoreWindow()\n"+\
            "oDesktop.OpenProject(" + PROJECT_PATH + ")\n"+\
            "oProject = oDesktop.SetActiveProject(\"GeneratedHFSSProject\")\n" +\
            "oDesign = oProject.SetActiveDesign(\"HFSSDesign1\")\n"+\
            "oEditor = oDesign.SetActiveEditor(\"3D Modeler\")\n" 
        self.templateTxt.append(txt)

    def deleteParticleGroup(self):
        # this also exists in the simulation template
        #make more general based on naming conventions
        tmpStr = "oEditor.Delete([\"NAME:Selections\", \n " +\
             "\"Selections:=\"		, \"particle_Group\"])\n"
        self.templateTxt.append(tmpStr)
 
    def groupParticles(self, nameList):
        tmpStr = "oEditor.CreateGroup(\n"+\
        "[\n"+\
		"\"NAME:GroupParameter\",\n"+\
		"\"ParentGroupID:=\"	, \"Model\",\n" +\
		"\"Parts:=\"		, \"" + nameList + "\" ,\n"+\
        "\"SubmodelInstances:=\"	, \"\",\n"+\
		"\"Groups:=\"		, \"\"\n"+\
	    "])\n"

        self.templateTxt.append(tmpStr)

    def addFiniteBoundaryParticles(self, nameList):
        tmpStr = "oModule = oDesign.GetModule(\"BoundarySetup\")\n" +\
        "oModule.AssignFiniteCond(\n"+\
        "[\n"+\
		"\"NAME:FiniteCond3\","+\
		"\"Objects:=\"		, [" + nameList + "],\n"+\
		"\"UseMaterial:=\"		, True,\n"+\
		"\"Material:=\"		, \"copper\",\n"+\
		"\"UseThickness:=\"	, False,\n"+\
		"\"Roughness:=\"		, \"0um\",\n"+\
		"\"InfGroundPlane:=\"	, False,\n"+\
		"\"IsTwoSided:=\"		, False,\n"+\
		"\"IsInternal:=\"		, True\n"+\
	    "])\n"

        self.templateTxt.append(tmpStr)

    def addRectangle(self, rectName, xLoc, yLoc, particleResolution, material):
        #this works better as a function because of how many times it would be called and parsed
        pRes = str(particleResolution) + " mm"
        tmpStr= "oEditor = oDesign.SetActiveEditor(\"3D Modeler\")\n" +\
        "oEditor.CreateRectangle(\n" +\
        "[\n"  +\
        "\"NAME:RectangleParameters\", \n" +\
        "\"IsCovered:=\" , True,\n" +\
        "\"XStart:=\" , \"" + str(xLoc) + "mm\" ,\n" +\
        "\"YStart:=\" , \"" + str(yLoc) + "mm\" ,\n" +\
        "\"ZStart:=\" , \"0mm\", \n" +\
        "\"Width:=\" , \"" + pRes + "\" ,\n" +\
        "\"Height:=\" , \""+ pRes +"\" ,\n" +\
        "\"WhichAxis:=\" , \"Z\"\n" +\
        "],\n" +\
        "[\n" +\
        "\"NAME:Attributes\",\n" +\
        "\"Name:=\" , \"" + str(rectName) +"\" ,\n" +\
        "\"Flags:=\" , \"\",\n" +\
        "\"Color:=\" , \"(250 195 5)\",\n"+\
        "\"Transparency:=\" , 0,\n" +\
        "\"PartCoordinateSystem:=\", \"Global\",\n" +\
        "\"UDMId:=\" , \"\",\n" +\
        "\"MaterialValue:=\" , " + str(material)+ " ,\n" +\
        "\"SurfaceMaterialValue:=\", \"\\\"\\\"\",\n" +\
        "\"SolveInside:=\" , True,\n"+\
        "\"ShellElement:=\" , False, \n" +\
        "\"ShellElementThickness:=\", \"0mm\",\n" +\
        "\"IsMaterialEditable:=\" , True,\n" +\
        "\"UseMaterialAppearance:=\", False,\n" +\
        "\"IsLightweight:=\" , False\n" +\
        "]) \n" 
        self.templateTxt.append(tmpStr)
    
    def resizeGroundplane(self, newL):
        tmpStr="oProject.ChangeProperty(\n" +\
	        "[\n" +\
		    "\t\"NAME:AllTabs\", \n" +\
		    "\t[" +\
			"\t\"NAME:ProjectVariableTab\", \n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:PropServers\", \n" +\
			"\t\t\"ProjectVariables\" \n" +\
			"\t\t],\n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:ChangedProps\",\n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:$ground_plane\",\n" +\
			"\t\t\"Value:=\"		, \"" + str(newL) + "mm\"\n" +\
			"\t\t]\n" +\
			"\t\t]\n" +\
		    "\t]\n" +\
	        "])\n"
        self.templateTxt.append(tmpStr)

    def updateProjectParametersWithList(self, paramList):
        print(paramList)
        for pl in paramList:
            #FOR NOW so safe vars to troubleshoot. TODO: edit
            if (pl[0] =="$width") or (pl[0] =="$length"):
                self.changeProjectParameter(pl[0], pl[1])
    
    def changeProjectParameter(self, paramName, paramVal="1"):
        INSERT_PARAM_NAME = str(paramName)
        INSERT_PARAM_VALUE= str(paramVal) #already as 'mm' in the template
        tmpStr="oProject.ChangeProperty(\n" +\
	        "[\n" +\
		    "\t\"NAME:AllTabs\", \n" +\
		    "\t[" +\
			"\t\"NAME:ProjectVariableTab\", \n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:PropServers\", \n" +\
			"\t\t\"ProjectVariables\" \n" +\
			"\t\t],\n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:ChangedProps\",\n" +\
			"\t\t[\n" +\
			"\t\t\"NAME:" + INSERT_PARAM_NAME + "\",\n" +\
			"\t\t\"Value:=\"		, \"" + INSERT_PARAM_VALUE + "mm\"\n" +\
			"\t\t]\n" +\
			"\t\t]\n" +\
		    "\t]\n" +\
	        "])\n"
        self.templateTxt.append(tmpStr)

    def patchStripFedScriptGenerator(self, w, l, d, sw, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        projectPath= "\"" + str(self.projectPath) + "\""
        atnW = "\"" + str(w) + "\""
        atnL = "\"" + str(l) + "\""
        atnDepth = "\"" + str(d) + "\""
        atnStripW = "\"" + str(sw) + "\""        
        substrateMaterial = "\"\\\"" + str(sMaterial) + "\\\"\""
        groundPlaneMaterial = "\"\\\"" + str(gpMaterial) + "\\\"\""
        groundPlaneMaterialBoundary = "\"" + str(gpMaterial) + "\""
        counductorMaterial = "\"\\\"" + str(cMaterial) + "\\\"\""
        counductorMatrialBoundary = "\"" + str(cMaterial) + "\""


        filepath = "./src/simulation_integrator/ANSYS/code_templates/patch_strip-fed.txt" 
        #filepath = "./src/simulation_integrator/ANSYS/code_templates/patch_strip-fed_adj-conductor.txt" 

        if os.path.isfile(filepath) == True:
            pass
        else:
            print("ERROR: templateGen_Antenna.py. path error to patch_strip-fed.txt template. check relative paths")
            print("attempted filepath: ", filepath)

        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    if l == "INSERT_WIDTH":
                        l = atnW
                    elif l == "INSERT_LENGTH":
                        l = atnL
                    elif l == "INSERT_DEPTH":
                        l = atnDepth
                    elif l == "INSERT_STRIP_WIDTH":
                        l = atnStripW
                    elif l == "INSERT_CONDUCTOR_MATERIAL":
                        l =  counductorMaterial#counductorMatrialBoundary
                    elif l == "INSERT_CONDUCTOR_MATERIAL_BOUNDARY_SETUP":
                        l = counductorMatrialBoundary #counductorMaterial
                    elif l == "INSERT_SUBSTRATE_MATERIAL":
                        l = substrateMaterial
                    elif l == "INSERT_GROUND_PLANE_MATERIAL":
                        l = groundPlaneMaterial    
                    elif l == "INSERT_GROUND_PLANE_MATERIAL_BOUNDARY_SETUP":
                        l = groundPlaneMaterialBoundary                    
                    elif str(l) == "oProject.SaveAs(PROJECT_NAME,":
                        l = "oProject.SaveAs(" + str(projectPath) + ","
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)
    
    def patchProbeFedScriptGenerator(self, w, l, x0, y0, d, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        projectPath= "\"" + str(self.projectPath) + "\""
        atnW = "\"" + str(w) + "\""
        atnL = "\"" + str(l) + "\""
        atnX0 = "\"" + str(x0) + "\""
        atnY0 = "\"" + str(y0) + "\""
        atnDepth = "\"" + str(d) + "\""
        substrateMaterial = "\"\\\"" + str(sMaterial) + "\\\"\""
        groundPlaneMaterial = "\"\\\"" + str(gpMaterial) + "\\\"\""
        groundPlaneMaterialBoundary = "\"" + str(gpMaterial) + "\""
        counductorMaterial = "\"\\\"" + str(cMaterial) + "\\\"\""
        counductorMatrialBoundary = "\"" + str(cMaterial) + "\""


        filepath = "./src/simulation_integrator/ANSYS/code_templates/patch_probe-fed.txt" 
        if os.path.isfile(filepath) == True:
            pass
        else:
            print("ERROR: templateGen_Antenna.py. path error to patch_probe-fed.txt template. check relative paths")
            print("attempted filepath: ", filepath)

        #dealing with the base template
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    if l == "INSERT_WIDTH":
                        l = atnW
                    elif l == "INSERT_LENGTH":
                        l = atnL
                    elif l == "INSERT_DEPTH":
                        l = atnDepth
                    elif l == "INSERT_X0":
                        l = atnX0
                    elif l == "INSERT_Y0":
                        l = atnY0
                    elif l == "INSERT_CONDUCTOR_MATERIAL":
                        l =  counductorMaterial
                    elif l == "INSERT_CONDUCTOR_MATERIAL_BOUNDARY_SETUP":
                        l = counductorMatrialBoundary
                    elif l == "INSERT_SUBSTRATE_MATERIAL":
                        l = substrateMaterial
                    elif l == "INSERT_GROUND_PLANE_MATERIAL":
                        l = groundPlaneMaterial    
                    elif l == "INSERT_GROUND_PLANE_MATERIAL_BOUNDARY_SETUP":
                        l = groundPlaneMaterialBoundary   
                    elif str(l) == "oProject.SaveAs(PROJECT_NAME,":
                        l = "oProject.SaveAs(" + str(projectPath) + ","
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)

    def geneticPatchProbeFedScriptGeneratorBase(self, d, resolution= "1 mm", cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy"):
        # this is just the basic structure
        # the ground plane is made larger later
        # so it doesn't need anything other than material info

        # Res freq = ~22.5Ghz @ -3.75dB
        # Gain = 1.86, efficiency = 0.27

        gp = "60 mm" # max(numRows, numCols)
        x0 = "30 mm" #int(numRows/2) #approx in the middle
        y0 = "30 mm" #int(numCols/2) #approx in the middle      
        seedW = "20 mm"
        seedL = "20 mm"  
        projectPath= "\"" + str(self.projectPath) + "\""
        atnX0 = "\"" + str(x0) + "\""
        atnY0 = "\"" + str(y0) + "\""
        atnSeedW = "\"" + str(seedW) + "\""
        atnSeedL = "\"" + str(seedL) + "\""
        atnDepth = "\"" + str(d) + "\""
        atnGp =  "\"" + str(gp) + "\""
        atnRes = "\"" + str(resolution) + "\""
        substrateMaterial = "\"\\\"" + str(sMaterial) + "\\\"\""
        groundPlaneMaterial = "\"\\\"" + str(gpMaterial) + "\\\"\""
        groundPlaneMaterialBoundary = "\"" + str(gpMaterial) + "\""
        counductorMaterial = "\"\\\"" + str(cMaterial) + "\\\"\""
        counductorMatrialBoundary = "\"" + str(cMaterial) + "\""


        filepath = "./src/simulation_integrator/ANSYS/code_templates/genetic_patch_probe-fed-base.txt" 
        if os.path.isfile(filepath) == True:
            pass
        else:
            print("ERROR: templateGen_Antenna.py. path error to genetic_patch_probe-fed.txt template. check relative paths")
            print("attempted filepath: ", filepath)

        #dealing with the base template
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    if l == "INSERT_DEPTH":
                        l = atnDepth
                    elif l == "INSERT_X0":
                        l = atnX0
                    elif l == "INSERT_Y0":
                        l = atnY0
                    elif l == "INSERT_SEED_WIDTH":
                        l = atnSeedW
                    elif l == "INSERT_SEED_LENGTH":
                        l = atnSeedL
                    elif l == "INSERT_GROUNDPLANE":
                        l = atnGp
                    elif l == "INSERT_PARTICLE_RES":
                        l = atnRes
                    elif l == "INSERT_CONDUCTOR_MATERIAL":
                        l =  counductorMaterial
                    elif l == "INSERT_CONDUCTOR_MATERIAL_BOUNDARY_SETUP":
                        l = counductorMatrialBoundary
                    elif l == "INSERT_SUBSTRATE_MATERIAL":
                        l = substrateMaterial
                    elif l == "INSERT_GROUND_PLANE_MATERIAL":
                        l = groundPlaneMaterial    
                    elif l == "INSERT_GROUND_PLANE_MATERIAL_BOUNDARY_SETUP":
                        l = groundPlaneMaterialBoundary   
                    elif str(l) == "oProject.SaveAs(PROJECT_NAME,":
                        l = "oProject.SaveAs(" + str(projectPath) + ","
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)

    def geneticPatchProbeFedScriptGeneratorParticles(self, particleList, numRows, numCols, particleResolution, cMaterial="copper"):
        #this edits the base template (which must be created first) to add parasitic particles
        #it needs a 2D list in the format [[x,y,...],[x,y,...],[]...] to draw squares at each coordinate
        
        #material
        counductorMaterial = "\"\\\"" + str(cMaterial) + "\\\"\""

        ##set/get base template
        #self.templateTxt = baseTemplate #includes sim setup, but not full sim

        maxX = 0
        maxY = 0

        #adding particles
        nameList = []#for grouping materials
        nameCtr = 1 #using HFSS' tendency to group by base/root name and number
        for p in particleList:
            pName = "particle"+str(nameCtr)
            nameList.append(pName)
            xVal = p[0]
            yVal = p[1]
            
            #need to scale vals around 0,0 (aka the probe point)
            centerX = math.floor(int(numRows)/2)
            centerY = math.floor(int(numCols)/2)
            scaledX = xVal*particleResolution - centerX #bring back to center
            scaledY = yVal*particleResolution - centerY
            #set max distance from center
            if abs(scaledX) > maxX:
                maxX=abs(scaledX)
            if abs(scaledY) > maxY:
                maxY=abs(scaledY)

            #adds txt to template
            self.addRectangle(pName, scaledX, scaledY, particleResolution, counductorMaterial)
            nameCtr = nameCtr + 1

        #group created particles
        nameStr = ""
        for pn in nameList:
            if nameStr == "":
                nameStr = pn
            else:
                nameStr = nameStr + "," + pn

        #needs format: "particle1,particle2,particle3,particle4,particle5,...""
        #in the future, let the function call handle the formatting
        self.groupParticles(nameStr)

        #needs format: "particle1","particle2","particle3",....
        #in the future, let the function call handle the formatting
                #group created particles
        nameStr = ""
        for pn in nameList:
            pn = "\"" + pn + "\""
            if nameStr == "":
                nameStr = pn
            else:
                nameStr = nameStr + "," + pn

        self.addFiniteBoundaryParticles(nameStr)

        newGroundLength = 2.1*max(maxX+particleResolution, maxY+particleResolution)
        self.changeProjectParameter(paramName="$ground_plane", paramVal=newGroundLength)
 
            

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
    AT.addOpenExistingProjectBase()#fullPath="C:/Users/LCLin/Desktop//GeneratedHFSSProject.aedt")
    AT.deleteParticleGroup()
    AT.resizeGroundplane(newL=60)

    template = AT.getTemplateScript()
    #print(template)
    noErrors = fIO.writeOut("C:/Users/LCLin/Desktop/test-edit-probe-patch-script.py", template)
    print(noErrors)


    #TODO remove the simulation text at the end


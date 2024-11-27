##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/templateGen_ParamEdit.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os.path
import re

class ParamEditTemplate:
    def __init__(self):
        self.templateTxt = []
        self.templateFile = ""
        #file path for templates and reports
        self.templateBaseDir = os.path.join('src','simulation_integrator','ANSYS','code_templates')
        self.calculatorTemplatesDir = os.path.join(self.templateBaseDir, 'calculator-designs')
        
    def getTemplateScript(self):
        return self.templateTxt
    
    def setTemplateScript(self, t):
        self.templateTxt = t
    
    def clearTemplateScript(self):
        self.templateTxt = []

    def deleteAndClearReports(self):
        # self.templateTxt.append("oDesign.DeleteFullVariation(\"All\", False)")
        # self.templateTxt.append("\n")
        self.templateTxt.append("oModule.DeleteAllReports()")
        self.templateTxt.append("\n")

    def deleteParticleGroup(self): #specific use case - keep for debug until Genetic Alg moved
        #make more general based on naming conventions
        tmpStr = "oEditor.Delete([\"NAME:Selections\", \n " +\
             "\"Selections:=\"		, \"particle_Group\"])\n"
        self.templateTxt.append(tmpStr)

    def addSaveProject(self):
        tmpStr = "oProject.Save()\n"
        self.templateTxt.append(tmpStr)

    def updateProjectParametersWithList(self, paramList):
        #takes in array of format [[param, val, unit],[param, val, unit],[param, val, unit]....]
        # array is SINGLE iteration of changes. loop through all
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-base.txt
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-edit-end.txt
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-edit-middle.txt        
        filepath = os.path.join(self.templateBaseDir, 'parameter', 'parameter-base.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_ParamEdit.py. path error to parameter-base.txt template. check relative paths")
            print("attempted filepath: ", filepath)        
        endFile = os.path.join(self.templateBaseDir, 'parameter', 'parameter-edit-end.txt')
        if os.path.isfile(endFile) == False:
            print("ERROR: templateGen_ParamEdit.py. path error to parameter-edit-end.txt template. check relative paths")
            print("attempted filepath: ", endFile)
        startFile = os.path.join(self.templateBaseDir, 'parameter', 'parameter-edit-middle.txt')
        if os.path.isfile(startFile) == False:
            print("ERROR: templateGen_ParamEdit.py. path error to parameter-edit-middle.txt template. check relative paths")
            print("attempted filepath: ", startFile)


        paramTemplate = []
        startTemplate = []
        endTemplate = []
        with open(startFile) as f:
            for line in f.readlines():
                startTemplate.append(line)

        with open(endFile) as f:
            for line in f.readlines():
                endTemplate.append(line)

        paramTemplate = []
        # take care of var set up first
        for pn in paramList:
            paramName = pn[0]
            paramVal = pn[1]
            paramUnit = pn[2]
            if pn is not paramList[-1]: #not last
                for line in startTemplate:
                    if re.search('INSERT_PARAM_NAME', line):
                        line = re.sub('INSERT_PARAM_NAME', paramName, line)
                    elif re.search('INSERT_PARAM_VALUE', line):
                        li = str(paramVal) + " " + str(paramUnit)
                        line = re.sub('INSERT_PARAM_VALUE', li, line)  
                    paramTemplate.append(line) 
            else:
                for line in endTemplate:
                    if re.search('INSERT_PARAM_NAME', line):
                        line = re.sub('INSERT_PARAM_NAME', paramName, line)
                    elif re.search('INSERT_PARAM_VALUE', line):
                        li = str(paramVal) + " " + str(paramUnit)
                        line = re.sub('INSERT_PARAM_VALUE', li, line)  
                    paramTemplate.append(line)  
        
        #read in the base format
        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_PROPERTY_CHANGES', line):
                    line = re.sub('INSERT_PROPERTY_CHANGES', "", line)
                    for l in paramTemplate: #cant append whole array so loop
                        self.templateTxt.append(l)
                self.templateTxt.append(line)


    ########################################################
    # Port adjustment
    # NOTE: not needed for all designs. 
    # used by default with calculator templates
    ########################################################

    def deletePort(self, portID):
        tmpStr= "oModule = oDesign.GetModule(\"BoundarySetup\")\n" +\
            "oModule.DeleteBoundaries([\""+ str(portID)+ "\"])\n"
        return tmpStr

    def getModalPortText(self, startX, startY, startZ, stopX, stopY, stopZ, units):
        tmpStr=""
        filepath = os.path.join(self.calculatorTemplatesDir,'ports', "modal_port.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to modal_port.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                if re.search('INSERT_START_X', line):
                    li = str(startX) + " " + str(units)
                    line = re.sub('INSERT_START_X', li, line)
                    if re.search('INSERT_START_Y', line):
                        li = str(startY) + " " + str(units)
                        line = re.sub('INSERT_START_Y', li, line)  
                    if re.search('INSERT_START_Z', line):
                        li = str(startZ) + " " + str(units)
                        line = re.sub('INSERT_START_Z', li, line)  
                elif re.search('INSERT_STOP_X', line):
                    li = str(stopX) + " " + str(units)
                    line = re.sub('INSERT_STOP_X', li, line)  
                    if re.search('INSERT_STOP_Y', line):
                        li = str(stopY) + " " + str(units)
                        line = re.sub('INSERT_STOP_Y', li, line)  
                    if re.search('INSERT_STOP_Z', line):
                        li = str(stopZ) + " " + str(units)
                        line = re.sub('INSERT_STOP_Z', li, line)  
                tmpStr = tmpStr + line
        return tmpStr

    def getTerminalPortText(self):
        tmpStr=""

    def getAutoPortText(self):
        tmpStr=""
        filepath = os.path.join(self.calculatorTemplatesDir, 'ports',"auto_port.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to auto_port.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            for line in f.readlines():
                tmpStr = tmpStr + line
        return tmpStr

    def updatePortLocation(self, startX, startY, startZ, stopX, stopY, stopZ, units="mm", networkType="modal", portID=1):
        
        #delete current port
        li = self.deletePort(portID)
        self.templateTxt.append(li)

        #add new port setup
        if networkType == "modal":
            li = self.getModalPortText(startX, startY, startZ, stopX, stopY, stopZ, units)                       
        elif networkType == "terminal": 
            li = self.getTerminalPortText()    
        else: #auto
            li = self.getAutoPortText()  

        self.templateTxt.append(li)

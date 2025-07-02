##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/design_template_integration/halfWaveDipoleScriptGenerator.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import re

def halfWaveDipoleScriptGenerator(parent, l, r, fg, cMaterial="copper", units="mm", networkType="modal"):
            #src\simulation_integrator\ANSYS\code_templates\patch_strip-fed.txt
    filepath = os.path.join(parent.calculatorTemplatesDir, 'dipole.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to dipole.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return


    saveProjectAs = parent.getFullProjectPath()
    projectPath = repr(saveProjectAs)  #full save location
    lVal =  str(l) + " " + str(units)
    fgVal = str(fg) + " " + str(units)
    rVal = str(r) + " " + str(units)

    counductorMaterial = str(cMaterial) 
    conductorMaterialBoundary = str(cMaterial) 

    #ints
    startX = 0 
    startY = 0
    startZ = float(fg)/2 # +feedgap/2
    stopX = 0 
    stopY = 0
    stopZ = -float(fg)/2

    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                # print(li)
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_LENGTH_VALUE', line):
                li = lVal
                line = re.sub('INSERT_LENGTH_VALUE', li, line)  
            elif re.search('INSERT_FEEDGAP_VALUE', line):
                li = fgVal
                line = re.sub('INSERT_FEEDGAP_VALUE', li, line)              
            elif re.search('INSERT_RADIUS_VALUE', line):
                li = rVal
                line = re.sub('INSERT_RADIUS_VALUE', li, line)             
            elif re.search('INSERT_CONDUCTOR_MATERIAL', line):
                li = counductorMaterial
                line = re.sub('INSERT_CONDUCTOR_MATERIAL', li, line)
            elif re.search('INSERT_CONDUCTOR_BOUNDARY_MATERIAL', line):
                li = conductorMaterialBoundary
                line = re.sub('INSERT_CONDUCTOR_BOUNDARY_MATERIAL', li, line)
            elif re.search('INSERT_PORT_SETUP', line):
                if networkType == "modal":
                    li = parent.getModalPortText(startX, startY, startZ, stopX, stopY, stopZ, units)                   
                elif networkType == "terminal": 
                    li = parent.getTerminalPortText()    
                else: #auto
                    li = parent.getAutoPortText()   
                line = re.sub('INSERT_PORT_SETUP', li, line)       
            elif re.search('INSERT_SOLUTION_TYPE', line):
                if networkType == "modal":
                    li = parent.getModalSolutionText()                    
                else: #terminal
                    li = parent.getTerminalSolutionText()                    
                line = re.sub('INSERT_SOLUTION_TYPE', li, line) 
            elif re.search('INSERT_DESIGN_NETWORK_TYPE', line):
                if networkType == "modal":
                    li = parent.getModalInsertDesign()                    
                else: #terminal
                    li = parent.getTerminalInsertDesign()
                line = re.sub('INSERT_DESIGN_NETWORK_TYPE', li, line)                                        
            parent.templateTxt.append(line)
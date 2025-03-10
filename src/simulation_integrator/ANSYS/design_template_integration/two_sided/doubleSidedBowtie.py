##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/design_template_integration/dualBandSerpentineScriptGenerator.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import re

def doubleSidedBowtieScriptGenerator(parent, w2, w3, w4, w5, w6, w7, w8, l2, l3, l4, l5, l6, l7,
                                         groundLength, groundWidth, substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):

    #src\simulation_integrator\ANSYS\code_templates\double-sided-bowtie.txt
    filepath = os.path.join(parent.replicatorTemplatesDir, 'double-sided-rounded-bowtie.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to double-sided-bowtie.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    w2Val = str(w2) + " " + str(units)
    w3Val = str(w3) + " " + str(units)
    w4Val = str(w4) + " " + str(units)
    w5Val = str(w5) + " " + str(units)
    w6Val = str(w6) + " " + str(units)
    w7Val = str(w7) + " " + str(units)
    w8Val = str(w8) + " " + str(units)
    l2Val = str(l2) + " " + str(units)
    l3Val = str(l3) + " " + str(units)
    l4Val = str(l4) + " " + str(units)
    l5Val = str(l5) + " " + str(units)
    l6Val = str(l6) + " " + str(units)
    l7Val = str(l7) + " " + str(units)
    groundLengthVal = str(groundLength) + " " + str(units)
    groundWidthVal = str(groundWidth) + " " + str(units)
    substrateHeightVal = str(substrateHeight) + " " + str(units)
    substrateLengthVal = str(substrateLength) + " " + str(units)
    substrateWidthVal = str(substrateWidth) + " " + str(units)

    groundPlaneMaterial = str(gpMaterial)
    substrateMaterial = str(sMaterial)
    counductorMaterial = str(cMaterial) 
    conductorMaterialBoundary = str(cMaterial) 

    #floats
    startX = float(substrateLength/2)  #$sub_length/2 
    startY = float(0) 
    startZ = float(-substrateHeight) 
    stopX = float(substrateLength/2)  #$sub_length/2 
    stopY = float(0) 
    stopZ = float(0) 
    # FORMAT
    # "Start:="		, ["18mm","-6.13480336465337e-17mm","-1.25mm"],
    # "End:="			, ["18mm","-3.46944695195361e-16mm","1.39332989590457e-16mm"]


    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                # print(li)
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_W2_VALUE', line):
                li = w2Val
                line = re.sub('INSERT_W2_VALUE', li, line)  
            elif re.search('INSERT_W3_VALUE', line):
                li = w3Val
                line = re.sub('INSERT_W3_VALUE', li, line)  
            elif re.search('INSERT_W4_VALUE', line):
                li = w4Val
                line = re.sub('INSERT_W4_VALUE', li, line)              
            elif re.search('INSERT_W5_VALUE', line):
                li = w5Val
                line = re.sub('INSERT_W5_VALUE', li, line)             
            elif re.search('INSERT_W6_VALUE', line):
                li = w6Val
                line = re.sub('INSERT_W6_VALUE', li, line)    
            elif re.search('INSERT_W7_VALUE', line):
                li = w7Val
                line = re.sub('INSERT_W7_VALUE', li, line)             
            elif re.search('INSERT_W8_VALUE', line):
                li = w8Val
                line = re.sub('INSERT_W8_VALUE', li, line)             
            elif re.search('INSERT_L2_VALUE', line):
                li = l2Val
                line = re.sub('INSERT_L2_VALUE', li, line)
            elif re.search('INSERT_L3_VALUE', line):
                li = l3Val
                line = re.sub('INSERT_L3_VALUE', li, line)              
            elif re.search('INSERT_L4_VALUE', line):
                li = l4Val
                line = re.sub('INSERT_L4_VALUE', li, line)             
            elif re.search('INSERT_L5_VALUE', line):
                li = l5Val
                line = re.sub('INSERT_L5_VALUE', li, line)    
            elif re.search('INSERT_L6_VALUE', line):
                li = l6Val
                line = re.sub('INSERT_L6_VALUE', li, line)             
            elif re.search('INSERT_L7_VALUE', line):
                li = l7Val
                line = re.sub('INSERT_L7_VALUE', li, line)             
            elif re.search('INSERT_GP_LENGTH_VALUE', line):
                li = groundLengthVal
                line = re.sub('INSERT_GP_LENGTH_VALUE', li, line)  
            elif re.search('INSERT_GP_WIDTH_VALUE', line):
                li = groundWidthVal
                line = re.sub('INSERT_GP_WIDTH_VALUE', li, line)    
            elif re.search('INSERT_SUB_HEIGHT_VALUE', line):
                li = substrateHeightVal
                line = re.sub('INSERT_SUB_HEIGHT_VALUE', li, line)             
            elif re.search('INSERT_SUB_LENGTH_VALUE', line):
                li = substrateLengthVal
                line = re.sub('INSERT_SUB_LENGTH_VALUE', li, line)             
            elif re.search('INSERT_SUB_WIDTH_VALUE', line):
                li = substrateWidthVal
                line = re.sub('INSERT_SUB_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_GROUND_PLANE_MATERIAL', line):
                li = groundPlaneMaterial
                line = re.sub('INSERT_GROUND_PLANE_MATERIAL', li, line)             
            elif re.search('INSERT_SUBSTRATE_MATERIAL', line):
                li = substrateMaterial
                line = re.sub('INSERT_SUBSTRATE_MATERIAL', li, line)                        
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


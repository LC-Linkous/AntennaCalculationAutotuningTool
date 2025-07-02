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

def twoArmSquareSpiralScriptGenerator(parent, initLength, initWidth, width, x0, y0, spacing, 
                                   #groundLength, groundWidth, 
                                   substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):

    filepath = os.path.join(parent.replicatorTemplatesDir, 'two-arm-square-spiral.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to two-arm-square-spiral.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    
    saveProjectAs = parent.getFullProjectPath()
    projectPath = repr(saveProjectAs)  #full save location
    initLengthVal = str(initLength) + " " + str(units)
    initWidthVal = str(initWidth) + " " + str(units)
    widthVal = str(width) + " " + str(units)
    x0Val = str(x0) + " " + str(units)
    y0Val = str(y0) + " " + str(units)
    spacingVal = str(spacing) + " " + str(units)
    # groundLengthVal = str(groundLength) + " " + str(units) #template uses the sub size, but these vars do exist
    # groundWidthVal = str(groundWidth) + " " + str(units)
    substrateHeightVal = str(substrateHeight) + " " + str(units)
    substrateLengthVal = str(substrateLength) + " " + str(units)
    substrateWidthVal = str(substrateWidth) + " " + str(units)

    groundPlaneMaterial = str(gpMaterial)
    counductorMaterial = str(cMaterial) 
    substrateMaterial = str(sMaterial)
    conductorMaterialBoundary = str(cMaterial) 

    #ints

    startX = float(x0)  + (0.85/2) # $fx  +$pinRad  (0.85/2)
    startY = float(y0)
    startZ = -3 - float(substrateHeight)  # -$PinH - $depth
    stopX =  float(x0) + (4.19/2)  #$fx + $PTFERad 
    stopY = float(y0)  
    stopZ =  -3 - float(substrateHeight)  # -$PinH -$depth

    # "Start:="		, ["0.4mm","0mm","-4.6mm"],
    # "End:="			, ["2mm","0mm","-4.6mm"]



    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_INIT_LENGTH_VALUE', line):
                li = initLengthVal
                line = re.sub('INSERT_INIT_LENGTH_VALUE', li, line)  
            elif re.search('INSERT_INIT_WIDTH_VALUE', line):
                li = initWidthVal
                line = re.sub('INSERT_INIT_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_STRIP_WIDTH_VALUE', line):
                li = widthVal
                line = re.sub('INSERT_STRIP_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_X0_VALUE', line):
                li = x0Val
                line = re.sub('INSERT_X0_VALUE', li, line)              
            elif re.search('INSERT_Y0_VALUE', line):
                li = y0Val
                line = re.sub('INSERT_Y0_VALUE', li, line)  
            elif re.search('INSERT_SPACING_VALUE', line):
                li = spacingVal
                line = re.sub('INSERT_SPACING_VALUE', li, line)  
            # elif re.search('INSERT_GP_LENGTH_VALUE', line):
            #     li = groundLengthVal
            #     line = re.sub('INSERT_GP_LENGTH_VALUE', li, line)              
            # elif re.search('INSERT_GP_WIDTH_VALUE', line):
            #     li = groundWidthVal
            #     line = re.sub('INSERT_GP_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_SUBSTRATE_HEIGHT_VALUE', line):
                li = substrateHeightVal
                line = re.sub('INSERT_SUBSTRATE_HEIGHT_VALUE', li, line)   
            elif re.search('INSERT_SUBSTRATE_LENGTH_VALUE', line):
                li = substrateLengthVal
                line = re.sub('INSERT_SUBSTRATE_LENGTH_VALUE', li, line)   
            elif re.search('INSERT_SUBSTRATE_WIDTH_VALUE', line):
                li = substrateWidthVal
                line = re.sub('INSERT_SUBSTRATE_WIDTH_VALUE', li, line)  



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

##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/design_template_integration/patchStripFedScriptGenerator.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import re

#def patchStripFedScriptGenerator(parent, w, l, d, sw, x0, y0, g, gp, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy", units="mm", networkType="modal"):
def patchStripFedScriptGenerator(parent, w, l, sw, x0, y0, g, 
                                #  groundLength, groundWidth, 
                                 substrateHeight, substrateLength, substrateWidth, cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy", units="mm", networkType="modal"):
      
    #src\simulation_integrator\ANSYS\code_templates\patch_strip-fed.txt
    filepath = os.path.join(parent.calculatorTemplatesDir, 'patch_strip-fed.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: patchStripFedScriptGenerator.py. path error to patch_strip-fed.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    wVal =  str(w) + " " + str(units)
    lVal = str(l) + " " + str(units)
    #dVal = str(substrateHeight) + " " + str(units)
    swVal = str(sw) + " " + str(units)
    x0Val = str(x0) + " " + str(units)
    y0Val = str(y0) + " " + str(units)
    gapVal = str(g) + " " + str(units)
    #gpVal = str(groundLength) + " " + str(units)
    # groundLengthVal = str(groundLength) + " " + str(units)
    # groundWidthVal = str(groundWidth) + " " + str(units)
    substrateHeightVal = str(substrateHeight) + " " + str(units)
    substrateLengthVal = str(substrateLength) + " " + str(units)
    substrateWidthVal = str(substrateWidth) + " " + str(units)

    groundPlaneMaterial = str(gpMaterial)
    substrateMaterial = str(sMaterial)
    counductorMaterial = str(cMaterial) 
    conductorMaterialBoundary = str(cMaterial) 

    # floats. This HAS to be NUMERIC, not parameterized
    startX = 0 #???
    startY = float(substrateLength)/2 #$ground_plane/2
    startZ = -float(substrateHeight) # -$depth
    stopX = 0 #surface
    stopY = float(substrateLength)/2 #$ground_plane/2
    stopZ = 0 #???
    #modal port - leave for debug until we know this works across configs
    # "Start:="		, ["-3.46944695195361e-16mm","29.4423612179361mm","-1.6mm"],
    # "End:="			, ["0mm","29.4423612179361mm","-2.80962294113563e-16mm"]

    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                # print(li)
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_WIDTH_VALUE', line):
                li = wVal
                line = re.sub('INSERT_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_LENGTH_VALUE', line):
                li = lVal
                line = re.sub('INSERT_LENGTH_VALUE', li, line)  
            # elif re.search('INSERT_DEPTH_VALUE', line):
            #     li = dVal
            #     line = re.sub('INSERT_DEPTH_VALUE', li, line)              
            elif re.search('INSERT_STRIP_WIDTH_VALUE', line):
                li = swVal
                line = re.sub('INSERT_STRIP_WIDTH_VALUE', li, line)             
            elif re.search('INSERT_X0_VALUE', line):
                li = x0Val
                line = re.sub('INSERT_X0_VALUE', li, line)    
            elif re.search('INSERT_Y0_VALUE', line):
                li = y0Val
                line = re.sub('INSERT_Y0_VALUE', li, line)             
            elif re.search('INSERT_GAP_VALUE', line):
                li = gapVal
                line = re.sub('INSERT_GAP_VALUE', li, line)             
            # elif re.search('INSERT_GROUND_PLANE_VALUE', line):
            #     li = gpVal
            #     line = re.sub('INSERT_GROUND_PLANE_VALUE', li, line)   
            
            # elif re.search('INSERT_GROUND_LENGTH_VALUE', line):
            #     li = groundLengthVal
            #     line = re.sub('INSERT_GROUND_LENGTH_VALUE', li, line)   
            # elif re.search('INSERT_GROUND_WIDTH_VALUE', line):
            #     li = groundWidthVal
            #     line = re.sub('INSERT_GROUND_WIDTH_VALUE', li, line)   
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


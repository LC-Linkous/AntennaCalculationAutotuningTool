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

def squareLoopScriptGenerator(parent, l, w, feedWidth, gapDist,
                                  #groundLength, groundWidth, 
                                  substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):

    filepath = os.path.join(parent.replicatorTemplatesDir, 'square-loop.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to square-loop.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    lVal = str(l) + " " + str(units)
    wVal = str(w) + " " + str(units)
    feedWidthVal = str(feedWidth) + " " + str(units)
    gapDistVal = str(gapDist) + " " + str(units)
    # groundLengthVal = str(groundLength) + " " + str(units)
    # groundWidthVal = str(groundWidth) + " " + str(units)
    substrateHeightVal = str(substrateHeight) + " " + str(units)
    substrateLengthVal = str(substrateLength) + " " + str(units)
    substrateWidthVal = str(substrateWidth) + " " + str(units)


    groundPlaneMaterial = str(gpMaterial)
    counductorMaterial = str(cMaterial) 
    substrateMaterial = str(sMaterial)
    conductorMaterialBoundary = str(cMaterial) 

    #floats
    startX = float(gapDist/2)  #$gap_dist/2
    startY = -1.0*float(l/2)+float(feedWidth/2) #-$length/2 + $feed_width/2
    startZ = float(0) 
    stopX =  -float(gapDist/2) #$gap_dist/2
    stopY = -1.0*float(l/2)+float(feedWidth/2) #-$length/2 - $feed_width/2
    stopZ = float(0) 
    # FORMAT:
    # "Start:="		, ["0.75mm","-6mm","0mm"],
    # "End:="			, ["-0.75mm","-6mm","0mm"]


    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_LENGTH_VALUE', line):
                li = lVal
                line = re.sub('INSERT_LENGTH_VALUE', li, line)  
            elif re.search('INSERT_WIDTH_VALUE', line):
                li = wVal
                line = re.sub('INSERT_WIDTH_VALUE', li, line)  
            elif re.search('INSERT_FEED_WIDTH_VALUE', line):
                li = feedWidthVal
                line = re.sub('INSERT_FEED_WIDTH_VALUE', li, line)              
            elif re.search('INSERT_GAP_DIST_VALUE', line):
                li = gapDistVal
                line = re.sub('INSERT_GAP_DIST_VALUE', li, line)  
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

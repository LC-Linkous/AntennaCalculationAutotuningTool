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

# def dualBandSerpentineScriptGenerator(parent, fy, px, py, d, lp, lsub, wp, wsub,
#                                                 ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4, lc,
#                                                 cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
def dualBandSerpentineScriptGenerator(parent, fy, px, py, lp, wp,
                                        ps1, ls1, ws1, ps2, ls2, ws2,
                                        ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                        #groundLength, groundWidth, 
                                        substrateHeight, substrateLength, substrateWidth,
                                        cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):

           
    filepath = os.path.join(parent.replicatorTemplatesDir, 'implantable-dual-band-serpentine.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to implantable-dual-band-serpentine.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    fyVal = str(fy) + " " + str(units)
    pxVal = str(px) + " " + str(units)
    pyVal = str(py) + " " + str(units)
    #dVal = str(substrateHeight) + " " + str(units)
    LpVal = str(lp) + " " + str(units)
    #LsubVal = str(substrateLength) + " " + str(units)
    WpVal = str(wp) + " " + str(units)
    #WsubVal = str(substrateWidth) + " " + str(units)
    Ps1Val = str(ps1) + " " + str(units)
    Ls1Val = str(ls1) + " " + str(units)
    Ws1Val = str(ws1) + " " + str(units)
    Ps2Val = str(ps2) + " " + str(units)
    Ls2Val = str(ls2) + " " + str(units)
    Ws2Val = str(ws2) + " " + str(units)
    Ps3Val = str(ps3) + " " + str(units)
    Ls3Val = str(ls3) + " " + str(units)
    Ws3Val = str(ws3) + " " + str(units)
    Ps4Val = str(ps4) + " " + str(units)
    Ls4Val = str(ls4) + " " + str(units)
    Ws4Val = str(ws4) + " " + str(units)
    LcVal = str(lc) + " " + str(units)

    # groundLengthVal = str(groundLength) + " " + str(units)
    # groundWidthVal = str(groundWidth) + " " + str(units)
    substrateHeightVal = str(substrateHeight) + " " + str(units)
    substrateLengthVal = str(substrateLength) + " " + str(units)
    substrateWidthVal = str(substrateWidth) + " " + str(units)

    groundPlaneMaterial = str(gpMaterial)
    counductorMaterial = str(cMaterial) 
    substrateMaterial = str(sMaterial)
    conductorMaterialBoundary = str(cMaterial) 

    #ints
    fx = ((float(ps4)-(float(ws4)/2))+(float(ps3)+(float(ws3)/2)))/2

    startX = float(fx)  # $fx
    startY = float(fy) + (0.85/2) # +$pinRad  (0.85/2)
    startZ = -3 - float(substrateHeight)  # -$PinH - $depth
    stopX =  float(fx) 
    stopY = float(fy) + (4.19/2)  # + $PTFERad
    stopZ =  -3 - float(substrateHeight)  # -$PinH -$depth

    # "Start:="		, ["2.35mm","-0.325mm","-4.6mm"],
    # "End:="			, ["2.35mm","-1.995mm","-4.6mm"]


    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            # elif re.search('INSERT_DEPTH_VALUE', line):
            #     li = dVal
            #     line = re.sub('INSERT_DEPTH_VALUE', li, line)  
            elif re.search('INSERT_PS1_VALUE', line):
                li = Ps1Val
                line = re.sub('INSERT_PS1_VALUE', li, line)  
            elif re.search('INSERT_WS1_VALUE', line):
                li = Ws1Val
                line = re.sub('INSERT_WS1_VALUE', li, line)              
            elif re.search('INSERT_LS1_VALUE', line):
                li = Ls1Val
                line = re.sub('INSERT_LS1_VALUE', li, line)  
            elif re.search('INSERT_PS2_VALUE', line):
                li = Ps2Val
                line = re.sub('INSERT_PS2_VALUE', li, line)  
            elif re.search('INSERT_WS2_VALUE', line):
                li = Ws2Val
                line = re.sub('INSERT_WS2_VALUE', li, line)              
            elif re.search('INSERT_LS2_VALUE', line):
                li = Ls2Val
                line = re.sub('INSERT_LS2_VALUE', li, line)  
            elif re.search('INSERT_PS3_VALUE', line):
                li = Ps3Val
                line = re.sub('INSERT_PS3_VALUE', li, line)  
            elif re.search('INSERT_WS3_VALUE', line):
                li = Ws3Val
                line = re.sub('INSERT_WS3_VALUE', li, line)              
            elif re.search('INSERT_LS3_VALUE', line):
                li = Ls3Val
                line = re.sub('INSERT_LS3_VALUE', li, line)  
            elif re.search('INSERT_PS4_VALUE', line):
                li = Ps4Val
                line = re.sub('INSERT_PS4_VALUE', li, line)  
            elif re.search('INSERT_WS4_VALUE', line):
                li = Ws4Val
                line = re.sub('INSERT_WS4_VALUE', li, line)              
            elif re.search('INSERT_LS4_VALUE', line):
                li = Ls4Val
                line = re.sub('INSERT_LS4_VALUE', li, line)  
            elif re.search('INSERT_FY_VALUE', line):
                li = fyVal
                line = re.sub('INSERT_FY_VALUE', li, line)              
            elif re.search('INSERT_PX_VALUE', line):
                li = pxVal
                line = re.sub('INSERT_PX_VALUE', li, line)     
            elif re.search('INSERT_PY_VALUE', line):
                li = pyVal
                line = re.sub('INSERT_PY_VALUE', li, line)              
            elif re.search('INSERT_LP_VALUE', line):
                li = LpVal
                line = re.sub('INSERT_LP_VALUE', li, line)   
            elif re.search('INSERT_WP_VALUE', line):
                li = WpVal
                line = re.sub('INSERT_WP_VALUE', li, line)     
            # elif re.search('INSERT_LSUB_VALUE', line):
            #     li = LsubVal
            #     line = re.sub('INSERT_LSUB_VALUE', li, line)              
            # elif re.search('INSERT_WSUB_VALUE', line):
            #     li = WsubVal
            #     line = re.sub('INSERT_WSUB_VALUE', li, line)   
            
            elif re.search('INSERT_LC_VALUE', line):
                li = LcVal
                line = re.sub('INSERT_LC_VALUE', li, line)


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

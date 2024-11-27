##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/design_template_integration/SlottedRectangularPatchScriptGenerator.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import re

def slottedRectangularPatchScriptGenerator(parent,Lr,Lh,Lv,l,Lg,fx,Pr,Wr,Wu,w,Wg, fy, d, cMaterial="copper", gpMaterial="copper",sMaterial="FR4_epoxy",units="mm", networkType="modal"):
    filepath = os.path.join(parent.replicatorTemplatesDir, 'slotted-patch.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to slotted-patch.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    LrVal = str(Lr) + " " + str(units)
    LhVal = str(Lh) + " " + str(units)
    LvVal = str(Lv) + " " + str(units)
    lVal = str(l) + " " + str(units)
    LgVal = str(Lg) + " " + str(units)
    fxVal = str(fx) + " " + str(units)
    PrVal = str(Pr) + " " + str(units)
    WrVal = str(Wr) + " " + str(units)
    WuVal = str(Wu) + " " + str(units)
    wVal = str(w) + " " + str(units)
    WgVal = str(Wg) + " " + str(units)
    fyVal = str(fy) + " " + str(units)
    dVal = str(d) + " " + str(units)



    groundPlaneMaterial = str(gpMaterial)
    counductorMaterial = str(cMaterial) 
    substrateMaterial = str(sMaterial)
    conductorMaterialBoundary = str(cMaterial) 


    #ints
    startX = float(fx)  # $fx
    startY = -float(w/2)+float(fy) + (0.85/2) # +$pinRad  (0.85/2)
    startZ = -3 - float(d)  # -$PinH - $depth
    stopX =  float(fx) 
    stopY = -float(w/2)+float(fy) + (4.19/2)  # + $PTFERad
    stopZ =  -3 - float(d)  # -$PinH -$depth

    # "Start:="		, ["22.43mm","-24.865mm","-4.6mm"],
    # "End:="			, ["22.43mm","-23.195mm","-4.6mm"]


    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_LR_VALUE', line):
                li = LrVal
                line = re.sub('INSERT_LR_VALUE', li, line)  
            elif re.search('INSERT_LH_VALUE', line):
                li = LhVal
                line = re.sub('INSERT_LH_VALUE', li, line)              
            elif re.search('INSERT_LV_VALUE', line):
                li = LvVal
                line = re.sub('INSERT_LV_VALUE', li, line)     
            elif re.search('INSERT_L_VALUE', line):
                li = lVal
                line = re.sub('INSERT_L_VALUE', li, line)  
            elif re.search('INSERT_LG_VALUE', line):
                li = LgVal
                line = re.sub('INSERT_LG_VALUE', li, line)              
            elif re.search('INSERT_FX_VALUE', line):
                li = fxVal
                line = re.sub('INSERT_FX_VALUE', li, line)     
            elif re.search('INSERT_PR_VALUE', line):
                li = PrVal
                line = re.sub('INSERT_PR_VALUE', li, line)              
            elif re.search('INSERT_WR_VALUE', line):
                li = WrVal
                line = re.sub('INSERT_WR_VALUE', li, line)   
            elif re.search('INSERT_WU_VALUE', line):
                li = WuVal
                line = re.sub('INSERT_WU_VALUE', li, line)              
            elif re.search('INSERT_W_VALUE', line):
                li = wVal
                line = re.sub('INSERT_W_VALUE', li, line)     
            elif re.search('INSERT_WG_VALUE', line):
                li = WgVal
                line = re.sub('INSERT_WG_VALUE', li, line)  
            elif re.search('INSERT_FY_VALUE', line):
                li = fyVal
                line = re.sub('INSERT_FY_VALUE', li, line)              
            elif re.search('INSERT_DEPTH_VALUE', line):
                li = dVal
                line = re.sub('INSERT_DEPTH_VALUE', li, line)     
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

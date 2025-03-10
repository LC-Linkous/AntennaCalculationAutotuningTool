##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/ANSYS/design_template_integration/EMicrostripFedScriptGenerator.py'
#   Class for ANSYS HFSS parameter manipuation template generator.
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import re

def EMicrostripFedScriptGenerator(parent, x, l, ls, lg, ps, ws, w, wg, cMaterial="copper", gpMaterial="copper", units="mm", networkType="modal"):
    filepath = os.path.join(parent.replicatorTemplatesDir, 'dual-band_E.txt')
    if os.path.isfile(filepath) == True:
        pass
    else:
        print("ERROR: templateGen_Design.py. path error to dual-band_E.txt template. check relative paths")
        print("attempted filepath: ", filepath)
        return

    projectPath = repr(parent.saveProjectAs)  #full save location
    xVal =  str(x) + " " + str(units)
    lVal = str(l) + " " + str(units)
    lsVal = str(ls) + " " + str(units)
    lgval =  str(lg) + " " + str(units) #ground plane length
    psVal = str(ps) + " " + str(units)
    wsVal = str(ws) + " " + str(units)
    wVal = str(w) + " " + str(units)
    wgVal = str(wg) + " " + str(units) #ground plane width 

    groundPlaneMaterial = str(gpMaterial)
    counductorMaterial = str(cMaterial) 
    conductorMaterialBoundary = str(cMaterial) 

    #ints
    startX = -float(x) - (4.19/2) # -$PTFERad = -2.095mm #CHECK SIGNS IN TEST
    startY = 0 # 0mm
    startZ = -3 # -$PinH
    stopX = -float(x) -(0.85/2) # -$PinRad #CHECK SIGNS IN TEST
    stopY = 0 # 0mm
    stopZ =  -3 # -$PinH

    with open(filepath) as f:
        for line in f.readlines():
            if re.search('INSERT_PROJECT_NAME', line):
                li = projectPath[1:-1]#strip extra quotes
                line = re.sub('INSERT_PROJECT_NAME', li, line)
            elif re.search('INSERT_WG_VALUE', line):
                li = wgVal
                line = re.sub('INSERT_WG_VALUE', li, line)  
            elif re.search('INSERT_LG_VALUE', line):
                li = lgval
                line = re.sub('INSERT_LG_VALUE', li, line)              
            elif re.search('INSERT_W_VALUE', line):
                li = wVal
                line = re.sub('INSERT_W_VALUE', li, line)     
            elif re.search('INSERT_L_VALUE', line):
                li = lVal
                line = re.sub('INSERT_L_VALUE', li, line)  
            elif re.search('INSERT_WS_VALUE', line):
                li = wsVal
                line = re.sub('INSERT_WS_VALUE', li, line)              
            elif re.search('INSERT_LS_VALUE', line):
                li = lsVal
                line = re.sub('INSERT_LS_VALUE', li, line)     
            elif re.search('INSERT_PS_VALUE', line):
                li = psVal
                line = re.sub('INSERT_PS_VALUE', li, line)              
            elif re.search('INSERT_X_VALUE', line):
                li = xVal
                line = re.sub('INSERT_X_VALUE', li, line)    
            elif re.search('INSERT_GROUND_PLANE_MATERIAL', line):
                li = groundPlaneMaterial
                line = re.sub('INSERT_GROUND_PLANE_MATERIAL', li, line)             
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
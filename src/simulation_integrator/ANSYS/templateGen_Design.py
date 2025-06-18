##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/HFSS/templateGen_Design.py'
#   Class for HFSS antenna template generator.
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 1, 2023
##--------------------------------------------------------------------\

from datetime import datetime
import os.path
import re
import sys 

sys.path.insert(0, './src/simulation_integrator/ANSYS/')

# split up the scrip gen code into helper functions to increase readibility with expansion
import design_template_integration.calculator.patchStripFedScriptGenerator as patch_sf_sg
import design_template_integration.calculator.patchProbeFedScriptGenerator as patch_pf_sg
import design_template_integration.calculator.halfWaveDipoleScriptGenerator as dipole_hw_sg
import design_template_integration.calculator.quarterWaveMonopoleScriptGenerator as monopole_qw_sg
import design_template_integration.planar.EMicrostripFedScriptGenerator as E_sf_sg
import design_template_integration.planar.slottedRectangularPatchScriptGenerator as patch_slotted_sg
import design_template_integration.planar.dualBandSerpentineScriptGenerator as serpentine_db_sg
import design_template_integration.planar.planarBowtie as planar_bowtie_sg
import design_template_integration.planar.twoArmSquareSpiral as two_arm_sq_spiral_sg
import design_template_integration.loop_and_coil.circularLoop as circular_loop_sg
import design_template_integration.loop_and_coil.coplanarKeyhole as coplanar_keyhole_sg
import design_template_integration.loop_and_coil.squareLoop as square_loop_sg
import design_template_integration.two_sided.doubleSidedBowtie as double_sided_bowtie_sg







sys.path.insert(0, './src/config')
import project.config.antennaCAT_config as c

class DesignTemplate:
    def __init__(self, projName, projDir):
        self.templateTxt = []
        self.projectName = projName
        self.projectPath = projDir
        self.saveProjectAs = os.path.join(self.projectPath, self.projectName)
        self.templateBaseDir = os.path.join('src','simulation_integrator','ANSYS','code_templates')
        self.calculatorTemplatesDir = os.path.join(self.templateBaseDir, 'calculator-designs')
        self.replicatorTemplatesDir = os.path.join(self.templateBaseDir, 'replication-designs')
        self.solutionTypeDir = os.path.join(self.templateBaseDir,'solution-type')

    def getEMSoftwareProjectName(self):
        return self.saveProjectAs

    def getTemplateScript(self):
        return self.templateTxt
    
    def setTemplateScript(self, s):
        self.templateTxt = s

    def clearTemplateText(self):
        #primarily for unit testing
        self.templateTxt.clear()
                
    def clearTemplateScript(self):
        self.templateTxt = []
                
    def addImportedTemplateScript(self, t):
        self.templateTxt.append(t) 

    def checkFileExists(self, filename, filepath):
        fileExists = False
        if os.path.isfile(filepath) == True:
            fileExists = True
        else:
            print("ERROR: ANSYS/templateGen_Design.py. path error to " + filename + ". check relative paths")
            print("attempted filepath: ", filepath)

        return fileExists

    def setComments(self, c):
        self.comments = c

    def addCommentsToFile(self, c=""):
        now = datetime.now()
        filepath = os.path.join(self.templateBaseDir, 'comments', 'add-comments.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: batch-test.py. path error to probe-edit-run-del.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return

        tmpTemplate = []
        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_DATE_AND_TIME', line):
                    li = str(now.strftime("%d/%m/%Y %H:%M:%S"))
                    line = re.sub('INSERT_DATE_AND_TIME', li, line)
                elif re.search('INSERT_COMMENT', line):
                    li = str(c)
                    line = re.sub('INSERT_COMMENT', li, line)  
                self.templateTxt.append(line)

    def getModalInsertDesign(self):
        tmpStr=""
        filepath = os.path.join(self.solutionTypeDir, "modal_insertDesign.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to modal_insertDesign.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpStr = tmpStr + line
        return tmpStr

    def getTerminalInsertDesign(self):
        tmpStr=""
        filepath = os.path.join(self.solutionTypeDir, "terminal_insertDesign.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to terminal_insertDesign.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpStr = tmpStr + line
        return tmpStr


    def getModalSolutionText(self):
        tmpStr=""
        filepath = os.path.join(self.solutionTypeDir, "modal_solution.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to modal_solution.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpStr = tmpStr + line
        return tmpStr

    def getTerminalSolutionText(self):
        tmpStr=""
        filepath = os.path.join(self.solutionTypeDir, "terminal_solution.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to terminal_solution.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return               
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpStr = tmpStr + line
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


    def addOpenExistingProjectBase(self, projectPath, projectName = "GeneratedHFSSProject"):
        # src\simulation_integrator\ANSYS\code_templates\open-file\open-existing-project-base.txt
        # print("templateGen_design prints")
        # print("projectPath: " + str(projectPath))
        # print("projectName: " + str(projectName))
        
        filepath = os.path.join(self.templateBaseDir, 'open-file', 'open-existing-project-base.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: batch-test.py. path error to open-existing-project-base.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return

        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_PROJECT_PATH', line):
                    li = str(projectPath) # repr(projectPath)[1:-1]#strip extra quotes. # this conversion is now done when the path is loaded in & converted to a string
                    line = re.sub('INSERT_PROJECT_PATH', li, line)
                elif re.search('INSERT_PROJECT_NAME', line):
                    li = str(projectName)
                    line = re.sub('INSERT_PROJECT_NAME', li, line)  
                self.templateTxt.append(line)

    def updateProjectParametersWithList(self, paramList):
        #takes in array of format [[param, val],[param, val],[param, val]....]
        # array is SINGLE iteration of changes. loop through all
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-base.txt
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-edit-end.txt
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-edit-middle.txt        
        filepath = os.path.join(self.templateBaseDir, 'parameter', 'parameter-base.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: batch-test.py. path error to parameter-base.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return        
        endFile = os.path.join(self.templateBaseDir, 'parameter', 'parameter-edit-end.txt')
        if os.path.isfile(endFile) == False:
            print("ERROR: batch-test.py. path error to parameter-edit-end.txt template. check relative paths")
            print("attempted filepath: ", endFile)
            return
        startFile = os.path.join(self.templateBaseDir, 'parameter', 'parameter-edit-middle.txt')
        if os.path.isfile(startFile) == False:
            print("ERROR: batch-test.py. path error to parameter-edit-middle.txt template. check relative paths")
            print("attempted filepath: ", startFile)
            return


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
            if pn is not paramList[-1]: #not last
                for line in startTemplate:
                    if re.search('INSERT_PARAM_NAME', line):
                        line = re.sub('INSERT_PARAM_NAME', paramName, line)
                    elif re.search('INSERT_PARAM_VALUE', line):
                        line = re.sub('INSERT_PARAM_VALUE', str(paramVal), line)  
                    paramTemplate.append(line) 
            else:
                for line in endTemplate:
                    if re.search('INSERT_PARAM_NAME', line):
                        line = re.sub('INSERT_PARAM_NAME', paramName, line)
                    elif re.search('INSERT_PARAM_VALUE', line):
                        line = re.sub('INSERT_PARAM_VALUE', str(paramVal), line)  
                    paramTemplate.append(line)  
        
        #read in the base format
        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_PROPERTY_CHANGES', line):
                    line = re.sub('INSERT_PROPERTY_CHANGES', "", line)
                    for l in paramTemplate: #cant append whole array so loop
                        self.templateTxt.append(l)
                self.templateTxt.append(line)
    
    def changeProjectParameter(self, pName, pVal="1"):
        #src\simulation_integrator\ANSYS\code_templates\parameter\parameter-edit-single.txt
        filepath = os.path.join(self.templateBaseDir, 'parameter', 'parameter-edit-single.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: batch-test.py. path error to parameter-edit-single.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return      
        
        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_PARAM_NAME', line):
                    li = str(pName)
                    line = re.sub('INSERT_PARAM_NAME', li, line)
                elif re.search('INSERT_PARAM_VALUE', line):
                    li = str(pVal)
                    line = re.sub('INSERT_PARAM_VALUE', li, line)  
                self.templateTxt.append(line)


    def patchStripFedScriptGenerator(self, w, l, sw, x0, y0, g,  
                                     #groundLength, groundWidth, 
                                     substrateHeight, substrateLength, substrateWidth,
                                     cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy", units="mm", networkType="modal"):
       patch_sf_sg.patchStripFedScriptGenerator(self, w, l, sw, x0, y0, g,  
                                                #groundLength, groundWidth, 
                                                substrateHeight, substrateLength, substrateWidth,
                                                 cMaterial, gpMaterial, sMaterial, units, networkType)

   
    def patchProbeFedScriptGenerator(self, w, l, x0, y0, 
                                     #groundLength, groundWidth, 
                                     substrateHeight, substrateLength, substrateWidth,
                                     cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy", units="mm", networkType="modal"):
        patch_pf_sg.patchProbeFedScriptGenerator(self, w, l, x0, y0,  
                                                 #groundLength, groundWidth, 
                                                 substrateHeight, substrateLength, substrateWidth,
                                                 cMaterial, gpMaterial, sMaterial, units, networkType)
        

    def halfWaveDipoleScriptGenerator(self, l, r, fg, 
                                      cMaterial="copper", units="mm", networkType="modal"):
        dipole_hw_sg.halfWaveDipoleScriptGenerator(self, l, r, fg, 
                                                   cMaterial, units, networkType)


    def quarterWaveMonopoleScriptGenerator(self, l, r, gp, fg, 
                                           cMaterial="copper", units="mm", networkType="modal"):
        monopole_qw_sg.quarterWaveMonopoleScriptGenerator(self, l, r, gp, fg, 
                                                          cMaterial, units, networkType)
    

    def EMicrostripFedScriptGenerator(self, x, l, ls, lg, ps, ws, w, wg, h,
                                    cMaterial="copper", gpMaterial="copper", units="mm", networkType="modal"):
        E_sf_sg.EMicrostripFedScriptGenerator(self, x, l, ls, lg, ps, ws, w, wg, h, 
                                              cMaterial, gpMaterial, units, networkType)



    def slottedRectangularPatchScriptGenerator(self, Lr,Lh,Lv,l,fx,Pr,Wr,Wu,w,fy,
                                               substrateHeight, substrateLength, substrateWidth,
                                               cMaterial="copper", gpMaterial="copper",sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        patch_slotted_sg.slottedRectangularPatchScriptGenerator(self, Lr,Lh,Lv,l,fx,Pr,Wr,Wu,w,fy,
                                               substrateHeight, substrateLength, substrateWidth,
                                                                cMaterial, gpMaterial,sMaterial,units, networkType)
  


    def dualBandSerpentineScriptGenerator(self, fy, px, py, lp, wp,
                                          ps1, ls1, ws1, ps2, ls2, ws2,
                                          ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                          #groundLength, groundWidth, 
                                          substrateHeight, substrateLength, substrateWidth,
                                          cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        serpentine_db_sg.dualBandSerpentineScriptGenerator(self, fy, px, py, lp, wp,
                                          ps1, ls1, ws1, ps2, ls2, ws2,
                                          ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                          #groundLength, groundWidth, 
                                          substrateHeight, substrateLength, substrateWidth,
                                          cMaterial, gpMaterial, sMaterial,units, networkType)        


    def coplanarKeyholeScriptGenerator(self, outerRad, innerRad, feedWidth, feedLength, gapDist,
                                       #groundLength, groundWidth, 
                                       substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        coplanar_keyhole_sg.coplanarKeyholeScriptGenerator(self, outerRad, innerRad, feedWidth, feedLength, gapDist, 
                                                        #groundLength, groundWidth,
                                                        substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units, networkType)



    def circularLoopScriptGenerator(self, outerRad, innerRad, feedWidth, inset, gapDist,
                                    #groundLength, groundWidth, 
                                    substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        
        circular_loop_sg.circularLoopScriptGenerator(self, outerRad, innerRad, feedWidth, inset, gapDist,
                                    #groundLength, groundWidth, 
                                    substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units, networkType)


    def squareLoopScriptGenerator(self, l, w, feedWidth, gapDist,
                                  #groundLength, groundWidth, 
                                  substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        square_loop_sg.squareLoopScriptGenerator(self, l, w, feedWidth, gapDist,
                                  #groundLength, groundWidth,
                                  substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units, networkType)


    def doubleSidedBowtieScriptGenerator(self, w2, w3, w4, w5, w6, w7, w8, l2, l3, l4, l5, l6, l7,
                                         groundLength, groundWidth, substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        double_sided_bowtie_sg.doubleSidedBowtieScriptGenerator(self, w2, w3, w4, w5, w6, w7, w8, l2, l3, l4, l5, l6, l7,
                                         groundLength, groundWidth, substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units, networkType)



    def planarBowtieScriptGenerator(self, l, w, feedWidth, gapDist,
                                    #groundLength, groundWidth, 
                                    substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        planar_bowtie_sg.planarBowtieScriptGenerator(self, l, w, feedWidth, gapDist,
                                    #groundLength, groundWidth, 
                                    substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units, networkType)


        
        

    def twoArmSquareSpiralScriptGenerator(self, initLength, initWidth, width, x0, y0, spacing, 
                                          #groundLength, groundWidth, 
                                          substrateHeight, substrateLength, substrateWidth,
                                   cMaterial="copper", gpMaterial="copper", sMaterial="FR4_epoxy",units="mm", networkType="modal"):
        two_arm_sq_spiral_sg.twoArmSquareSpiralScriptGenerator(self, initLength, initWidth, width, x0, y0, spacing, 
                                          #groundLength, groundWidth, 
                                          substrateHeight, substrateLength, substrateWidth,
                                                        cMaterial, gpMaterial, sMaterial, units)



if __name__ == "__main__":
    import sys
    sys.path.insert(0, './')
    import src.helper_func.fileIO_helperFuncs as fIO

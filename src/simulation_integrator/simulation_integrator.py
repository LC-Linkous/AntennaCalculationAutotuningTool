##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/simulation_integrator/simulation_integrator.py'
#   Main class for managing the EM software hooks
#   This is the 'SO'/Simulation Object referenced in code
#
#   Scripts are NOT written or read to file in this class
#
#   There are 4 functions for generating the primary scripts
#   * designTemplateGen()
#   * simulationTemplateGen()
#   * paramEditTemplateGen()
#   * reportExportTemplateGen()
#
#
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\



import sys
import os
import time

## sim integrator imports
sys.path.insert(0, './simulation_integrator/ANSYS')
from simulation_integrator.ANSYS.simIntegrator_ANSYS import SimIntegrator_ANSYS
from simulation_integrator.ANSYS.configs_materials import materials_dict

sys.path.insert(0, './simulation_integrator/COMSOL')
from simulation_integrator.COMSOL.simIntegrator_COMSOL import SimIntegrator_COMSOL
# from simulation_integrator.COMSOL.configs_materials import materials_dict

sys.path.insert(0, './simulation_integrator/CST')
from simulation_integrator.CST.simIntegrator_CST import SimIntegrator_CST
# from simulation_integrator.CST.configs_materials import materials_dict

sys.path.insert(0, './simulation_integrator/EMPIRE')
from simulation_integrator.EMPIRE.simIntegrator_EMPIRE import SimIntegrator_EMPIRE
# from simulation_integrator.EMPIRE.configs_materials import materials_dict

sys.path.insert(0, './simulation_integrator/FEKO')
from simulation_integrator.FEKO.simIntegrator_FEKO import SimIntegrator_FEKO
# from simulation_integrator.FEKO.configs_materials import materials_dict

class SimulationIntegrator():
    def __init__(self, DC, PC): #, softwareSelection, softwarePath, numLicenses):
        # class maybe created before config uploaded
        self.DC = DC
        self.PC = PC
        # class maybe created before config uploaded
        self.numSimsRunning = 0
        self.simulationSoftwarePath = None
        self.numLicense = 1
        self.p = -1 #return code for polling
        self.SO = None
        self.DT = None # design template
        self.PT = None # param edit template
        self.ST = None # simulation export template
        self.RT = None # report export template

        # self.setupSI(softwareSelection, softwarePath, numLicenses)
        
    def setSimulationSoftwareFromPC(self):
        numLicenses=1
        softwareSelection = self.PC.getSimulationSoftware()
        softwarePath = self.PC.getSimulationSoftwarePath()
        self.setSimulationSoftware(softwareSelection, softwarePath, numLicenses)

    def setSimulationSoftware(self, softwareSelection, softwarePath, numLicenses):
        #might end up being a different function/merged with something else
        self.setupSI(softwareSelection, softwarePath, numLicenses)

    def setupSI(self, softwareSelection, softwarePath, numLicenses):
        self.SO = self.selectSimIntegrator(softwareSelection, softwarePath, numLicenses)
        self.getTemplateObjects()
        dfn, sfn, pfn, rfn = self.SO.getDefaultFilePathNames() # this should  be moved
        self.PC.setDefaultScriptPaths(dfn, sfn, pfn, rfn)

    def selectSimIntegrator(self, softwareSelection, softwarePath, numLicenses=1):
        if softwareSelection == "ANSYS":
           SO = SimIntegrator_ANSYS(softwarePath, numLicenses)
        elif softwareSelection == "COMSOL":
           SO = SimIntegrator_COMSOL(softwarePath, numLicenses)
        elif softwareSelection == "CST":
           SO = SimIntegrator_CST(softwarePath, numLicenses)
        elif softwareSelection == "EMPIRE":
           SO = SimIntegrator_EMPIRE(softwarePath, numLicenses)
        elif softwareSelection == "FEKO":
           SO = SimIntegrator_FEKO(softwarePath, numLicenses)
        return SO
    

    def getTemplateObjects(self):
        self.DT = self.SO.getDesignTemplateObject()
        self.PT = self.SO.getParamEditTemplateObject()
        self.ST = self.SO.getSimulationTemplateObject()
        self.RT = self.SO.getReportEditTemplateObject()

    #def createDesignTemplate(self, projName, projDir=None):
    def createDesignTemplate(self, projDir):
        self.SO.createDesignTemplate(projDir)
    
    def createParamEditTemplate(self):
        self.SO.createParamEditTemplate()
    
    def createSimulationTemplate(self, projDir=None):
        self.SO.createSimulationTemplate(projDir)

    def createReportExportTemplate(self, projDir):
        self.SO.createReportExportTemplate(projDir)
    
    def getDefaultFilePathNames(self):
        return self.SO.getDefaultFilePathNames()
    
    def getEMSoftwareProjectName(self):
        return self.SO.getEMSoftwareProjectName()

    ##########################################################
    # General operation functions
    ###########################################################
        
    def setConfig(self):
        #TODO
        pass

    def getInstanceInformation(self):
        #TODO
        return 0

    def createInstance(self):
        #TODO
        #instance saved as ['name', '', '']
        return 0

    def terminateRunningProcess(self):
        self.SO.terminateRunningProcess()

    def runWithScript(self, pth, newSession=True):
        self.SO.runWithScript(pth, newSession)

    def runWithScriptAndExit(self, pth, newSession=True):
        self.SO.runWithScriptAndExit(pth, newSession)

    def checkRunningProcess(self):
        return self.SO.checkRunningProcess()
    
    def getSimulationRunningBool(self):
        return self.SO.getSimulationRunningBool()

    def runBatchAndExit(self, files, numLicenses, newSession=True):
        self.SO.runBatchAndExit(files, numLicenses, newSession)

    def runBatchAndWait(self, files, numLicenses, newSession=True):
        self.SO.runBatchAndWait(files, numLicenses, newSession)

    
    ##################################################
    # Adding comments
    ##################################################

    def addCommentsToDesignFile(self, t=""):
        self.DT.addCommentsToFile(t)
        self.comments = t

#############################################################
# Write scripts out to save loc with proper file extensions
############################################################

    def getExpectedScriptFileExtension(self):
        return self.SO.getExpectedScriptFileExtension()
    
    def getExpectedScriptFileType(self):
        return self.SO.getExpectedScriptFileType()
        
    def getExpectedLockFileExtension(self):
        return self.SO.getExpectedLockFileExtension()
    
    def getLockFile(self):
        return self.SO.getLockFile()

#############################################################
# Design Template Functions
# # these functions are for getting/setting design scripts
############################################################

    def setDesignTemplateScript(self, s):
        self.SO.setDesignTemplateScript(s)

    def getDesignTemplateScript(self):
        return self.SO.getDesignTemplateScript()
    
    def useOpenProjectDesignScript(self, projectPath, filename=None):
        head, tail = os.path.split(projectPath)
        filename = tail.split(".")[0]
        self.SO.clearDesignTemplateScript()
        # create the open-file design base           
        self.SO.addOpenExistingProjectBase(projectPath, filename)
        script = self.getDesignTemplateScript()
        self.DC.setDesignScript(script)

    def designTemplateGen(self):
        # all simulations will be created and saved in the antennaCAT project folder
        projPath = str(self.PC.getResultsDirectory())
        #TODO: check for more options as layers and custom shapes are added

       #design from imported script (has full script)
        if self.PC.getImportScriptBoolean() == True:
            self.SO.createDesignTemplate(projDir=projPath)#use default projName
            #TODO: let users add comments to this file
            scriptText = self.DC.getImportedScript()
            self.SO.setDesignTemplateScript(scriptText)
            self.SO.addCommentsToFile("using imported design")

        #loaded project + manually added params
        elif self.PC.getImportProjectBoolean() == True:
            projectPath = self.PC.getImportedProjectPath()
            head, tail = os.path.split(projectPath)
            filename = tail.split(".")[0]
            self.SO.createDesignTemplate(tail, head)
            # create the open-file design base           
            self.SO.addOpenExistingProjectBase(projectPath, filename)
            self.SO.addCommentsToFile("using imported project")
    
        elif self.PC.getAntennaGeneratorBoolean() == True:
            self.SO.createDesignTemplate(projDir=projPath)#use default projName
            # design from calculator
            features = self.DC.getFeatures()
            aType = features["antenna_type"][0]
            # calculated designs & replication study designs might share templates 
            #   because their inputs should look the same at this point
            if (aType == 'rectangular_patch') or (aType == 'rep_rectangular_patch'):
                w = self.DC.getParamsByName("width", unconverted=True)
                l = self.DC.getParamsByName("length", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                x0 = self.DC.getParamsByName("x0", unconverted=True)
                y0 = self.DC.getParamsByName("y0", unconverted=True)
                #gp = float(l)*2         
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)

                conductorMaterial = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")



                fType = features["feed_type"][0]
                if fType =="microstrip":
                    sw = self.DC.getParamsByName("strip_width", unconverted=True)
                    g = self.DC.getParamsByName("gap", unconverted=True)
                    self.SO.addCommentsToFile("microstrip patch antenna generated through GUI")
                    #TODO: parse this out - the lower level of the SO should 
                    # take care of the name inputs
                    self.SO.patchStripFedScriptGenerator(w, l, sw, x0, y0, g, #w, l,d, sw, x0, y0, g, gp, 
                                                         #groundLength, groundWidth,
                                                         d,substrateLength, substrateWidth,
                                                         conductorMaterial, groundMaterial,substrateMaterial,
                                                         units="mm")
                else: #probe fed template
                    self.SO.addCommentsToFile("probe fed patch antenna generated through GUI")
                    self.SO.patchProbeFedScriptGenerator(w, l, x0, y0, # w, l, x0, y0, gp,
                                                        #groundLength, groundWidth, 
                                                        d, substrateLength, substrateWidth,
                                                        cMaterial=conductorMaterial, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm")
            elif (aType == 'half_wave_dipole') or (aType == 'rep_half_wave_dipole'):
                l = self.DC.getParamsByName("length", unconverted=True)
                rad = self.DC.getParamsByName('conductor_radius', unconverted=True)
                fg = self.DC.getParamsByName('feed_gap', unconverted=True)
                conductorName = self.DC.getFeaturesByName("conductor_material")
                self.SO.halfWaveDipoleScriptGenerator(l, rad, fg, cMaterial=conductorName, units="mm")
                

            elif (aType == 'quarter_wave_monopole') or (aType == 'rep_quarter_wave_monopole'):
                l = self.DC.getParamsByName("length", unconverted=True)
                rad = self.DC.getParamsByName('conductor_radius', unconverted=True)
                gp = self.DC.getParamsByName('ground_plane_radius', unconverted=True)
                fg = self.DC.getParamsByName('feed_gap', unconverted=True)
                conductorName = self.DC.getFeaturesByName("conductor_material")
                self.SO.quarterWaveMonopoleScriptGenerator(l, rad, gp, fg, cMaterial=conductorName, units="mm")

            elif aType == 'rep_E':
                x = self.DC.getParamsByName("X", unconverted=True)
                l = self.DC.getParamsByName("L", unconverted=True)
                ls = self.DC.getParamsByName("Ls", unconverted=True)
                lg = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                ps = self.DC.getParamsByName("Ps", unconverted=True)
                ws = self.DC.getParamsByName("Ws", unconverted=True)
                w = self.DC.getParamsByName("W", unconverted=True)
                wg = self.DC.getParamsByName("ground_plane_width", unconverted=True) #does not have substrate
                h = self.DC.getParamsByName("ground_plane_dist", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                #no substrate
                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")


                self.SO.EMicrostripFedScriptGenerator(x, l, ls, lg, ps, ws, w, wg, h,
                                                      cMaterial=conductorName, gpMaterial=groundMaterial, units="mm")

            elif aType == 'rep_slotted_r_patch':
                Lr = self.DC.getParamsByName("Lr", unconverted=True)
                Lh = self.DC.getParamsByName("Lh", unconverted=True)
                Lv = self.DC.getParamsByName("Lv", unconverted=True)
                l = self.DC.getParamsByName("L", unconverted=True)
                Lg= self.DC.getParamsByName("substrate_length", unconverted=True)
                fx = self.DC.getParamsByName("fx", unconverted=True)
                Pr = self.DC.getParamsByName("Pr", unconverted=True)
                Wr = self.DC.getParamsByName("Wr", unconverted=True)
                Wu = self.DC.getParamsByName("Wu", unconverted=True)
                w = self.DC.getParamsByName("W", unconverted=True)
                Wg = self.DC.getParamsByName("substrate_width", unconverted=True)
                fy = self.DC.getParamsByName("fy", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                
                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                
                self.SO.slottedRectangularPatchScriptGenerator(Lr,Lh,Lv,l,fx,Pr,Wr,Wu,w,fy, # Lr,Lh,Lv,l,Lg,fx,Pr,Wr,Wu,w,Wg,fy, d,
                                                               substrateHeight=d,substrateLength=Lg, substrateWidth=Wg,
                                                               cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                               units="mm")

            elif aType == 'rep_db_serpentine':                    
                lp = self.DC.getParamsByName("Lp", unconverted=True)
                lsub = self.DC.getParamsByName("substrate_length", unconverted=True)
                wp = self.DC.getParamsByName("Wp", unconverted=True)
                wsub = self.DC.getParamsByName("substrate_width", unconverted=True)
                ps1 = self.DC.getParamsByName("Ps1", unconverted=True)
                ls1 = self.DC.getParamsByName("Ls1", unconverted=True)
                ws1 = self.DC.getParamsByName("Ws1", unconverted=True)
                ps2 = self.DC.getParamsByName("Ps2", unconverted=True)
                ls2 = self.DC.getParamsByName("Ls2", unconverted=True)
                ws2 = self.DC.getParamsByName("Ws2", unconverted=True)
                ps3 = self.DC.getParamsByName("Ps3", unconverted=True)
                ls3 = self.DC.getParamsByName("Ls3", unconverted=True)
                ws3 = self.DC.getParamsByName("Ws3", unconverted=True)
                ps4 = self.DC.getParamsByName("Ps4", unconverted=True)
                ls4 = self.DC.getParamsByName("Ls4", unconverted=True)
                ws4 = self.DC.getParamsByName("Ws4", unconverted=True)
                lc = self.DC.getParamsByName("Lc", unconverted=True)
                fy = self.DC.getParamsByName("Fy", unconverted=True)
                px = self.DC.getParamsByName("Px", unconverted=True)
                py = self.DC.getParamsByName("Py", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                
                self.SO.dualBandSerpentineScriptGenerator(fy, px, py, lp, wp, #fy, px, py, d, lp, lsub, wp, wsub,
                                                        ps1, ls1, ws1, ps2, ls2, ws2,
                                                        ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                                        #groundLength, groundWidth, 
                                                        substrateHeight=d, substrateLength=lsub, substrateWidth=wsub,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm")

            elif aType == 'rep_coplanar_keyhole':                    
                outerRad = self.DC.getParamsByName("outer_radius", unconverted=True)
                innerRad = self.DC.getParamsByName("inner_radius", unconverted=True)
                feedWidth = self.DC.getParamsByName("feed_width", unconverted=True)
                feedLength = self.DC.getParamsByName("feed_length", unconverted=True) #inset
                gapDist = self.DC.getParamsByName("gap_distance", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")

                self.SO.coplanarKeyholeScriptGenerator(outerRad, innerRad, feedWidth, feedLength, gapDist, #outerRad, innerRad, feedWidth, inset, gapDist, d,
                                                        #groundLength, groundWidth, 
                                                        d, substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm")

            elif aType == 'rep_circular_loop':                    
                outerRad = self.DC.getParamsByName("outer_radius", unconverted=True)
                innerRad = self.DC.getParamsByName("inner_radius", unconverted=True)
                feedWidth = self.DC.getParamsByName("feed_width", unconverted=True)
                inset = self.DC.getParamsByName("inset", unconverted=True)
                gapDist = self.DC.getParamsByName("gap_distance", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                self.SO.circularLoopScriptGenerator(outerRad, innerRad, feedWidth, inset, gapDist,
                                                    #groundLength, groundWidth, 
                                                    d,substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm") 

            elif aType == 'rep_square_loop':                    
                l = self.DC.getParamsByName("length", unconverted=True)
                w = self.DC.getParamsByName("width", unconverted=True)
                feedWidth = self.DC.getParamsByName("feed_width", unconverted=True)
                gapDist = self.DC.getParamsByName("gap_distance", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                self.SO.squareLoopScriptGenerator(l, w, feedWidth, gapDist,
                                                        #groundLength, groundWidth, 
                                                        d, substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm") 

            elif aType == 'rep_double_sided_bowtie':           
                w2 = self.DC.getParamsByName("W2", unconverted=True)
                w3 = self.DC.getParamsByName("W3", unconverted=True)
                w4 = self.DC.getParamsByName("W4", unconverted=True)
                w5 = self.DC.getParamsByName("W5", unconverted=True)
                w6 = self.DC.getParamsByName("W6", unconverted=True)
                w7 = self.DC.getParamsByName("W7", unconverted=True)
                w8 = self.DC.getParamsByName("W8", unconverted=True)
                l2 = self.DC.getParamsByName("L2", unconverted=True)
                l3 = self.DC.getParamsByName("L3", unconverted=True)
                l4 = self.DC.getParamsByName("L4", unconverted=True)
                l5 = self.DC.getParamsByName("L5", unconverted=True)
                l6 = self.DC.getParamsByName("L6", unconverted=True)
                l7 = self.DC.getParamsByName("L7", unconverted=True)
                substrateHeight = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                #GP is NOT the fill back, so this MUST be a different variable
                groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                self.SO.doubleSidedBowtieScriptGenerator(w2, w3, w4, w5, w6, w7, w8,
                                                         l2, l3, l4, l5, l6, l7,
                                                        groundLength, groundWidth, substrateHeight,substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm") 

            elif aType == 'rep_planar_bowtie':                    
                l = self.DC.getParamsByName("length", unconverted=True)
                w = self.DC.getParamsByName("width", unconverted=True)
                feedWidth = self.DC.getParamsByName("feed_width", unconverted=True)
                gapDist = self.DC.getParamsByName("gap_distance", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                self.SO.planarBowtieScriptGenerator(l, w, feedWidth, gapDist,
                                                        #groundLength, groundWidth, 
                                                        d, substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm") 

            elif aType == 'rep_two_arm_square_spiral':                    
                initLength = self.DC.getParamsByName("init_length", unconverted=True)
                initWidth = self.DC.getParamsByName("init_width", unconverted=True)
                sw = self.DC.getParamsByName("strip_width", unconverted=True)
                x0 = self.DC.getParamsByName("feed_x", unconverted=True)
                y0 = self.DC.getParamsByName("feed_y", unconverted=True)
                spacing = self.DC.getParamsByName("spacing", unconverted=True)
                d = self.DC.getParamsByName("substrate_height", unconverted=True)
                #conductorHeight = self.DC.getParamsByName("conductor_height", unconverted=True)
                # groundLength = self.DC.getParamsByName("ground_plane_length", unconverted=True)
                # groundWidth = self.DC.getParamsByName("ground_plane_width", unconverted=True)
                substrateLength = self.DC.getParamsByName("substrate_length", unconverted=True)
                substrateWidth =self.DC.getParamsByName("substrate_width", unconverted=True)

                conductorName = self.DC.getFeaturesByName("conductor_material")
                groundMaterial = self.DC.getFeaturesByName("conductor_material")
                substrateMaterial = self.DC.getFeaturesByName("substrate_material")
                self.SO.twoArmSquareSpiralScriptGenerator(initLength, initWidth, sw, x0, y0, spacing, 
                                                        #groundLength, groundWidth, 
                                                        d,substrateLength, substrateWidth,
                                                        cMaterial=conductorName, gpMaterial=groundMaterial, sMaterial=substrateMaterial,
                                                        units="mm") 


        #save out to config file
        script = self.getDesignTemplateScript()
        self.DC.setDesignScript(script)

#############################################################
# Batch Template Functions
#
# makes use of all templateGen_ classes
#############################################################

    def batchTemplateGen(self, dfParams, dfUnits):
        # passed in a df of parameters
        # this is a SINGLE batch that goes in 1 script/exported file
        # (can be one row or many)

        batchTemplateScript = [] #running template arr

        #get names of the parameters
        paramNameArr = [] #for report templates
        for line in dfParams:
            if line not in paramNameArr:
                paramNameArr.append(str(line))

        #this is the same for ALL permutations - dont need to redo all sim setup
        # farFieldList = self.DC.getFarFieldReportList()  
        # terminalList = self.DC.getTerminalReportList()
        originalSimReportsTemplate = self.SO.getSimulationReportOnlyScript()

        #pair up names and vals for looping through param assignment template
        for i in range(0, len(dfParams)):
            self.SO.incrementExportReportGroupCounter()
            paramLst = []
            singleParamTemplate = []
            #get 1 row of name/value/unit pairs
            for p in paramNameArr:
                val = dfParams[p][i]
                unit = dfUnits[p][0]
                paramLst.append([p, val, unit])

            # 1) remove current reports/graphs
            if i > 0: #no reports to clear if first run
                self.SO.addClearSimulatedReports()
            rScript = self.SO.getReportEditTemplateScript()
            singleParamTemplate.extend(rScript)
            self.SO.clearReportEditTemplateScript()

            # 2) update params with list and add adjust params script
            self.paramEditTemplateGen(paramLst)

            # 3) update port location - if needed
            #NOTE: this might be auto move in HFSS - testing now
            # if self.PC.getAntennaGeneratorBoolean() == True: #used calc script
            #         atype = self.DC.getFeaturesByName('antenna_type')
            #         if atype == 'rectangular_patch':
            #             fType = self.DC.getFeaturesByName('feed_type')
            #             # get name format from params
            #             EMsoftware = self.PC.getSimulationSoftware()
            #             #get current values from batch inputs
            #             lName = self.DC.convertParamName(["length"],EMsoftware, returnGeneral=False)[0]
            #             for p in paramLst:
            #                 if p[0] == lName:
            #                     l = p[1]
            #                     units = p[2]
            #             networkType = "modal"
            #             portID = 1
            #             gp = float(l)*2 #for consistency
            #             d = self.DC.getFeaturesByName("substrate_height")
            #             if fType == 'microstrip':
            #                 startX = 0 
            #                 startY = float(gp)/2 #$ground_plane/2
            #                 startZ = -float(d) # -$depth
            #                 stopX = 0 #surface
            #                 stopY = float(gp)/2 #$ground_plane/2
            #                 stopZ = 0 
            #             elif fType == 'probe':
            #                 #these are based on genreally non-editable parameters,
            #                 # so this implementation may not catch all edge cases
            #                 pass
            #         self.SO.updatePortLocation(startX, startY, startZ, stopX, stopY, stopZ, units, networkType, portID)




            # 4) get script and update local template
            pScript = self.getParamEditTemplateScript()
            singleParamTemplate.extend(pScript)

            # 5) add the report setup 
            rScript = self.SO.getReportEditTemplateScript()
            singleParamTemplate.extend(rScript)
            self.SO.clearReportEditTemplateScript()

            # 6) append code to run graphs (use same as originally generated)
            #see top of file for vars
            singleParamTemplate.extend(originalSimReportsTemplate)

            # 7) report export
            # self.SO.exportFarFieldReportData(farFieldList, ctr=True)
            # self.SO.exportTerminalReportData(terminalList, ctr=True)
            reportNames = self.SO.getReportNames()
            self.SO.exportReportsByName(reportNames, ctr=True)
            rScript = self.SO.getReportEditTemplateScript()
            singleParamTemplate.extend(rScript)

            # 8) append the main mini batch script
            batchTemplateScript.append(singleParamTemplate)

            # 9) clear script template objs
            self.SO.clearParamEditTemplateScript()
            self.SO.clearReportEditTemplateScript()
            
        return batchTemplateScript    


#############################################################
# Parameter Edit Template Functions
#
# Tuning uses this directly
############################################################

    def setParamEditTemplateScript(self, s):
        self.SO.setParamEditTemplateScript(s)

    def getParamEditTemplateScript(self):
        return self.SO.getParamEditTemplateScript()
    
    def clearParamEditTemplateScript(self):
        self.SO.clearParamEditTemplateScript()

    def addSaveToParamEditScript(self):
        self.SO.addSaveToParamEditScript()

    def paramEditTemplateGen(self, lst):
        #gets list of [[paramName, val, unit],[paramName, val, unit]...] of param and values for single sim change
        # uses the same function called internally bt TG_Design
        self.SO.updateProjectParametersWithList(lst)


#############################################################
# Simulation Template Functions
############################################################

    def setSimulationTemplateScript(self, s):
        self.SO.setSimulationTemplateScript(s)

    def getSimulationTemplateScript(self):
        return self.SO.getSimulationTemplateScript()
    
    def useDefaultOptimizerReportSimulationOptions(self, optimizerDir):
        self.SO.createSimulationTemplate()
        self.SO.createParamEditTemplate() #reset this each time bc dont need long term mem
        self.SO.createReportExportTemplate(optimizerDir)

        modalLst, modalFtsLst, terminalLst, terminalFtsLst, \
            farFieldLst, farfieldFtsLst, dataTableLst, antennaParamLst =self.SO.useDefaultOptimizerReportSimulationOptions()

        self.DC.setModalReportList(modalLst, modalFtsLst)
        self.DC.setTerminalReportList(terminalLst, terminalFtsLst)
        self.DC.setFarFieldReportList(farFieldLst, farfieldFtsLst)
        self.DC.setDataTableReportList(dataTableLst, dataTableLst, dataTableLst) #modal,terminal,farfield
        self.DC.setAntennaParamTableList(antennaParamLst) 
        
        self.simulationTemplateGen(createNew=False)

        reportNames = self.SO.getReportNames()
        self.SO.exportReportsByName(reportNames, ctr=False)


    def simulationTemplateGen(self, createNew=True):
        if createNew == True: #toggle to combine 2 funcs
            self.SO.createSimulationTemplate() #creates new obj so no clearing
        
        #design from imported script (has full script)
        if self.PC.getImportScriptBoolean() == True:
            pass
        #loaded project + manually added params
        elif self.PC.getImportProjectBoolean() == True:
            pass
        elif self.PC.getAntennaGeneratorBoolean() == True:
            pass

        freq = self.DC.getSimulationFreq()
        useMult = self.DC.getUseMultipleFreq()
        minFreq= self.DC.getMinSimRange()
        maxFreq= self.DC.getMaxSimRange()
        maxDelta = self.DC.getMaxDelta()
        numPasses = self.DC.getNumPasses()
        numPoints = self.DC.getNumSimPts()
        self.SO.addBaseSimTemplateSetup(freq, useMult, minFreq, maxFreq, maxDelta, numPasses, numPoints)
        # set to the sim script memory in DC
        script = self.SO.getSimulationTemplateScript()
        self.DC.setSimulationScript(script)
        #clear memory to do the report setup
        self.SO.clearSimulationTemplateScript()

        # get list of reports to gen
        # modal
        modalList = self.DC.getModalReportList()
        modalFtList = self.DC.getModalFeaturesList()
        # modalFcList = self.DC.getModalFunctionsList()
        # terminal
        terminalList = self.DC.getTerminalReportList()
        terminalFtList = self.DC.getTerminalFeaturesList()
        # terminalFcList = self.DC.getTerminalFunctionsList()
        # far field
        farFieldList = self.DC.getFarFieldReportList()
        farFieldFtList = self.DC.getFarFieldFeaturesList()
        # farFieldFcList = self.DC.getFarFieldFunctionsList()
        # data table
        DTModalFtList = self.DC.getDataTableModalFeaturesList()
        # DTModalFcList = self.DC.getDataTableModalFunctionsList()
        DTTerminalFtList = self.DC.getDataTableTerminalFeaturesList()
        # DTTerminalFcList = self.DC.getDataTableTerminalFunctionsList()
        DTFarFieldFtList = self.DC.getDataTableFarFieldFeaturesList()
        #antenna parameter table
        antennaParametersFtList = self.DC.getAntennaParamTableList()

        # # get param names to add to reports (for nominal)
        paramNameArr = []# get param names to add to reports (for nominal)
        for pn in self.DC.getParams():
            paramNameArr.append(pn)
        # TODO: get other report features (i.e. features for individual TS or FF pass thru)
           
        #add analyze all and report setup to template
        self.SO.addSimulationRunAnalysis()
        self.SO.addSimulationReportSetup()


        #add report code to template
        self.SO.generateModalReportsFromList(modalList, modalFtList, paramNameArr)
        self.SO.generateTerminalReportsFromList(terminalList, terminalFtList, paramNameArr)
        self.SO.generateFarFieldReportsFromList(farFieldList, farFieldFtList, paramNameArr, freq)
        self.SO.generateDataTableReportsFromList(DTModalFtList, DTTerminalFtList, DTFarFieldFtList, paramNameArr, freq)
        self.SO.generateAntennaParameterTableReportsFromList(antennaParametersFtList, paramNameArr)
        
        self.SO.addSimulationSaveProject()

        # set the report script memort in DC
        script = self.SO.getSimulationReportOnlyScript()
        # print(script)
        self.DC.setReportsScript(script)
        # print("REPORT SCRIPT SET IN SIMULATION_INTEGRATOR.PY")

#############################################################
# Report Export Template Functions
############################################################


# this is mostly left over from scrap code, but might be
# important for some export-only funcs

    def setReportEditTemplateScript(self, s):
        self.SO.setReportEditTemplateScript(s)

    def getReportEditTemplateScript(self):
        return self.SO.getReportEditTemplateScript()

    def reportExportTemplateGen(self):
        # projPath = str(self.PC.getProjectDirectory())
        # self.SO.ST.exportTerminalReportData(terminalList)
        # self.SO.ST.exportFarFieldReportData(farFieldList)

        #TODO: check for more options as layers and custom shapes are added
        #design from imported script (has full script)
        if self.PC.getImportScriptBoolean() == True:
            pass

        #loaded project + manually added params
        elif self.PC.getImportProjectBoolean() == True:
 
            pass
    
        elif self.PC.getAntennaGeneratorBoolean() == True:
            pass


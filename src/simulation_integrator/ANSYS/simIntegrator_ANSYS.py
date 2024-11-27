##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/HFSS/simInterator_HFSS.py'
#   The main class for integrating AntennaCAT with HFSS.
#   This class contains code for tracking running HFSS instances, 
#   and template creation/editing
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\
import sys
import os
import subprocess
from subprocess import Popen
from wx import MessageDialog, YES_NO, ID_YES, ICON_QUESTION
from wx import CallLater
from queue import Queue
import time

sys.path.insert(0, './src/simulation_integrator')
from simulation_integrator.ANSYS.templateGen_Design import DesignTemplate
from simulation_integrator.ANSYS.templateGen_ParamEdit import ParamEditTemplate
from simulation_integrator.ANSYS.templateGen_ReportExport import ReportExportTemplate
from simulation_integrator.ANSYS.templateGen_Simulation import SimulationTemplate


sys.path.insert(0, './src/config')
import project.config.antennaCAT_config as c


class SimIntegrator_ANSYS():
    def __init__(self, softwarePath, numLicenses, projName="generatedProject.aedt", projDir="./output"):
        self.numSimsRunning = 0
        self.simulationSoftwarePath = softwarePath
        self.numLicense = numLicenses
        self.projectName = projName
        self.emSoftwareProjectName = None
        self.p = -1 #return code for polling
        self.fileQueue = [] #files that are in queue to simulate
        self.reportNames = []

        self.DT = None # design template
        self.PT = None # param edit template
        self.ST = None # simulation export template     
        self.RT = None # report export template

        # self.projDir=None
        #default names
        self.designFileName = "DesignCreation.py"
        # ANSYS_DESIGN_EDIT_SCRIPT_NAME = "DesignEdit.py" #for Tuning/iterative scripts
        self.simulationFileName =  "DesignSimulation.py"
        self.parameterEditFileName = "DesignParamChange.py"
        self.reportExportFileName = "ReportExport.py"

    def getEMSoftwareProjectName(self): 
        return self.emSoftwareProjectName

    def createDesignTemplate(self, projName="generatedProject.aedt", projDir=None):
        self.DT = DesignTemplate(projName, projDir)
        self.emSoftwareProjectName = self.DT.getEMSoftwareProjectName()
     
    def createParamEditTemplate(self):
        self.PT = ParamEditTemplate()
    
    def createSimulationTemplate(self):
        self.ST = SimulationTemplate()
    
    def createReportExportTemplate(self, projDir):
        self.RT = ReportExportTemplate(projDir)

    def getDefaultFilePathNames(self):
        return self.designFileName, self.simulationFileName, self.parameterEditFileName, self.reportExportFileName
     
    #######################################################
    # make sure files match expected types for saving
    #######################################################

    def getExpectedScriptFileExtension(self):
        return ".py"

    def getExpectedScriptFileType(self):
        return "Python files (*.py)|*.py"
  
    def getExpectedLockFileExtension(self):
        return ".lock"

    def getExpectedProjectExtension(self):
        return ".aedt"
  
    def getLockFile(self):
        lockFileExt = self.getExpectedLockFileExtension() # get lock file extension
        projFileExt = self.getExpectedProjectExtension()
        simFile = self.getEMSoftwareProjectName() # path with simulation file including extension
        head, tail = os.path.splitext(simFile) #solit to get everything but extension
        lockFilepath = os.path.join(head + projFileExt + lockFileExt) # join
        return lockFilepath

    #######################################################
    # Add comments to file
    #######################################################

    # default option
    def addCommentsToFile(self, t=""):
        self.DT.addCommentsToFile(t)
        self.comments = t
        
    # comments to specific scripts
    def addCommentsToDesignTemplate(self, t):
        self.DT.addCommentsToFile(t)
        

    ########################################################
    # Small Helper Funcs
    ########################################################

    def clearReportNames(self):
        self.ST.clearReportNames()

    def getReportNames(self):
        return self.ST.getReportNames()
    
    # def addNewReportName(self, nameList):
    #     for n in nameList:
    #         if n not in self.reportNames:
    #             self.reportNames.append(n)

    ########################################################
    # Design Template Funcs
    ########################################################

    def getDesignTemplateObject(self):
        return self.DT

    def getDesignTemplateScript(self):
        return self.DT.getTemplateScript()
        
    def setDesignTemplateScript(self, s):
        self.DT.setTemplateScript(s)
    
    def clearDesignTemplateScript(self):
        self.DT.clearTemplateScript()

    def addOpenExistingProjectBase(self, projectPath, filename):
        self.DT.addOpenExistingProjectBase(projectPath, filename)

    ########################################################
    # Antenna Generation pre-made script calls
    ########################################################

    def patchStripFedScriptGenerator(self,w, l,d, sw, x0, y0, g, gp, conductorMaterial, groundMaterial,substrateMaterial, units):
        self.DT.patchStripFedScriptGenerator(w, l,d, sw, x0, y0, g, gp, conductorMaterial, groundMaterial,substrateMaterial, units)
    
    def patchProbeFedScriptGenerator(self, w, l, d, x0, y0, gp, cMaterial, gpMaterial, sMaterial, units):
        self.DT.patchProbeFedScriptGenerator(w, l, d, x0, y0, gp, cMaterial, gpMaterial, sMaterial, units)

    def halfWaveDipoleScriptGenerator(self,l, r, fg, cMaterial, units):
        self.DT.halfWaveDipoleScriptGenerator(l, r, fg, cMaterial, units)
    
    def quarterWaveMonopoleScriptGenerator(self,l, r, gp, fg, cMaterial, units):
        self.DT.quarterWaveMonopoleScriptGenerator(l, r, gp, fg, cMaterial, units)

    def EMicrostripFedScriptGenerator(self,x, l, ls, lg, ps, ws, w, wg, cMaterial, gpMaterial, units):
        self.DT.EMicrostripFedScriptGenerator(x, l, ls, lg, ps, ws, w, wg, cMaterial, gpMaterial, units)

    def slottedRectangularPatchScriptGenerator(self,Lr,Lh,Lv,l,Lg,fx,Pr,Wr,Wu,w,Wg,fy,d, cMaterial, gpMaterial, sMaterial, units):
        self.DT.slottedRectangularPatchScriptGenerator(Lr,Lh,Lv,l,Lg,fx,Pr,Wr,Wu,w,Wg,fy,d, cMaterial, gpMaterial, sMaterial, units)

    def dualBandSerpentineScriptGenerator(self,fy, px, py, d, lp, lsub, wp, wsub, 
                                          ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                                        cMaterial, gpMaterial, sMaterial, units):
        self.DT.dualBandSerpentineScriptGenerator(fy, px, py, d, lp, lsub, wp, wsub,
                                                   ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4, lc,
                                                        cMaterial, gpMaterial, sMaterial, units)

    def CircularLoopScriptGenerator(self,outerRad, innerRad, feedWidth, inset, gapDist,
                                                        cMaterial, gpMaterial, sMaterial, units):
        self.DT.CircularLoopScriptGenerator(outerRad, innerRad, feedWidth, inset, gapDist,
                                                        cMaterial, gpMaterial, sMaterial, units)



    ########################################################
    # Param Edit Template Funcs
    ########################################################

    def getParamEditTemplateObject(self):
        return self.PT

    def getParamEditTemplateScript(self):
        return self.PT.getTemplateScript()
        
    def setParamEditTemplateScript(self, s):
        self.PT.setTemplateScript(s) 
    
    def clearParamEditTemplateScript(self):
        self.PT.clearTemplateScript()

    def addSaveToParamEditScript(self):
        self.PT.addSaveProject()

    def updateProjectParametersWithList(self, s):
        self.PT.updateProjectParametersWithList(s)

    def updatePortLocation(self, startX, startY, startZ, stopX, stopY, stopZ, units="mm", networkType="modal", portID=1):
        self.PT.updatePortLocation(startX, startY, startZ, stopX, stopY, stopZ, units, networkType, portID)

    ########################################################
    # Simulation Template Funcs
    ########################################################
    def addBaseSimTemplateSetup(self, freq, useMult, minFreq, maxFreq, maxDelta, numPasses, numPoints):
        self.ST.addBaseSimTemplateSetup(f=freq, useMult= useMult, minR=minFreq, maxR=maxFreq, delta=maxDelta,
                                   numPass=numPasses, numPts=numPoints)

    def getSimulationTemplateObject(self):
        return self.ST 

    def getSimulationTemplateScript(self):
        return self.ST.getTemplateScript()
        
    def setSimulationTemplateScript(self, s):
        self.ST.setTemplateScript(s)

    def getSimulationReportOnlyScript(self):
        return self.ST.getReportOnlyScript()

    def clearSimulationTemplateScript(self):
        self.ST.clearTemplateScript()

    def useDefaultOptimizerReportSimulationOptions(self):
        return self.ST.getDefaultOptimizerReports()
        
    def generateTerminalReportsFromList(self, terminalList, terminalFtList, paramNameArr):
        self.ST.generateTerminalReportsFromList(terminalList, terminalFtList, paramNameArr)
       
    def generateModalReportsFromList(self, modalList, modalFtList, paramNameArr):
        self.ST.generateModalReportsFromList(modalList, modalFtList, paramNameArr)

    def generateFarFieldReportsFromList(self, farFieldList, farFieldFtList, paramNameArr, freq):
        self.ST.generateFarFieldReportsFromList(farFieldList, farFieldFtList, paramNameArr, freq)

    def generateDataTableReportsFromList(self, DTModalFtList, DTTerminalFtList, DTFarFieldFtList, paramNameArr, freq):
        self.ST.generateDataTableReportsFromList(DTModalFtList, DTTerminalFtList, DTFarFieldFtList, paramNameArr, freq)

    def generateAntennaParameterTableReportsFromList(self, antennaParamTableFtList, paramNameArr):
        self.ST.generateAntennaParameterTableReportsFromList(antennaParamTableFtList, paramNameArr)

    def addSimulationSaveProject(self):
        self.ST.addSaveProject()

    def addSimulationRunAnalysis(self):
        self.ST.analyzeAll()
    
    def addSimulationReportSetup(self):
        self.ST.reportSetup()
        

    ########################################################
    # Report Export Template Funcs
    ########################################################

    def getReportEditTemplateObject(self):
        return self.RT

    def getReportEditTemplateScript(self):
        return self.RT.getTemplateScript()
        
    def setReportEditTemplateScript(self, s):
        self.RT.setTemplateScript(s)

    def clearReportEditTemplateScript(self):
        self.RT.clearTemplateScript()
    
    def addClearSimulatedReports(self):
        self.RT.addClearSimulatedReports()
    
    def addRunNewAnalysis(self):
        self.RT.addRunNewAnalysis()
    
    def addReportSetup(self):
        self.RT.addReportSetup()

    def incrementExportReportGroupCounter(self):
        self.RT.incrementExportReportGroupCounter()
        
    def exportFarFieldReportData(self, lst, ctr=False):
        self.RT.exportFarFieldReportData(lst, ctr)

    def exportModalReportData(self, lst, ctr=False):
        self.RT.exportModalReportData(lst, ctr)
    
    def exportTerminalReportData(self, lst, ctr=False):
        self.RT.exportTerminalReportData(lst, ctr)

    def exportReportsByName(self, lst, ctr=False):
        self.RT.exportReportsByName(lst, ctr)

    ##########################################################
    # HFSS software integration functions
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

    def runWithScript(self, sim, newSession=True):
        cmds = [self.simulationSoftwarePath, "-RunScript", sim]
        self.runProcess(cmds, newSession)
      
    def runWithScriptAndExit(self, sim, newSession=True):
        cmds = [self.simulationSoftwarePath, "-RunScriptAndExit", sim]
        self.runProcess(cmds, newSession)
    
    def runBatchAndExit(self, files, numLicenses=1, newSession=True):
        #TODO: add in the multi threading 
        self.fileQueue = Queue()
        [self.fileQueue.put(f) for f in files]
        self.numLicense = numLicenses
        self.runBatchLoopAndExit()

    def runBatchLoopAndExit(self):
        #used CallLater to make this non blocking
        #check if anything left in queue
        if (self.fileQueue.empty() ==False):
            CallLater(5000, self.runBatchLoopAndExit) #1000 = 1 second 
        else:
            #print("done looping")
            pass
        #check if sim running
        if self.checkRunningProcess() == -1:
                sim = self.fileQueue.get() #first sim
                cmds = [self.simulationSoftwarePath, "-RunScriptAndExit", sim]
                self.runProcess(cmds, newSession=True)
                # print(self.fileQueue)        

    def runBatchAndWait(self, files, numLicenses, newSession=True):
        #TODO: add in the multi threading 
        self.fileQueue = Queue()
        [self.fileQueue.put(f) for f in files]
        self.numLicense = numLicenses
        self.runBatchLoopAndWait()

    def runBatchLoopAndWait(self):
        #used CallLater to make this non blocking
        #check if anything left in queue
        if (self.fileQueue.empty() ==False):
            CallLater(5000, self.runBatchLoopAndWait) #1000 = 1 second 
        else:
            # print("done looping")
            pass
        #check if sim running
        if self.checkRunningProcess() == -1:
                sim = self.fileQueue.get() #first sim
                cmds = [self.simulationSoftwarePath, "-RunScript", sim]
                self.runProcess(cmds, newSession=True)
                # print(self.fileQueue)

    def runProcess(self, cmds, newSession):
        # time.sleep(3) # wait 3 seconds because in some instances the pipe closes too fast for the program
        proc = self.checkRunningProcess()
        try:
            if (proc == None):
                # wait 2 seconds because in some instances the pipe closes too fast for the program
                time.sleep(2)
                proc = self.checkRunningProcess()  
        except:
            # if proc is an int, the type comparison mismatch might throw an error. 
            # It's not actually an error that needs to be dealt with. Just double checked
            pass
             
        if (proc == -1):
            self.p = subprocess.Popen(cmds, start_new_session=newSession)
            time.sleep(10) # give the process 10 seconds to start up properly
        else: 
            pass
            # dlg = MessageDialog(None, "simulation thread is currently running. Do you want to stop it and start another?\
            #                     If you are getting this in mistake, go to simIntegrator_ANSYS.py and comment out the proc == None option",'Stop simulation?', YES_NO| ICON_QUESTION)
            # result = dlg.ShowModal()
            # if result == ID_YES:
            #     #self.p.kill()
            #     try:
            #        self.p.terminate() 
            #        time.sleep(2) # make sure the process is fully shut down
            #     except Exception as e:
            #         print("EXCEPTION raised when attempting to terminate process. " + str(e))
                
            #     self.p = None
            #     self.p = subprocess.Popen(cmds, start_new_session=newSession)
            #     time.sleep(10) # give the process 10 seconds to start up properly

    def checkRunningProcess(self):
        try:
            stat = self.p.poll()
            #print("stat: " + str(stat))
            if stat == 0:
                self.markProcessFinished()
            return stat
        except:
            return -1
        
    def getSimulationRunningBool(self):
        # interprets the running process values as a bool
        # -1: no simulation created
        #  1: simulation active (some systems)
        # None: running
        # 0: shutting down
        noError = True
        val = self.checkRunningProcess()
        if (val == -1):
            return False, noError
        elif (val == 1) or (val == None) or (val == 0):
            return True, noError
        else:
            print("Abnormal termination in simIntegrator_ANSYS.py")
            return False, False
             
        
    def markProcessFinished(self):
        self.p = -1
        
    def terminateRunningProcess(self):
        self.p.terminate() 
        time.sleep(5) # make sure the process is fully shut down. 
                    # 2 seconds was not enough in all cases, but 10 is too much
        self.p = -1


if __name__ == "__main__":
    pass

##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/EMPIRE/simInterator_EMPIRE.py'
#   The main class for integrating AntennaCAT with EMPIRE.
#   This class contains code for tracking running EMPIRE instances, 
#   and template creation/editing
#
#   NOTE: Redoing with the updated ANSYS template to bring everything up to date
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import subprocess
from subprocess import Popen
from wx import MessageDialog, YES_NO, ID_YES, ICON_QUESTION

import pandas as pd
import numpy as np

import sys
sys.path.insert(0, './src/simulation_integrator')
from simulation_integrator.EMPIRE.templateGen_Design import DesignTemplate
# from simulation_integrator.EMPIRE.templateGen_ParamEdit import ParamEditTemplate
# from simulation_integrator.EMPIRE.templateGen_ReportExport import ReportExportTemplate
from simulation_integrator.EMPIRE.templateGen_Simulation import SimulationTemplate


import project.config.antennaCAT_config as c
# EMPIRE_PATH = c.EMPIRE_PATH
FREQ_PARAM_DATA = ".\output\data\Terminal_S-Parameter_Rectangular-Plot.csv"
ANTENNA_PARAM_DATA = ".\output\data\Antenna-Parameters-Table.csv"
DEFAULT_EMPIRE_PROJECT_NAME = "GeneratedProject.py"
EMPIRE_DESIGN_CREATION_SCRIPT_NAME = "DesignCreation.py"
EMPIRE_DESIGN_EDIT_SCRIPT_NAME = "DesignEdit.py"
EMPIRE_SIMULATION_SCRIPT_NAME =  "DesignSimulation.py"
EMPIRE_PARAM_EDIT_SCRIPT_NAME = "DesignParamChange.py"
EMPIRE_REPORT_EXPORT_SCRIPT_NAME = "ReportExport.py"


class SimIntegrator_EMPIRE:
    def __init__(self, softwarePath, numLicenses):
        self.numSimsRunning = 0
        self.simulationSoftwarePath = softwarePath
        self.numLicense = numLicenses
        self.p = -1 #return code for polling

        self.DT = None # design template
        self.PT = None # param edit template
        self.RT = None # report export template
        self.ST = None # simulation export template        

        self.projDir=None

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

    def runProcess(self, cmds, newSession):
        proc = self.checkRunningProcess()
        if proc == -1:
            self.p = subprocess.Popen(cmds, start_new_session=newSession)
        else: 
            dlg = MessageDialog(None, "A simulation thread is currently running. Do you want to stop it and start another?",'Stop simulation?', YES_NO| ICON_QUESTION)
            result = dlg.ShowModal()
            if result == ID_YES:
                #self.p.kill()
                try:
                   self.p.terminate() 
                except Exception as e:
                    print("EXCEPTION raised when attempting to terminate process. " + str(e))
                
                self.p = None
                self.p = subprocess.Popen(cmds, start_new_session=newSession)

    def checkRunningProcess(self):
        try:
            stat = self.p.poll()
            if stat == 0:
                self.markProcessFinished()
            return stat
        except:
            return -1

    def markProcessFinished(self):
        self.p = -1
        
    def terminateRunningProcess(self):
        self.p.terminate()
        self.p = -1

    ##################################################
    # antenna design and build template functions
    ##################################################
    
    def createDesignTemplate(self, projName, projDir):
        #create the antenna template object
        self.DT = DesignTemplate(projName, projDir)
        self.projDir = projDir

    def addCommentsToFile(self, t=""):
        self.DT.addCommentsToFile(t)
        self.comments = t

    ##################################################
    # antenna simulation template functions
    ##################################################

    def createSimulationScriptObject(self):
        self.ST = SimulationTemplate()
        self.ST.setProjectPath(self.projDir)

    def addDesignTemplateFromMemory(self):
        #specifically uses the already created antenna design
        #does not need to be used to create a sim script for an already RUNNING project
        atnScript = self.DT.getTemplateScript()
        self.ST.addTemplateFromMemory(atnScript)

    ##################################################
    # csv/data manipulation and processing
    ##################################################

    def readInCSV(self, file):
        # read in CSV data
        data = pd.read_csv(file)
        return data


    def getFrequencyParameters(self, targetFreq, file=FREQ_PARAM_DATA):
        print("loading freq parameter file")
        print("targetFreq:", targetFreq)


        data = self.readInCSV(file) 
        xData = data.iloc[:,0] #the freq vals in GHz
        yData = data.iloc[:,1] #the s11 dB data 
        targetFreq = float(targetFreq)#convert from string

        #get the local minimas
        localMinima = self.findLocalMinima(data=yData)

        #Get the closest resonant frequency to the target
        potenitalResFreqs= (data._get_value(localMinima, 0, takeable=True))*1e9 #scale bc this is in GHz. i.e  2.4GHz is 2.4
        #go through the list to get the val that's closest to the target frequency
        idx = np.argmin(abs((potenitalResFreqs - targetFreq)))
        simS11ResFreq = potenitalResFreqs[0]
        print("closest resonant freq: ", simS11ResFreq)
        # index of resonant freq
        simS11ResIdx = localMinima[idx]
        #value of the resonant freq in dB
        simS11ResFreqs11dB = data._get_value(simS11ResIdx, 1, takeable=True)

        #find the simulated frequency value that best matches the target frequency 
        # - this is a metric for how well the antenna is simulating at the target frequency
        getDistanceFromTarget = (data.iloc[:,0] - targetFreq/1e9).abs().argmin()
        nearestTargetFreqVal = data._get_value(getDistanceFromTarget, 0, takeable=True)
        nearestTargetFreqValdB = data._get_value(getDistanceFromTarget, 1, takeable=True)
        print("found nearest target value")

        pltData = data
        return simS11ResFreq, simS11ResFreqs11dB, nearestTargetFreqVal, nearestTargetFreqValdB, pltData

    def findLocalMinima(self, data):
        #takes in a 1D array of data
        #outputs a 1D array of indexes
        numElements = len(data)
        ctr = 0
        localMinIdxList = []
        for i in data:
            if ctr == 0: #check fist val special case
                if data[ctr] < data[ctr+1]: #first val is lower, so technically a local min
                    localMinIdxList.append(ctr)
            else:
                if ctr==(numElements-1): #at end of the list
                    if data[ctr-1]>data[ctr]: #last value is technically local minima
                        localMinIdxList.append(ctr)
                else: #not at start or end of list. operate as normal
                    if data[ctr-1] > data[ctr] < data[ctr+1]: #vals on either side are higher, so this is the local minima
                        localMinIdxList.append(ctr)
            ctr = ctr + 1
        return localMinIdxList

    def getAntennaParameters(self, file = ANTENNA_PARAM_DATA):
        data = pd.read_csv(file)
        #Freq, PeakDirectivity, PeakGain, TotalEfficiency
        peakDirectivity = data._get_value(0, 1, takeable=True) #use later
        peakGain = data._get_value(0, 2, takeable=True)
        totalEfficiency = data._get_value(0, 3, takeable=True)
        return peakGain, totalEfficiency

if __name__ == "__main__":
    import time
    # from templateGen_Antenna import AntennaTemplate
    # from templateGen_Simulation import SimulationTemplate

    # SI = SimIntegrator_HFSS(simPath="C:\Program Files\AnsysEM\Ansys Student\\v222\Win64\\ansysedtsv.exe")
    # f, d = SI.getResonantFrequency()
    # print(f)
    # print(d)
    # g = SI.getGain()
    # print(g)

    # uncomment this to test if fim program starts correctly
    # cmds = ["C:\Program Files\AnsysEM\Ansys Student\\v222\Win64\\ansysedtsv.exe", 
    # "-RunScript", "C:\\Users\LCLin\\VSCodeProjects\\AntennaCalculationAutotuningTool\\output\\AntennaSimulation.py"]
    # p = subprocess.Popen(cmds, start_new_session=True)

    #FEKO test
    cmds = ["C:\\Program Files\\Altair\\2022-edu\\feko\\bin\\cadfeko.exe", 
    "--run-script", "C:\\Users\\LCLin\\Desktop\\MacroRecording_1.lua"]
    p = subprocess.Popen(cmds, start_new_session=True)

    while True:
        # None = not started yet. script running. probably a windows thing?
        # 0 = nothing running, but subprocess still active
        # 1 = busy, but doesnt always hit. this is from documentation
        print(p.poll())
        time.sleep(10)

##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/page_optimizer/page_optimizer.py'
#   Class for batch data collection page
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 10, 2025
##--------------------------------------------------------------------\
# system level imports
import os
import sys
import wx
import wx.aui
import wx.lib.newevent
import pandas as pd

# local imports
import project.config.antennaCAT_config as c
from optimizers.optimizer_integrator import OptimizerIntegrator
from gui.page_optimizer.notebook_summary.notebook_summary import SummaryNotebook
from gui.page_optimizer.notebook_params.notebook_params import ParamsNotebook
from gui.page_optimizer.notebook_optimizer.notebook_optimizer import OptimizerNotebook

sys.path.insert(0, './project/')
from project.antennaCAT_project import AntennaCATProject

# default frame/panel sizes
#CHANGE IN CONSTANTS.PY FOR CONSISTENCY ACROSS PROJECT
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
PANEL_HEIGHT = c.PANEL_HEIGHT
PANEL_WIDTH = c.PANEL_WIDTH
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class OptimizerPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO        
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)
        
        self.OI = OptimizerIntegrator(self, self.DC, self.PC, self.SO)        
        
        self.optimizerSelected = False
        self.paramList = []
        self.paramValLst = []
        self.paramInput = []

        # optimizer notebook
        self.notebook_optimizer = OptimizerNotebook(self, self.DC, self.PC, self.SO)
        self.notebook_optimizer.SetMaxSize(wx.Size(-1, 450))  # set a max so the controllable parameters menu is readable
        # controllable parameters panel
        self.notebook_params  = ParamsNotebook(self)
        # summary notebook
        self.notebook_summary = SummaryNotebook(self)

        # buttons
        
        self.btnRun = wx.Button(self, label="Run")
        self.btnRun.Bind(wx.EVT_BUTTON, self.btnRunClicked)
        self.btnPause = wx.Button(self, label="Pause")
        self.btnPause.Bind(wx.EVT_BUTTON, self.btnPauseClicked)
        self.btnStop = wx.Button(self, label="Stop")
        self.btnStop.Bind(wx.EVT_BUTTON, self.btnStopClicked)

        self.btnKillSimulation = wx.Button(self, label="End Simulation")
        self.btnKillSimulation.Bind(wx.EVT_BUTTON, self.btnKillSimulationClicked)

        # # sizers
        # top sizer wth params and summary
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.notebook_optimizer, 1, wx.ALL | wx.EXPAND, border=5)

        ## btnSizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        btnTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnTopSizer.Add(self.btnRun, 0, wx.ALL, border=10)
        btnTopSizer.Add(self.btnPause, 0, wx.ALL, border=10)
        btnTopSizer.Add(self.btnStop, 0, wx.ALL, border=10)
        btnBottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        # btnBottomSizer.Add(self.btnRerunSimulation, 0, wx.ALL, border=10)
        btnBottomSizer.Add(self.btnKillSimulation, 0, wx.ALL, border=10)
        btnSizer.Add(btnTopSizer, 0, wx.ALL, border=10)
        btnSizer.Add(btnBottomSizer, 0, wx.ALL, border=10)

        # bottom window sizer with param detection and status
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(self.notebook_params, 1, wx.ALL | wx.EXPAND, border=5)
        bottomSizer.Add(self.notebook_summary , 1, wx.ALL | wx.EXPAND, border=5)

        # main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(topSizer, 1, wx.ALL | wx.EXPAND, border=0)
        pageSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_RIGHT, border=0)
        pageSizer.Add(bottomSizer, 1, wx.ALL | wx.EXPAND, border=0)
        self.SetSizer(pageSizer)


    def updateStatusText(self, t):
        if t is None:
            return
        self.notebook_summary.updateStatusText(t)

    def updateDetailsText(self, t):
        if t is None:
            return
        self.notebook_summary.updateDetailsText(t)

    def clearTextWindows(self):
        self.notebook_summary.clearStatus()
        self.notebook_summary.clearDetails()

    def clearCurrent(self):
        self.paramList = []
        self.paramValLst = []
        self.paramInput = []
        #clear old rows
        self.notebook_params.clearPanelRows()    

    def updateSimulationSettingsBoxes(self):
        self.notebook_optimizer.updateSimulationSettingsBoxes()
        # # self.notebook_optimizer.updateSimulationSetupValues()
        # self.notebook_simSettings.updateSimulationAutoGenValues()
        # self.notebook_simSettings.updateSimulationSetupValues()



#######################################################
# Button Events
#######################################################

    def btnRunClicked(self, evt=None):        
        # called from panels in optimizer notebook, calls OI function

        # check if design was set
        if self.PC.getDesignScriptCreatedBool() == False:
            msg = "No design script detected to export"
            self.updateStatusText(msg)
            return
    
        # check if optimizer has been selected
        if self.checkIfOptimizerSelected() == False:
            return
        self.OI.run()

    def btnPauseClicked(self, evt=None):
        # check if optimizer has been selected
        if self.checkIfOptimizerSelected() == False:
            return
        self.OI.pause()

    def btnKillSimulationClicked(self, evt=None):
        # force kill simulation if process is hung
        if self.checkIfOptimizerSelected() == False:
            return
               
        self.OI.killSimulation()

    # def btnRerunSimulationClicked(self, evt=None):
    #     # force rerun simulation if process is hung
    #     if self.checkIfOptimizerSelected() == False:
    #         return
    #     self.OI.RerunSimulation()

    def btnStopClicked(self, evt=None):
        #called from panels in optimizer notebook, calls OI function        
        # check if optimizer has been selected
        if self.checkIfOptimizerSelected() == False:
            return
        
        self.OI.stop()

    def checkIfOptimizerSelected(self):        
        # check if optimizer has been selected and print warning
        if self.optimizerSelected == False:
            msg = "an optimizer must be selected before running"
            self.updateStatusText(msg)
        return self.optimizerSelected


    def btnOpenClicked(self, pth):
        #called from panels in optimizer notebook, calls OI function
        self.OI.openSaved(pth)
    
    def btnSelectClicked(self, optimizerName, noError):
        # TODO This should probably be pulled out one level higher or to a different file, 
        # but that needs to be hashed out with the balance between 
        # UI driven controls & segmentation vs. pulling commands out of the GUI state machine

        self.set_up_optimizer(optimizerName, noError)

       
    def btnExportClicked(self, evt=None):
        if self.optimizerSelected == False:
            msg = "an optimizer must be selected before state can be exported"
            self.updateStatusText(msg)
            return

        self.export_optimizer_settings()        


    def btnDetectClicked(self, evt=None):
        # check that a design was created
        if self.PC.getDesignConfigBool() == False:
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)
            return        
        #clear old rows
        self.clearCurrent()
        #if design was created, then there's something in:
        # 1) design script (even if it's just a call to open a file)
        # and 2) self.DC.self.designParams <- any provided/calculated params
        # future expansion: self.DC.designFeatures <- like layer height (to make substrate dynamic)
        designParams = self.DC.getParams()
        self.populateDetectedKeywords(designParams)
        if self.paramList == [] or self.paramList == None:
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)            
        else:
            self.notebook_params.addParamRows(self.paramList, self.paramValLst)


    def btnApplyClicked(self, evt=None):
        #check that there's either a loaded design, or that the param list isn't empty
        if (self.PC.getDesignConfigBool() == False) or (self.paramList == [] or self.paramList == None):
            wx.MessageBox('No design configuration detected.', 'Error', wx.OK | wx.ICON_ERROR)
            return        
        
        self.check_and_set_optimizer_params()
       



#######################################################
# Actions called by buttons
#
# populateDetectedKeywords()   : called by btnDetectClicked()
# check_and_set_optimizer_params() : called by btnApplyClicked()
# checkCanBeFloat()            : called by btnApplyClicked()
#
#  set_up_optimizer()          : called by btnSelectClicked()
#  export_optimizer_settings() : called by btnExportClicked()
#######################################################

# TODO This should probably be pulled out one level higher or to a different file, 
# but that needs to be hashed out with the balance between 
# UI driven controls & segmentation vs. pulling commands out of the GUI state machine


    def check_and_set_optimizer_params(self):

        #get the vals from the scrollbox
        # set vals to array/tuple
        paramInput = pd.DataFrame({})
        paramFields, originalVal, unitVal, lowerFields, upperFields, ignoreVal = self.notebook_params.getParamInputBoxVals()
        paramsCheckedCtr = 0
        for i in range(0, len(paramFields)):
            a = paramFields[i].GetValue()
            b = originalVal[i].GetValue()
            c = unitVal[i].GetValue()
            d = lowerFields[i].GetValue()
            e = upperFields[i].GetValue()
            f = ignoreVal[i].IsChecked()
            
            # check if the vals can be converted to floats (to cover ints and other number formats).
            # they dont stay floats since it's not an actual conversion.
            # check if f is UNCHECKED (being used) and originalVal value is NOT NUMERIC
            checkIsOnlyNumbers = self.checkCanBeFloat(b,f) 
            if checkIsOnlyNumbers == False:
                wx.MessageBox('Parameters used for optimization must be numbers (Int or Floats), not NaN or strings.', 'Error', wx.OK | wx.ICON_ERROR)
                return  

            paramInput[str(a)] = pd.Series([b,c,d,e,f])
            if f == False:
                paramsCheckedCtr = paramsCheckedCtr + 1
        #put params into optimizer integrator. let integrator deal with processing
       
        # set to class varriable after checking if it's a valid setup
        self.paramInput = paramInput 


        numControllable = len(self.paramInput) + 1
        msg = str(numControllable) + " controllable parameters detected."
        self.updateStatusText(msg)

        self.OI.setControllableParams(self.paramInput)
        self.notebook_optimizer.parameterSummaryUpdate(numControllable, self.paramInput)

        msg = str(paramsCheckedCtr) + " parameters selected for optimization."
        self.updateStatusText(msg)


    def populateDetectedKeywords(self, paramVals):
        #read design params into class variables
        for p in paramVals:
           self.paramList.append(str(p)) #name in list
           val = paramVals[str(p)][0] # get value by name
           self.paramValLst.append(str(val)) #set val to list


    def checkCanBeFloat(self, origVal, ignoreBool):
        # send a value from self.paramList to make sure that the string value can be converted
        # to a float. This will rule out any NaN, nan, None, True, False, or string vals
        # the optimization algs can ONLY take numbers
        try:
            if (origVal.lower()=='nan') or (origVal.lower()=='none'):
                if ignoreBool == False:
                    return False
            float(origVal)
            return True
        except:
            return False


    def set_up_optimizer(self, optimizerName, noError):
        #make sure a project has been created first, or prompt for new project
        #check if save location has been selected
        if self.PC.getProjectDirectory()== None:
            with wx.FileDialog(self, "Save antennaCAT project", wildcard="AntennaCAT files (*.ancat)|*.ancat",
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # user cancelled
                pathname = fileDialog.GetPath()
                try:
                    acp = AntennaCATProject(self.DC, self.PC, self.SO)
                    acp.createNewProject(pathname)
                except Exception as e:
                    print(e)

        #use the optimizer name to select which optimizer is now being used     
        optimizerParams = self.DC.getOptimizerParameters()

        if optimizerParams.empty == True:
            return

        self.optimizerSelected = True
            
        #check if multi-freq was enabled. If it was, duplicate vals
        if self.DC.getUseMultipleFreq() == True:
            numFreqs = self.DC.getNumMultipleFreq()
            targetMetricsTmp = []
            targetValTmp = []
            ctr = 0
            for op in optimizerParams["target_metrics"][0]:
                print(optimizerParams["target_values"][0])
                targVals = optimizerParams["target_values"][0][ctr].split(",")
                for idx in range(0, int(numFreqs)):
                    targetMetricsTmp.append(op)
                    targetValTmp.append(float(targVals[idx%len(targVals)]))
                ctr = ctr + 1
          
            # set the vals to include the duplicates
            optimizerParams["target_metrics"] = pd.Series([targetMetricsTmp])
            optimizerParams["target_values"] = pd.Series([targetValTmp])
            optimizerParams['num_output'] = pd.Series(len(targetValTmp))

            # print("optimizerParams2 in page_optimizer")
            # print(optimizerParams)
            # print(optimizerParams["target_metrics"])
            # print(optimizerParams["target_values"])

        else: # do a quick str to float conversion
            targetValTmp = []
            # print("****************************************************")
            # print("optimizerParams[target_values][0] in page_optimizer")
            # print(optimizerParams)
            # print("****************^^^^^^^^^^^^^^^********************")

            # print(optimizerParams["target_values"][0])
            try:
                for op in optimizerParams["target_values"][0]:
                    targetValTmp.append(float(op))
                optimizerParams["target_values"] = pd.Series([targetValTmp])
            except:
                noError = False
                
                # this is usually triggered when the controllable parameters aren't set
                # error messages are displayed in the parent classes, but it's still
                # possible to hit this condition.

                # this is NOT a fatal condition (yet)

               
        self.OI.setOptimizerParams(optimizerParams)

        # get the data collection bools
        saveLog, saveOptimizer, saveData = self.notebook_optimizer.getDataCollectionBools()
        self.OI.setDataCollectionBools(saveLog, saveOptimizer, saveData)


        msg = self.OI.selectOptimizer(optimizerName)
        self.updateStatusText(msg)
        if noError == True:
            # errors have been reported to user already
            self.OI.enableRun() 


    def export_optimizer_settings(self):
        
        #GET optimizer state and write out current
        st = self.OI.getState()

        d = self.OI.getOptimizerDir()
        msg = "optimizer directory is " + str(d)
        self.updateStatusText(msg)
        d = self.OI.getDataDir()
        msg = "optimizer data directory is " + str(d)
        self.updateStatusText(msg)

        # TODO: Write out    
        msg = "TODO: write out state to file"
        self.updateStatusText(msg)

        with wx.FileDialog(self, "Export optimizer state", wildcard="JSON (*.json)|*.json",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # user cancelled
            pathname = fileDialog.GetPath()
            try:
                msg = "TODO: write out. path selected " + str(pathname)
                self.updateStatusText(msg)
            except Exception as e:
                print(e)
 

#######################################################
# Error checking
#######################################################

    def errorCheck(self):
        #checks that a design and simulation script exists
        #you can genreate parameters without the scripts (preview),
        #  but not export or run
        noErrors = False
        # check design script
        if self.PC.getDesignScriptCreatedBool() == False:
            msg = "No design script created. Create or import a design to use an optimizer."
            self.updateStatusText(msg)
            return noErrors
        # check simulation script
        if self.PC.getSimulationConfigBool() == False:
            msg = "No simulation script created. Configure simulation options to use an optimizer."
            self.updateStatusText(msg)
            return noErrors
        noErrors = True
        return noErrors        
   
#######################################################
# Reloading project
#######################################################

    def applyLoadedProjectSettings(self, PC):
        self.notebook_params.applyLoadedProjectSettings(PC) 
        self.notebook_summary.applyLoadedProjectSettings(PC)

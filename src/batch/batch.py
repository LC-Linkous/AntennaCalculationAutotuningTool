##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/batch/batch.py'
#   Class for batch configuration setup to be passed to sim object
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import os
import os.path
import wx
import numpy as np
import pandas as pd


class Batch:
    def __init__(self, parent, DC, PC, SO):
        self.parent = parent
        self.DC = DC  
        self.PC = PC
        self.SO = SO

        self.paramInput = pd.DataFrame({}) #the vals from page_batch
        self.paramArr = [] #$name, minVal, maxVal, incrementSize, units
        self.paramCombinations = pd.DataFrame({}) 
        self.paramUnits = pd.DataFrame({})
        self.batchScripts = [] #temporary for debug


    def updateStatusText(self, t):
        self.parent.updateStatusText(t)


    def updateDetailsText(self, t):
        self.parent.updateDetailsText(t)


    def updateAllText(self, t):
        self.updateStatusText(t)
        self.updateDetailsText(t)


    def setInputParams(self, df):
        self.paramInput = df
        self.initialProcessing()


    def initialProcessing(self):
        #add messages to summary and details
        msg = str(len(self.paramInput)) + " controllable parameters detected."
        self.updateStatusText(msg)
        # self.updateSummaryText(msg)
        self.updateDetailsText(msg)
        #Vals for batch:
        # self.paramArr: $name, minVal, maxVal, incrementSize, units, ignoreVal
        self.paramArr = []
        for p in self.paramInput:
            nameVal = str(p)
            unitVal = self.paramInput[p][1]
            incVal = float(self.paramInput[p][5])
            ignoreVal = self.paramInput[p][6]
            if ignoreVal == True:
                # min and max are the original value
                try:
                    minVal = float(self.paramInput[p][0])
                    maxVal = float(self.paramInput[p][0])
                except:
                    # input is a val that relies on a param (e.g. $length/4)
                    minVal = str(self.paramInput[p][0])
                    maxVal = str(self.paramInput[p][0])
            else:
                # use the range vals field
                rangeArr = self.paramInput[p][4]
                rangeArr = rangeArr.replace('[', '')
                rangeArr = rangeArr.replace(']', '')
                rangeArr = rangeArr.strip()
                rangeArr = rangeArr.split(',')
                minVal = float(rangeArr[0])
                maxVal = float(rangeArr[1])            
            self.paramArr.append([nameVal, minVal, maxVal, incVal, unitVal, ignoreVal])


    def createCombinationsDataFrame(self):
        #for each param, make a list of all vals, combine, and put into dataFrame
        msg = "Combining parameters. This may take a moment."
        self.updateStatusText(msg)

        valArr=[]
        nameArr = []
        unitArr = []
        combinationCtr = 1   
        for p in self.paramArr:
            #check if ignored. if ignored, don't add to template
            if p[5] == False:
                nameArr.append(p[0])                
                minVal = p[1]
                maxVal = p[2]
                incVal = p[3]
                combArr = np.arange(minVal, maxVal+incVal, incVal)
                valArr.append(combArr)
                unitArr.append(p[4])
                msg = "Parameter " + str(p[0]) + " has " + str(len(combArr)) + \
                        " values from " + str(minVal) + " to " + str(maxVal) + "."
                self.updateDetailsText(msg)
                combinationCtr = combinationCtr * (len(combArr))
            else:
                msg = "Parameter " + str(p[0]) + " is being ignored and will not be included " +\
                    "in the adjustment template."
                self.updateDetailsText(msg)

        msg = "Design has " + str(combinationCtr) + " total combinations."
        self.updateAllText(msg)

        #prompt to continue or not
        if combinationCtr > 20000:                        
            msg = "These parameters result in a total of " + str(combinationCtr) + \
                " simulations. Continue anyways?"
            dlg = wx.MessageDialog(None, msg,'WARNING',wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                msg = "Attempting matrix meshing."
                self.updateStatusText(msg)
                
            else:
                msg = "Design attempt canceled by user."
                self.updateAllText(msg)
                return

        try:
            #use meshgrid to get all combinations of values in 2D array
            combArr = np.stack(np.meshgrid(*valArr), axis=-1).reshape(-1, len(valArr))
            msg = "Matrix mesh success."
            self.updateStatusText(msg)
        except Exception as e:
                msg = "Matrix mesh failure. " + str(combinationCtr) +  " combinations exceeds available memory. Try a larger delta."
                wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
                self.updateStatusText(msg)
                self.updateStatusText(e)
                msg = "Operation cancelled."
                self.updateStatusText(msg)
                return
        
        #read into dataframe, cols are nameArr params
        self.paramCombinations =  pd.DataFrame(combArr, columns=nameArr)
        self.paramUnits =  pd.DataFrame([unitArr], columns=nameArr)
        msg = "Operation completed with " + str(combinationCtr) + " valid combinations."
        self.updateStatusText(msg)
 
    def generateBatchScripts(self, numScripts):
        #reset these each time this func is called to gen new scripts
        self.SO.createParamEditTemplate() #reset this each time bc dont need long term mem
        batchReportDir = str(self.PC.getBatchDirectory())
        self.SO.createReportExportTemplate(batchReportDir)#start the ctr for file naming
        # ^ creates the PT object 2 levels down + starts the counter for naming scripts

        #for running scripts
        nameArr = []

        #split ranges
        # split the total number of param changes by numScripts
        msg = "Splitting scripts into " + str(int(np.floor(numScripts))) + " file(s)"
        self.updateStatusText(msg)
        splitScripts =  np.array_split(self.paramCombinations, numScripts) 

        #create each mini-batch script
        # pass in the split dataframes
        # get out a list of scripts
        
        #get script bases
        scriptDir = self.PC.getScriptDirectory()
        fileExt = self.SO.getExpectedScriptFileExtension()
        designScript = self.DC.getDesignScript()
        simulationScript = []
        if self.PC.getImportedSimulationConfigBool() == False:
           simulationScript = self.DC.getSimulationScript()
         
        ctr = 0
        for miniBatch in splitScripts:
            outScript = []
            ctr =  ctr + 1
            miniBatch = miniBatch.reset_index(drop=True)#reset so the original index isn't split into the new dfs
            singleScript = self.SO.batchTemplateGen(miniBatch, self.paramUnits)
            # batchScripts.append(singleScript)
            self.DC.addBatchScript(singleScript)

            #merge script texts
            outScript.extend(designScript)
            #editing here to see if this gets rid of the first dropped sim
            outScript.extend(simulationScript)
            outScript.extend(singleScript)
            #write out to the scripts file  in the antennaCAT project
            try:
                pathname = os.path.join(scriptDir, str(ctr) + "-exported-batch" + str(fileExt))
                nameArr.append(pathname)
                with open(pathname, 'w') as f:
                    for line in outScript:
                        for li in line:
                            f.writelines(li)
                msg = "file exported to " + str(pathname)
                self.updateStatusText(msg)
            except Exception as e:
                    msg = "Cannot save current data in file " + str(pathname)
                    self.updateStatusText(msg)
                    self.updateStatusText(e)

        return nameArr


    def applyLoadedProjectSettings(self, PC):
        pass
##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/data_processing/data_processing_ANSYS.py'
#   Class for calculating target metrics from optimization
#       class-based for managing changing EM software
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os
import pandas as pd
import numpy as np
##################################################
# optimizer data processing using default files
##################################################

class DataProcessing_ANSYS():
    def __init__(self):

        #default data file names
        self.dataDir = None
        self.antennaParamDataTableFile = "Antenna Params Table.csv"
        self.rectangularPlotFile = "Modal S Parameter Rectangular Plot.csv"

    def getDefaultOptimizerSimulationData(self, dataDir):
        # return data from:
        #   rectangular plot: s11, BW
        #   antenna Parameter Data table: Peak Directivity, Peak Gain, TotalEfficiency
        self.dataDir = dataDir
        df = pd.DataFrame({})
        apdtFilepath = os.path.join(self.dataDir,self.antennaParamDataTableFile)
        targetFreq, pDir, pGain, tEff = self.getAntennaParameterDataTable(apdtFilepath)
        rpFilepath = os.path.join(self.dataDir,self.rectangularPlotFile)
        s11, bw = self.getResonanceAtFreq(rpFilepath, targetFreq)
        df['directivity'] = pd.Series([pDir])
        df['gain'] = pd.Series([pGain])
        df['efficiency'] = pd.Series([tEff])
        df['s11'] = pd.Series([s11])
        df['bw'] = pd.Series([bw])
        return df

    def getAntennaParameterDataTable(self, filepath):
        # report: antenna parameter data table
        # default exports: "dB(PeakDirectivity)","dB(PeakGain)","TotalEfficiency", "BeamArea"
        df, noError = self.readInCSV(filepath)
        if noError == False: return None, None, None, None
        
        targetFreq = df.iloc[:, 0].tolist()
        peakDirectivity = df.iloc[:, 1].tolist()
        peakGain = df.iloc[:, 2].tolist() 
        totalEfficiency = df.iloc[:, 3].tolist()
        return targetFreq, peakDirectivity, peakGain, totalEfficiency

    def getResonanceAtFreq(self, filepath, targetFreq):
        # report: rectangular plot, modal or terminal
        #default exports: "dB(S(1,1))"
        #this function gets the s11 at the closest point to the target freq
        # that is, the data points sampled might not be perfectly at the 
        # target freq, so get the closest
        df, noError = self.readInCSV(filepath)
        if noError == False: return None, None#, None

        s11Arr = []
        bwArr = []

        for tf in targetFreq:
            #default vals
            s11 = 0
            bw = 0

            freqCol = df.iloc[:,0]
            s11Col = df.iloc[:,1]

            # find dB(s11) at closest value to target freq
            # this catches cases where the intervals of the sweep dont include the exact target freq
            closestFreqIdx = (np.abs(freqCol-tf)).argmin()
            # print(closestFreqIdx)
            # print(freqCol[closestFreqIdx])
            s11 = s11Col[closestFreqIdx]

            # calculate bw
            if s11 > -10: #not -10dB at resonance, so 0 bandwidth automatically
                s11Arr.append(s11)
                bwArr.append(bw)
            else:
                s11Arr.append(s11)
                # use that closest val and search both directions until vals greater than -10dB
                lowF = freqCol[closestFreqIdx]
                lowS11 = s11
                highF = freqCol[closestFreqIdx]
                highS11 = s11
                #find lowest freq
                for idx in reversed(range(0,closestFreqIdx)):
                    newS11 = s11Col[idx]
                    if (newS11 <= lowS11) and (newS11<=-10):
                        lowS11 = newS11
                        lowF = freqCol[idx]
                    if (newS11>-10):
                        break
                #find highest freq
                for idx in range(closestFreqIdx, len(freqCol)):
                    newS11 = s11Col[idx]
                    if (newS11 <= highS11) and (newS11<=-10):
                        highS11 = newS11
                        highF = freqCol[idx]
                    if (newS11>-10):
                        break

                #substract to get bw
                bw = highF-lowF
                bwArr.append(bw)

        return s11Arr, bwArr
        




    ##################################################
    # csv/data manipulation and processing
    ##################################################

    def readInCSV(self, file):
        noError = True
        data = None
        if os.path.isfile(file) == False:
            print("ERROR: data_processing_ANSYS.py. path error to exported data file. check simulation for error")
            print("attempted filepath: ", file)
            noError = False
            return data, noError

        # read in CSV data
        data = pd.read_csv(file)
        return data, noError




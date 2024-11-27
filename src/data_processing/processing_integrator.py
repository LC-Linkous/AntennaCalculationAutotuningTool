##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/data_processing/processing_integrator.py'
#   Main class for managing the data processing hooks
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

from data_processing.data_processing_ANSYS import DataProcessing_ANSYS

class DataProcessingIntegrator():
    def __init__(self,softwareSelection): 
        # class may be created before config uploaded
        self.DP = None # data processing class obj
        self.selectDataProcessor(softwareSelection)

    def selectDataProcessor(self, softwareSelection):
        if softwareSelection == "ANSYS":
           self.DP = DataProcessing_ANSYS()
        elif softwareSelection == "COMSOL":
           self.DP = None
        elif softwareSelection == "CST":
           self.DP = None
        elif softwareSelection == "EMPIRE":
           self.DP = None
        elif softwareSelection == "FEKO":
           self.DP = None

    #TODO: give these less terrible names as they get finalized
    def getDefaultOptimizerSimulationData(self, dataDir):
        # get the default metrics
        return self.DP.getDefaultOptimizerSimulationData(dataDir)


    def getAntennaParameterDataTable(self, filepath):
        return self.DP.getAntennaParameterDataTable(filepath)
    
    def getResonanceAtFreq(self, targetFreq, filepath):
        return self.DP.getResonanceAtFreq(targetFreq, filepath)

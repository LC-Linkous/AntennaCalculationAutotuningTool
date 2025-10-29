##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/replicator.py'
#   Class for creating designs using templates for replication studies
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: October 29, 2025
##--------------------------------------------------------------------\

import sys
import os
import logging
logger = logging.getLogger(__name__)

import project.config.antennaCAT_config as c

CALCULATOR_EXPORT_LIST = c.CALCULATOR_EXPORT_LIST

class Replicator():
    def __init__(self, DC, aType, panelFeats):
        self.DC = DC
        self.aType = aType
        self.calcPanelFeatures = panelFeats
        
    def setupAntennaParams(self, panelParams):
        errMsg = None
        #pull UI vals to set antenna configuration to shared object         
        aFt = [["antenna_type", self.aType]]
        self.DC.setAllFeaturesByName(aFt)
        self.DC.setAllFeaturesByName(self.calcPanelFeatures)
        self.DC.setAllParamsByName(panelParams)
        return errMsg
    
   
    def exportSelections(self, filePath, dxfBool, pngBool, gerberBool):
        errMsg = None
        features = self.DC.getFeatures()
        aType = features["antenna_type"][0]
        if aType not in CALCULATOR_EXPORT_LIST:
            errMsg = "unable to export topology. this feature has not been added yet"
            return errMsg
        
        if aType == 'rep_rectangular_patch':
            fType =  features["feed_type"][0]
            if fType == 'microstrip':
                self.exportMicrostripRectangularPatch(filePath, dxfBool, pngBool, gerberBool)
            else:
                self.exportProbeRectangularPatch(filePath, dxfBool, pngBool, gerberBool)
        return errMsg

    def exportMicrostripRectangularPatch(self, filePath, dxfBool, pngBool, gerberBool):
        print("EXPORTING FROM REPLICATOR.PY DOES NOT EXIST YET")
        logger.info("WARNING: feature does not exist. exporting microstrip rectangular patch from replicator.py is not yet supported")

    def exportProbeRectangularPatch(self, filePath, dxfBool, pngBool, gerberBool):
        print("EXPORTING FROM REPLICATOR.PY DOES NOT EXIST YET")
        logger.info("WARNING: feature does not exist. exporting probe fed rectangular patch from replicator.py is not yet supported")
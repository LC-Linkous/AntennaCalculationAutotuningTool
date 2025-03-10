##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/generator/calculator.py'
#   Class interfacing with the internal antenna calculator
#   Antenna calculator from: https://github.com/Dollarhyde/AntennaCalculator
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import sys
import os

import project.config.antennaCAT_config as c
sys.path.insert(0, './AntenaCalculator')
from AntennaCalculator.antenna_calculator import AntennaCalculator

CALCULATOR_EXPORT_LIST = c.CALCULATOR_EXPORT_LIST

class Calculator():
    def __init__(self, DC, aType, panelFeats):
        self.DC = DC
        self.aType = aType
        self.calcPanelFeatures = panelFeats
        
    def calculateAntennaParams(self, altX0Bool):
        errMsg = None
        #pull UI vals to set antenna configuration to shared object         
        aFt = [["antenna_type", self.aType]]
        self.DC.setAllFeaturesByName(aFt)
        self.DC.setAllFeaturesByName(self.calcPanelFeatures)
        #call to func that formats the calculator project call
        inputParams = self.setCalculatorArgParams()
        # call to AntennaCalc project
        try:
            calcedParams = self.callCalculator(inputParams)
        except Exception as e:
            errMsg = "Invalid configuration detected in calculator"
            return errMsg

        #convert from meters to millimeters
        calcedParams = self.convertFromMetersToMillimeters(calcedParams)
        #update Antenna Config with calculated vars
        if self.aType == 'rectangular_patch': 
            fType = self.DC.getFeaturesByName('feed_type')
            if altX0Bool == True: #use L/4 for X0
                x0 = float(calcedParams[1])/4
            else:
                x0 = calcedParams[2]
            if (fType == 'microstrip') or (fType == 'probe'):
                if fType == 'probe':
                    sw = None
                else:
                    sw = calcedParams[4]
                paramArr = [["width", calcedParams[0]],
                    ["length", calcedParams[1]],
                    ["x0", x0],
                    ["y0", calcedParams[3]],
                    ["gap", float(1)],
                    ["strip_width", sw],
                    ["substrate_length", 2*calcedParams[1]],
                    ["substrate_width", 2*calcedParams[0]],
                    ["ground_plane_width", 2*calcedParams[0]],
                    ["ground_plane_length", 2*calcedParams[1]],
                    ["conductor_height", None],
                    ["substrate_height", self.DC.getFeaturesByName('substrate_height')]]


            else:
                errMsg = errMsg + "ERROR: unrecognized feed type. check dictionary imports"
                return errMsg
 
        
        elif self.aType == 'half_wave_dipole':
            paramArr = [["length", calcedParams[0]],
                        ["half_length",float(calcedParams[0])/2],
                        ["conductor_radius", self.DC.getFeaturesByName('conductor_radius')],
                        ["feed_gap", self.DC.getFeaturesByName('feed_gap')]]

        elif self.aType == 'quarter_wave_monopole':
            paramArr = [["length", calcedParams[0]],
                        ["conductor_radius", self.DC.getFeaturesByName('conductor_radius')],
                        ["ground_plane_radius", self.DC.getFeaturesByName('ground_plane_radius')],
                        ["feed_gap", self.DC.getFeaturesByName('feed_gap')]]


        self.DC.setAllParamsByName(paramArr)
        return errMsg
    
    
    def callCalculator(self, args):
        shell = AntennaCalculator(args)
        args = shell.getArgs()
        shell.main(args)
        calcedParams = shell.getCalcedParams()
        return calcedParams


    def convertFromMetersToMillimeters(self, params):
        convertedParams = []
        if type(params) == tuple: #rectangular patch
            for p in params:
                pmm = float(p)*1000
                convertedParams.append(pmm)
        elif type(params)== float:  #monopole, dipole
            pmm = float(params)*1000
            convertedParams.append(pmm)
        return convertedParams
    
    
    def setCalculatorArgParams(self):
        ap = []
        features = self.DC.getFeatures()
        atype = features["antenna_type"][0]
        if atype == 'rectangular_patch':
            f =  features["simulation_frequency"][0]
            er =  features["dielectric"][0]
            h =  str(float(features["substrate_height"][0])/1000) #convert to meters for calculator
            ty =  features["feed_type"][0]
            ap = ['rectangular_patch',
                  '-f', str(f),
                  '-er',str(er),
                  '-h', str(h),
                  '--type', str(ty),
                  '--variable_return']
        elif atype == 'half_wave_dipole':
            f =  features["simulation_frequency"][0]
            ap = ['half_wave_dipole',
                  '-f', str(f),
                  '--variable_return']
        elif atype == 'quarter_wave_monopole':
            f =  features["simulation_frequency"][0]
            ap = ['quarter_wave_monopole',
                  '-f', str(f),
                  '--variable_return']
        return ap

    def exportSelections(self, filePath, dxfBool, pngBool, gerberBool):
        errMsg = None
        features = self.DC.getFeatures()
        aType = features["antenna_type"][0]
        if aType not in CALCULATOR_EXPORT_LIST:
            errMsg = "unable to export topology. this feature has not been added yet"
            return errMsg
        
        if aType == 'rectangular_patch':
            fType =  features["feed_type"][0]
            if fType == 'microstrip':
                self.exportMicrostripRectangularPatch(filePath, dxfBool, pngBool, gerberBool)
            else:
                self.exportProbeRectangularPatch(filePath, dxfBool, pngBool, gerberBool)
        return errMsg

    def exportMicrostripRectangularPatch(self, filePath, dxfBool, pngBool, gerberBool):
        features = self.DC.getFeatures()
        atype = features["antenna_type"][0]
        fType =  features["feed_type"][0]

        #search with the leading character
        sw = self.DC.getParamsByName("strip_width", unconverted=True)
        w = self.DC.getParamsByName("width", unconverted=True)
        l = self.DC.getParamsByName("length", unconverted=True)
        x0 = self.DC.getParamsByName("x0", unconverted=True)
        y0 = self.DC.getParamsByName("y0", unconverted=True)

        basePath = os.path.join(filePath, str(atype))
        if dxfBool == True:
            ap = []
            pth = str(basePath + ".dxf")
            ap = ['rectangular_patch_export',
                    '--type', str(fType),
                    '-W', str(w),
                    '-L', str(l),
                    '-x0', str(x0),
                    '-y0', str(y0),
                    '-ws', str(sw),
                    '--dxfoutput', pth]
            self.callCalculator(ap)
        if pngBool == True:
            ap = []
            pth = str(basePath + ".png")
            ap = ['rectangular_patch_export',
                '--type', str(fType),
                '-W', str(w),
                '-L', str(l),
                '-x0', str(x0),
                '-y0', str(y0),
                '-ws', str(sw),
                '--pngoutput', pth]
            self.callCalculator(ap)
        if gerberBool == True:
            ap = []
            pth = str(basePath) #no extension
            ap = ['rectangular_patch_export',
                '--type', str(fType),
                '-W', str(w),
                '-L', str(l),
                '-x0', str(x0),
                '-y0', str(y0),
                '-ws', str(sw),
                '--gerberoutput', pth]
            self.callCalculator(ap)

    def exportProbeRectangularPatch(self, filePath, dxfBool, pngBool, gerberBool):
        features = self.DC.getFeatures()
        atype = features["antenna_type"][0]
        fType =  features["feed_type"][0]
        w = self.DC.getParamsByName("width", unconverted=True)
        l = self.DC.getParamsByName("length", unconverted=True)
        x0 = self.DC.getParamsByName("x0", unconverted=True)
        y0 = self.DC.getParamsByName("y0", unconverted=True)

        basePath =  os.path.join(filePath, str(atype))
        if dxfBool == True:
            ap = []
            pth = str(basePath + ".dxf")
            ap = ['rectangular_patch_export',
                '--type', str(fType),
                '-W', str(w),
                '-L', str(l),
                '-x0', str(x0),
                '-y0', str(y0),
                '--dxfoutput', pth]
            self.callCalculator(ap)
        if pngBool == True:
            ap = []
            pth = str(basePath + ".png")
            ap = ['rectangular_patch_export',
                '--type', str(fType),
                '-W', str(w),
                '-L', str(l),
                '-x0', str(x0),
                '-y0', str(y0),
                '--pngoutput', pth]
            self.callCalculator(ap)
        if gerberBool == True:
            ap = []
            pth = str(basePath) #no extension
            ap = ['rectangular_patch_export',
                '--type', str(fType),
                '-W', str(w),
                '-L', str(l),
                '-x0', str(x0),
                '-y0', str(y0),
                '--gerberoutput', pth]
            self.callCalculator(ap)

    
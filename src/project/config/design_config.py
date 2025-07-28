##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/config/design_config.py'
#   Class for storing calculated and UI antenna/design values
#   This class contains values that will change between iterations
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 16, 2024
##--------------------------------------------------------------------\

import pandas as pd

class DesignConfiguration:
    def __init__(self):

        # data structures
        # physical model design
        self.designParams = pd.DataFrame({})     #the calculated or provided params sorted by name
        self.designFeatures = pd.DataFrame({})   # values such as the layer composition or num elements
        # precision settings - these are used with the calculator and 
        #       other vals so often it's easier to make them a design config than a project config
        self.numericalPrecisionParameters = pd.DataFrame({})
        self.numericalPrecisionParameters["default_units"] = pd.Series('mm')
        self.numericalPrecisionParameters["numerical_precision"] = pd.Series(4)
        #optimizer
        self.optimizerParameters = pd.DataFrame({})
        # simulation
        self.simulationSettings = pd.DataFrame({})
        self.simulationSettings["simulation_frequency"] = pd.Series(2.4e9)
        self.simulationSettings["use_multiple_freq"] = pd.Series(False)
        self.simulationSettings["num_multiple_freq"] = pd.Series(0)
        self.simulationSettings["use_multiple_delta"] = pd.Series(False)
        self.simulationSettings["min_sim_range"] = pd.Series(1.5e9)
        self.simulationSettings["max_sim_range"] = pd.Series(3.5e9)
        self.simulationSettings["num_passes"] = pd.Series(6)
        self.simulationSettings["max_delta"] = pd.Series(0.002)
        self.simulationSettings["num_sim_points"] = pd.Series(401)

        self.simulationReports = pd.DataFrame({})
        self.simulationReports["terminal_report_list"] = pd.Series(False)
        self.simulationReports["terminal_features"] = pd.Series(False)
        self.simulationReports["terminal_functions"] = pd.Series(False)
        self.simulationReports["modal_report_list"] = pd.Series(False)
        self.simulationReports["modal_features"] = pd.Series(False)
        self.simulationReports["modal_functions"] = pd.Series(False)
        self.simulationReports["far_field_report_list"] = pd.Series(False)
        self.simulationReports["far_field_features"] = pd.Series(False)
        self.simulationReports["far_field_functions"] = pd.Series(False)
        self.simulationReports["data_table_modal_features"] = pd.Series(False)
        # self.simulationReports["data_table_modal_functions"] = []
        self.simulationReports["data_table_terminal_features"] = pd.Series(False)
        # self.simulationReports["data_table_terminal_functions"] = []
        self.simulationReports["data_table_far_field_features"] = pd.Series(False)
        self.simulationReports["antenna_parameter_table_features"] =  pd.Series(False)

        #arrays used for saving templates - these are CREATED in the simulation integrator
        # not all of these are going to stay - thay'll be phased out with debugging
        self.importedScript = [] #for preservation
        self.designScript = []
        self.simulationScript = []
        self.reportsScript = []
        self.batchScript = [] #might be 2D
        self.lastParamEditScript = [] #not all param edits (might be used by tuning)
        self.reportExportScript = []


        #layers 
        self.conductorLayers = []
        self.substrateLayers = []
        self.superstrateLayers = []
        # bend & shape
        # TODO


        #quick convert
        self.leadChar = ""
   
    def clearConfig(self):
        # scripts
        # physical model design
        self.designParams = pd.DataFrame({})     #the calculated or provided params sorted by name
        self.designFeatures = pd.DataFrame({})   # values such as the layer composition or num elements
        
        # numerical precision
        self.numericalPrecisionParameters = pd.DataFrame({})
        self.numericalPrecisionParameters["default_units"] = pd.Series('mm')
        self.numericalPrecisionParameters["numerical_precision"] = pd.Series(4)
        
        # simulation
        self.simulationSettings = pd.DataFrame({})
        self.simulationSettings["simulation_frequency"] = pd.Series(2.4e9)
        self.simulationSettings["use_multiple_freq"] = pd.Series(False)
        self.simulationSettings["num_multiple_freq"] = pd.Series(0)
        self.simulationSettings["min_sim_range"] = pd.Series(1.5e9)
        self.simulationSettings["max_sim_range"] = pd.Series(3.5e9)
        self.simulationSettings["num_passes"] = pd.Series(6)
        self.simulationSettings["max_delta"] = pd.Series(0.002)
        self.simulationSettings["use_multiple_delta"] = pd.Series(False)
        self.simulationSettings["num_sim_points"] = pd.Series(401)

        self.simulationReports = pd.DataFrame({})
        self.simulationReports["terminal_report_list"] = pd.Series(False)
        self.simulationReports["terminal_features"] = pd.Series(False)
        self.simulationReports["terminal_functions"] = pd.Series(False)
        self.simulationReports["modal_report_list"] = pd.Series(False)
        self.simulationReports["modal_features"] = pd.Series(False)
        self.simulationReports["modal_functions"] = pd.Series(False)
        self.simulationReports["far_field_report_list"] = pd.Series(False)
        self.simulationReports["far_field_features"] = pd.Series(False)
        self.simulationReports["far_field_functions"] = pd.Series(False)
        self.simulationReports["data_table_modal_features"] = pd.Series(False)
        # self.simulationReports["data_table_modal_functions"] = []
        self.simulationReports["data_table_terminal_features"] = pd.Series(False)
        # self.simulationReports["data_table_terminal_functions"] = []
        self.simulationReports["data_table_far_field_features"] =  pd.Series(False)
        self.simulationReports["antenna_parameter_table_features"] =  pd.Series(False)

        self.importedScript = [] #for preservation
        self.designScript = []
        self.simulationScript = []
        self.reportsScript=[]
        self.batchScript = [] #might be 2D
        self.lastParamEditScript = [] #not all param edits (might be used by tuning)
        self.reportExportScript = []
    
    ##################################################
    # script variables
    #
    #################################################

    # imported script, read in from design
    # for preserving original script
    def setImportedScript(self, s):
        self.importedScript = s
    
    def getImportedScript(self):
        return self.importedScript

    def clearImportedScript(self):
        self.importedScript = []

    # general design base - might be merged with multiple features
    def setDesignScript(self, s):
        self.designScript = s
    
    def getDesignScript(self):
        #main script to pull for design export/merge
        return self.designScript

    def clearDesignScript(self):
        self.designScript = []
    
    # simulation script - for setting up sim analysis
    def setSimulationScript(self, s):
        self.simulationScript = s

    def addSimulationScript(self, s):
        self.simulationScript.append(s)
    
    def getSimulationScript(self):
        return self.simulationScript

    def clearSimulationScript(self):
        self.simulationScript = []

    def setReportsScript(self, s):
        self.reportsScript = s

    def addReportsScript(self, s):
        self.reportsScript.append(s)
    
    def getReportsScript(self):
        return self.reportsScript

    def clearReportsScript(self):
        self.reportsScript = []

    def setBatchScript(self, s):
         self.batchScript = s
        
    def addBatchScript(self, s):
        self.batchScript.append(s)

    def getBatchScript(self):
        return self.addBatchScript

    def clearBatchScript(self):
        self.batchScript = []


    #################################################
    # set and get design parameters
    # 
    # these values are provided or calculated
    # NUMBERS ONLY - makes the math easier
    #################################################

    def setAllParamsByName(self, arr):
        for a in arr:
            self.setParamsByName(n=a[0], val=a[1])

    def setParamsByName(self, n, val):
        self.designParams[str(n)] = pd.Series(val)

    def getParamsByName(self, n, unconverted=False):
        if unconverted == False:
            # dont need the leading character to search
            return self.designParams[str(n)][0]
        else:
            #calculator template call needing values that 
            # weren't updated to match the EM sim software names.
            # add leading char before searchinf
            n = self.leadChar + str(n)
            return self.designParams[str(n)][0]

    def getParams(self):
        #returns all a params set in the class
        return self.designParams

    def setParams(self, df):
        self.designParams = df
  
    def clearParams(self):
        #resets to calculator basics
        # self.designParams = pd.DataFrame({})     #the calculated or provided params sorted by name
        del  self.designParams # hard delete
        self.designParams = pd.DataFrame({})

    def setLeadChar(self, EMsoftware):
        self.leadChar = ""
        if EMsoftware == 'ANSYS':
            self.leadChar = "$"
        elif EMsoftware == 'COMSOL':
            self.leadChar = ""
        elif EMsoftware == 'CST':
            self.leadChar = ""
        elif EMsoftware == 'EMPIRE':
            self.leadChar = ""
        elif EMsoftware == 'FEKO':
            self.leadChar = ""

    #
    # Numerical precision and default units
    #

    def setDefaultUnits(self, units):
        self.numericalPrecisionParameters["default_units"] = pd.Series(units)

    def getDefaultUnits(self):
       return  self.numericalPrecisionParameters["default_units"][0]

    def setNumericalPrecision(self, i):
        self.numericalPrecisionParameters["numerical_precision"] = pd.Series(i)

    def getNumericalPrecision(self):
       return  self.numericalPrecisionParameters["numerical_precision"][0]
    


#************************************************************************       
# These couple conversion sections are a mess due to some late additions 
#   with features and multi-EM compatibility. They're getting cleaned up,
#   but are ugly in the meantime.
#************************************************************************    
    def convertParamName(self, pName, EMsoftware, returnGeneral=True):
        #input pName is array
        #convert naming convention between general (no lead characters) and EM software conventions
        cName = []
        
        if returnGeneral == True: 

            for p in pName:
                cName.append(str(p[1:]))#strip lead character

        else: #return converted name
            self.leadChar = ""
            if EMsoftware == 'ANSYS':
                self.leadChar = "$"
            elif EMsoftware == 'COMSOL':
                self.leadChar = ""
            elif EMsoftware == 'CST':
                self.leadChar = ""
            elif EMsoftware == 'EMPIRE':
                self.leadChar = ""
            elif EMsoftware == 'FEKO':
                self.leadChar = ""

            for p in pName:
                cName.append(str(self.leadChar + p))        
        return cName

    def convertParamFormat(self, params, EMsoftware):
        #make the param name match the format expected for the EM software conventions
        #done on returned var bc users may switch the software
        #input: params in dataframe, EM software from project_config        
        convertedParams = pd.DataFrame({})
        self.leadChar = ""
        if EMsoftware == 'ANSYS':
            self.leadChar = "$"
        elif EMsoftware == 'COMSOL':
            self.leadChar = ""
        elif EMsoftware == 'CST':
            self.leadChar = ""
        elif EMsoftware == 'EMPIRE':
            self.leadChar = ""
        elif EMsoftware == 'FEKO':
            self.leadChar = ""

        for p in params:
            name = str(p)
            name = self.leadChar + name
            val =  params[str(p)][0]
            convertedParams[str(name)] = pd.Series([val])

        return convertedParams
    
    #################################################
    # set and get design features
    # 
    # antenna type, feed type, layer heights, layer materials
    # may be copied into other DF objects
    #################################################

    def setAllFeaturesByName(self, arr):
        for a in arr:
            self.setFeaturesByName(n=a[0], val=a[1])

    def setFeaturesByName(self, n, val):
        self.designFeatures[str(n)] = pd.Series(val)

    def getFeaturesByName(self, n):
        return self.designFeatures[str(n)][0]

    def getFeatures(self):
        #returns all a features set in the class
        return self.designFeatures
    
    def clearFeatures(self):
        #resets to calculator basics
        self.designFeatures = pd.DataFrame({})   # values such as the layer composition or num elements

    #################################################
    # set and get reports
    # 
    # these functions are for triggering when reports are run 
    # these were originally sorted based on Ansys HFSS categories, 
    # so this is step 1 of generalization
    #################################################

    def setReportsByName(self, rt, l):
        # if l == []: #leave this bc might be needed for proper reset
        #     return
        # clear the col of the main df so deleted vals are overwritten
        self.simulationReports[str(rt)] = pd.Series([])
        # new df for combination
        tmpDf = pd.DataFrame(l, columns=[str(rt)])
        #combine
        self.simulationReports = tmpDf.combine_first(self.simulationReports)

    def getReportsByCategory(self, ct):
        return self.simulationReports[str(ct)]

    def getReports(self):
        #returns all a params set in the class
        return self.simulationReports

    def setModalReportList(self, lReports, lFeatures):
        self.setReportsByName("modal_report_list", lReports)
        self.setReportsByName("modal_features", lFeatures)
        # self.setReportsByName("modal_functions", lFunctions)

    def getModalReportList(self):
        #returns just the list of reports by name. not user set vals
        return self.simulationReports["modal_report_list"]

    def getModalFeaturesList(self):
        return self.simulationReports["modal_features"]
    
    # def getModalFunctionsList(self):
    #     return self.simulationReports["modal_functions"]

    def setTerminalReportList(self, lReports, lFeatures):
        self.setReportsByName("terminal_report_list", lReports)
        self.setReportsByName("terminal_features", lFeatures)
        # self.setReportsByName("terminal_functions", lFunctions)

    def getTerminalReportList(self):
        #returns just the list of reports by name. not user set vals
        return self.simulationReports["terminal_report_list"]
    
    def getTerminalFeaturesList(self):
        return self.simulationReports["terminal_features"]
    
    # def getTerminalFunctionsList(self):
    #     return self.simulationReports["terminal_functions"]

    def setFarFieldReportList(self, lReports, lFeatures):
        self.setReportsByName("far_field_report_list", lReports)
        self.setReportsByName("far_field_features", lFeatures)
        # self.setReportsByName("far_field_functions", lFunctions)

    def getFarFieldReportList(self):
        #returns just the list of reports by name. not user set vals
        return self.simulationReports["far_field_report_list"]
    
    def getFarFieldFeaturesList(self):
        return self.simulationReports["far_field_features"]
    
    # def getFarFieldFunctionsList(self):
    #     return self.simulationReports["far_field_functions"]

    def setDataTableReportList(self, DTMFeats, DTTFeats, FFFeats):
        self.setReportsByName("data_table_modal_features", DTMFeats)
        # self.setReportsByName("data_table_modal_functions", DTMFuncs)
        self.setReportsByName("data_table_terminal_features", DTTFeats)
        # self.setReportsByName("data_table_terminal_functions", DTTFuncs)
        self.setReportsByName("data_table_far_field_features", FFFeats)

    def getDataTableModalFeaturesList(self):
        #returns just the list of reports by name. not user set vals
        return self.simulationReports["data_table_modal_features"]

    # def getDataTableModalFunctionsList(self):
    #     return self.simulationReports["data_table_modal_functions"]
    
    def getDataTableTerminalFeaturesList(self):
        return self.simulationReports["data_table_terminal_features"]
    
    # def getDataTableTerminalFunctionsList(self):
    #     return self.simulationReports["data_table_terminal_functions"]
    
    def getDataTableFarFieldFeaturesList(self):
        return self.simulationReports["data_table_far_field_features"]


    def setAntennaParamTableList(self, antennaParamFts):
        self.setReportsByName("antenna_parameter_table_features", antennaParamFts)

    def getAntennaParamTableList(self):
        return self.simulationReports["antenna_parameter_table_features"]

    #################################################
    # vals for simulation settings as set by user
    # these are generic enough to use in multiple simulation softwares
    #
    #################################################

    def setSimulationFreq(self, n):
        self.simulationSettings["simulation_frequency"] = pd.Series(str(n)) #store as str to catch multi

    def getSimulationFreq(self):
        return self.simulationSettings["simulation_frequency"][0]
    
    def setUseMultipleFreq(self, n):
        self.simulationSettings["use_multiple_freq"] = pd.Series(bool(n))

    def getUseMultipleFreq(self):
        return self.simulationSettings["use_multiple_freq"][0]    

    def setNumMultipleFreq(self, n):
        self.simulationSettings["num_multiple_freq"] = pd.Series(float(n))

    def getNumMultipleFreq(self):
        return self.simulationSettings["num_multiple_freq"][0]    

    def setMinSimRange(self, n):
        self.simulationSettings["min_sim_range"] = pd.Series(float(n))

    def getMinSimRange(self):
        return self.simulationSettings["min_sim_range"][0]

    def setMaxSimRange(self, n):
        self.simulationSettings["max_sim_range"] = pd.Series(float(n))

    def getMaxSimRange(self):
        return self.simulationSettings["max_sim_range"][0]

    def setNumPasses(self, n):
        self.simulationSettings["num_passes"] = pd.Series(float(n))

    def getNumPasses(self):
        return self.simulationSettings["num_passes"][0]

    def setMaxDelta(self, n):
        self.simulationSettings["max_delta"] = pd.Series(str(n))

    def getMaxDelta(self):
        return self.simulationSettings["max_delta"][0]
    
    def setUseMultipleDelta(self, n):
        self.simulationSettings["use_multiple_delta"] = pd.Series(bool(n))
    
    def getUseMultipleDelta(self):
        return self.simulationSettings["use_multiple_delta"][0]

    def setNumSimPts(self, n):
        self.simulationSettings["num_sim_points"] = pd.Series(float(n))

    def getNumSimPts(self):
        return self.simulationSettings["num_sim_points"][0]

    def setSimulationSettingsDF(self, cf, useMultF,numMultF, minR, maxR, numPass, maxDel, useMultD, numSP):
        self.simulationSettings["simulation_frequency"] = pd.Series(cf) 
        self.simulationSettings["use_multiple_freq"] = pd.Series(useMultF)
        self.simulationSettings["num_multiple_freq"] = pd.Series(numMultF)
        self.simulationSettings["min_sim_range"] = pd.Series(minR)
        self.simulationSettings["max_sim_range"] = pd.Series(maxR)
        self.simulationSettings["num_passes"] = pd.Series(numPass)
        self.simulationSettings["max_delta"] = pd.Series(maxDel)
        self.simulationSettings["use_multiple_delta"] = pd.Series(useMultD)
        self.simulationSettings["num_sim_points"] = pd.Series(numSP)

    #################################################
    #  Optimizer Params
    #################################################

    def setOptimizerParameters(self, df):
        self.optimizerParameters = df

    def getOptimizerParameters(self):
        return self.optimizerParameters 
    


    #################################################
    # Values for layers, bend, shape, etc
    #################################################

    def setConstructorLayers(self, arr):
        self.conductorLayers = arr

    def getConstructorLayers(self):
        return self.conductorLayers 

    def setSubstrateLayers(self, arr):
        self.substrateLayers = arr

    def getSubstrateLayers(self):
        return self.substrateLayers 
    
    def setSuperstrateLayers(self, arr):
        self.superstrateLayers = arr

    def getSuperstrateLayers(self):
        return self.superstrateLayers 


    #################################################
    # EXPORT
    #################################################

    def export_DC(self):
        # This is turned into a dataframe and exported properly in the driver class.
        # That way the file format and naming are always set to whatever the most updated version is

        DC_export = {            
            # dataframes
            'df_designParams': [self.designParams],
            'df_designFeatures': [self.designFeatures],
            'df_numericalPrecisionParameters': [self.numericalPrecisionParameters],
            'df_optimizerParameters': [self.optimizerParameters],
            'df_simulationSettings': [self.simulationSettings],
            'df_simulationReports': [self.simulationReports],
            'arr_importedScript': [self.importedScript],
            'arr_designScript': [self.designScript],
            'arr_simulationScript': [self.simulationScript],
            'arr_reportsScript': [self.reportsScript],
            'arr_batchScript': [self.batchScript],
            'arr_lastParamEditScript': [self.lastParamEditScript],
            'arr_reportExportScript': [self.reportExportScript],
            'arr_conductorLayers': [self.conductorLayers],
            'arr_substrateLayers': [self.substrateLayers],
            'arr_superstrateLayers': [self.superstrateLayers]}        
       
        return DC_export # this is turned into a dataframe in the driver class
    

    #################################################
    # IMPORT
    #################################################

    def import_DC(self, DC_import):
        # DC_import is a DF of DFs

        noError = False

        try:

            self.designParams= DC_import['df_designParams'][0] 
            self.designFeatures= DC_import['df_designFeatures'][0] 
            self.numericalPrecisionParameters= DC_import['df_numericalPrecisionParameters'][0] 
            self.optimizerParameters= DC_import['df_optimizerParameters'][0] 
            self.simulationSettings= DC_import['df_simulationSettings'][0] 
            self.simulationReports= DC_import['df_simulationReports'][0] 
            self.importedScript= DC_import['arr_importedScript'][0] 

            self.designScript= DC_import['arr_designScript'][0]
            self.simulationScript= DC_import['arr_simulationScript'][0]
            self.reportsScript= DC_import['arr_reportsScript'][0]
            self.batchScript= DC_import['arr_batchScript'][0]
            self.lastParamEditScript= DC_import['arr_lastParamEditScript'][0]
            self.reportExportScript= DC_import['arr_reportExportScript'][0]
            self.conductorLayers= DC_import['arr_conductorLayers'][0]
            self.substrateLayers= DC_import['arr_substrateLayers'][0]
            self.superstrateLayers= DC_import['arr_superstrateLayers'][0]

            noError = True
        except Exception as e:
             print(e)
             print("Error in design_config.py importing information from saved file")

        return noError


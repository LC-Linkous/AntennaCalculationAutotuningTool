##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/simulation_integrator/ANSYS/templateGen_Simulation.py'
#   Class for ANSYS HFSS simulation template generator.
#   Complements TG_ReportExport
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

from datetime import datetime
import re
import os.path

class SimulationTemplate:
    def __init__(self):
        self.templateTxt = []
        self.templateFile = ""
        self.reportTxt = [] #used for batch and tuning scripting without rerunning sim setup
        self.reportNames = []
        
        #file path for templates and reports
        self.templateBaseDir = os.path.join('src','simulation_integrator','ANSYS','code_templates')
        self.simulateBaseDir = os.path.join(self.templateBaseDir, 'simulation')
        self.reportTemplateDir = os.path.join(self.templateBaseDir,'report-templates')
        self.FFTemplateDir = os.path.join(self.reportTemplateDir, 'far-field')
        self.TSTemplateDir = os.path.join(self.reportTemplateDir, 'terminal-s')
        self.MSTemplateDir = os.path.join(self.reportTemplateDir, 'modal')
        self.ATTemplateDir = os.path.join(self.reportTemplateDir, 'antenna-parameter')

        #report name constants
        ## Antenna Parameter data
        self.NameAntennaParameterTable = "Antenna Params Table"
        ## Modal Solution Data
        self.NameMSRectangularPlot = "Modal S Parameter Rectangular Plot"
        self.NameMSRectangularStackedPlot = "Modal S Parameter Rectangular Stacked Plot"
        self.NameMSPolarPlot = "Modal S Parameter Polar Plot"
        self.NameMSDataTable = "Modal S Parameter Data Table"
        self.NameMSSmithChart = "Modal S Parameter Smith Chart"
        self.NameMS3DRectangularPlot = "Modal S Parameter 3D Rectangular"
        self.NameMS3DRectangularBarPlot = "Modal S Parameter 3D Rectangular Bar"
        self.NameMS3DPolarPlot = "Modal S Parameter 3D Polar Plot"
        self.NameMS3DSphericalPlot = "Modal S Parameter 3D Spherical Plot"
        self.NameMSRectangularContourPlot = "Modal S Parameter Rectangular Contour Plot"
        self.NameMSSmithContourPlot = "Modal S Parameter Smith Contour Plot"
        self.NameMSZRectangularPlot = "Modal Z Parameter Rectangular Plot"
        self.NameMSZRectangularStackedPlot = "Modal Z Parameter Rectangular Stacked Plot"
        self.NameMSZPolarPlot = "Modal Z Parameter Polar Plot"
        self.NameMSZDataTable = "Modal Z Parameter Data Table"
        self.NameMSZSmithChart = "Modal Z Parameter Smith Chart"
        self.NameMSZ3DRectangularPlot = "Modal Z Parameter 3D Rectangular"
        self.NameMSZ3DRectangularBarPlot = "Modal Z Parameter 3D Rectangular Bar"
        self.NameMSZ3DPolarPlot = "Modal Z Parameter 3D Polar Plot"
        self.NameMSZ3DSphericalPlot = "Modal Z Parameter 3D Spherical Plot"
        self.NameMSZRectangularContourPlot = "Modal Z Parameter Rectangular Contour Plot"
        self.NameMSZSmithContourPlot = "Modal Z Parameter Smith Contour Plot"
        ## Terminal Solution Data
        self.NameTSRectangularPlot = "Terminal S Parameter Rectangular Plot"
        self.NameTSRectangularStackedPlot = "Terminal S Parameter Rectangular Stacked Plot"
        self.NameTSPolarPlot = "Terminal S Parameter Polar Plot"
        self.NameTSDataTable = "Terminal S Parameter Data Table"
        self.NameTSSmithChart = "Terminal S Parameter Smith Chart"
        self.NameTS3DRectangularPlot = "Terminal S Parameter 3D Rectangular"
        self.NameTS3DRectangularBarPlot = "Terminal S Parameter 3D Rectangular Bar"
        self.NameTS3DPolarPlot = "Terminal S Parameter 3D Polar Plot"
        self.NameTS3DSphericalPlot = "Terminal S Parameter 3D Spherical Plot"
        self.NameTSRectangularContourPlot = "Terminal S Parameter Rectangular Contour Plot"
        self.NameTSSmithContourPlot = "Terminal S Parameter Smith Contour Plot"
        self.NameTSZRectangularPlot = "Terminal Z Parameter Rectangular Plot"
        self.NameTSZRectangularStackedPlot = "Terminal Z Parameter Rectangular Stacked Plot"
        self.NameTSZPolarPlot = "Terminal Z Parameter Polar Plot"
        self.NameTSZDataTable = "Terminal Z Parameter Data Table"
        self.NameTSZSmithChart = "Terminal Z Parameter Smith Chart"
        self.NameTSZ3DRectangularPlot = "Terminal Z Parameter 3D Rectangular"
        self.NameTSZ3DRectangularBarPlot = "Terminal Z Parameter 3D Rectangular Bar"
        self.NameTSZ3DPolarPlot = "Terminal Z Parameter 3D Polar Plot"
        self.NameTSZ3DSphericalPlot = "Terminal Z Parameter 3D Spherical Plot"
        self.NameTSZRectangularContourPlot = "Terminal Z Parameter Rectangular Contour Plot"
        self.NameTSZSmithContourPlot = "Terminal Z Parameter Smith Contour Plot"
        ## Far Field Data
        self.NameFFRectangularPlot = "Far Field Rectangular Plot"
        self.NameFFRectangularStackedPlot= "Far Field Rectangular Stacked Plot"
        self.NameFFRadiationPattern = "Far Field Radiation Pattern"
        self.NameFFDataTable = "Far Field Data Table"
        self.NameFF3DRectangularPlot = "Far Field 3D Rectangular Plot"
        self.NameFF3DRectangularBarPlot = "Far Field 3D Rectangular Bar Plot"
        self.NameFF3DPolarPlot = "Far Field 3D Polar Plot"
        self.NameFF3DSphericalPlot = "Far Field 3D Spherical Plot"
        self.NameFFRectangularContourPlot = "Far Field Rectangular Contour Plot"

    def getTemplateScript(self):
        return self.templateTxt
    
    def getReportOnlyScript(self):
        return self.reportTxt

    def setTemplateScript(self, t):
        self.templateTxt = t

    def clearTemplateScript(self):
        self.templateTxt = []
        self.reportTxt = []

    def clearReportNames(self):
        self.reportNames = []
    
    def getReportNames(self):
        return self.reportNames

    def addTemplateFromMemory(self, lst):
        for l in lst:
            self.templateTxt.append(l)

######################################################################
# single line 'template' calls
######################################################################
    def addSaveProject(self):
        tmpStr = "oProject.Save()\n"
        self.templateTxt.append(tmpStr)
    
    def deleteAndClearReports(self):
        # self.templateTxt.append("oDesign.DeleteFullVariation(\"All\", False)\n")
        self.templateTxt.append("oModule.DeleteAllReports()\n")
    
    def removeOldSimSetup(self):
        tmpStr = "oModule = oDesign.GetModule(\"RadField\")\n"+\
                "oModule.DeleteSetup([\"Infinite Sphere1\"])\n"+\
                "oModule = oDesign.GetModule(\"AnalysisSetup\")\n"+\
                "oModule.DeleteSetups([\"Setup1\"])\n"
        self.templateTxt.append(tmpStr)

    def analyzeAll(self):
        tmpStr = "oDesign.AnalyzeAll()\n"
        self.templateTxt.append(tmpStr)
        self.reportTxt.append(tmpStr)

    def reportSetup(self):
        tmpStr = "oModule = oDesign.GetModule(\"ReportSetup\")\n"
        self.templateTxt.append(tmpStr)
        self.reportTxt.append(tmpStr)

#######################################################################
# Project Setup
#######################################################################
    def addBaseSimTemplateSetup(self, f, useMult, minR, maxR, delta=0.02, numPass=6, numPts=401, units='Hz'):
        if useMult == True:
            self.addBaseMultiSimTemplateSetup(f, minR, maxR, delta, numPass, numPts, units)
        else: 
            self.addBaseSingleSimTemplateSetup(f, minR, maxR, delta, numPass, numPts, units)

    def addBaseSingleSimTemplateSetup(self, f, minR, maxR, delta, numPass, numPts, units):
                # src\simulation_integrator\ANSYS\code_templates\open-file\simulation\simulation-single-freq-base.txt
        filepath = os.path.join(self.simulateBaseDir, "simulation-single-freq-base.txt")
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to simulation-single-freq-base.txt template. check relative paths")
            print("attempted filepath: ", filepath)
            return       
        
        atnF = str(f) + " " + str(units)
        simDelta = str(delta)
        simMaxNumPass = str(numPass)
        simMinRange = str(minR) + " " + str(units) 
        simMaxRange = str(maxR) + " " + str(units) 
        simNumPoints = str(numPts)

        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                if re.search('INSERT_FREQUENCY', line):
                    li = atnF
                    line = re.sub('INSERT_FREQUENCY', li, line)
                elif re.search('INSERT_DELTA', line):
                    li = simDelta
                    line = re.sub('INSERT_DELTA', li, line)  
                elif re.search('INSERT_NUM_PASSES', line):
                    li =simMaxNumPass
                    line = re.sub('INSERT_NUM_PASSES', li, line)  
                elif re.search('INSERT_MIN_RANGE', line):
                    li =  simMinRange
                    line = re.sub('INSERT_MIN_RANGE', li, line)                                    
                elif re.search('INSERT_MAX_RANGE', line):
                    li =  simMaxRange
                    line = re.sub('INSERT_MAX_RANGE', li, line)  
                elif re.search('INSERT_NUM_POINTS', line):
                    li =  simNumPoints
                    line = re.sub('INSERT_NUM_POINTS', li, line)  
                self.templateTxt.append(line)
    
    def addBaseMultiSimTemplateSetup(self,f, minR, maxR, delta, numPass, numPts, units):
        #combine freqeuncy and delta values to get a 2D list
        paramList = self.combineFrequencyAndDelta(f, delta, units)

        #create inner template
        paramTemplate = self.updateMultiFrequencyTemplateWithList(paramList)

        #merge with base template
        #src\simulation_integrator\ANSYS\code_templates\simulation\simulation-multi-freq-base.txt
        filepath = os.path.join(self.templateBaseDir, 'simulation', 'simulation-multi-freq-base.txt')
        if os.path.isfile(filepath) == False:
            print("ERROR: templateGen_Simulation.py. path error to simulation-multi-freq-base.txt template. check relative paths")
            print("attempted filepath: ", filepath)   
            return

        simMaxNumPass = str(numPass)
        simMinRange = str(minR) + " " + str(units) 
        simMaxRange = str(maxR) + " " + str(units) 
        simNumPoints = str(numPts) 

        #read in the base format
        with open(filepath) as f:
            for line in f.readlines():
                if re.search('INSERT_FREQUENCY_CHANGES', line):
                    line = re.sub('INSERT_FREQUENCY_CHANGES', "", line)
                    for l in paramTemplate: #cant append whole array so loop
                        self.templateTxt.append(l)
                elif re.search('INSERT_NUM_PASSES', line):
                    li =simMaxNumPass
                    line = re.sub('INSERT_NUM_PASSES', li, line)  
                elif re.search('INSERT_MIN_RANGE', line):
                    li =  simMinRange
                    line = re.sub('INSERT_MIN_RANGE', li, line)                                    
                elif re.search('INSERT_MAX_RANGE', line):
                    li =  simMaxRange
                    line = re.sub('INSERT_MAX_RANGE', li, line)  
                elif re.search('INSERT_NUM_POINTS', line):
                    li =  simNumPoints
                    line = re.sub('INSERT_NUM_POINTS', li, line)  
                self.templateTxt.append(line)

       
    def combineFrequencyAndDelta(self, freq, delta, units):
        paramList = []
        freqList = freq.split(",")
        deltaList = delta.split(",")

        ctr = 0
        for f in freqList:
            f = f.strip() #remove extra whitespace
            f = f + " " + str(units)
            d = deltaList[ctr%len(deltaList)] #use mod to deal with mismatch
            d = d.strip()
            paramList.append([f, d])
            ctr = ctr+1
        return paramList


    def updateMultiFrequencyTemplateWithList(self, paramList):
        #takes in array of format [[freq, del],[freq, del],[freq, del]....]
        #src\simulation_integrator\ANSYS\code_templates\simulation\simulation-multi-end.txt
        #src\simulation_integrator\ANSYS\code_templates\simulation\simulation-multi-middle.txt 
        endFile = os.path.join(self.templateBaseDir, 'simulation', 'simulation-multi-end.txt')
        if os.path.isfile(endFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to simulation-multi-end.txt template. check relative paths")
            print("attempted filepath: ", endFile)
            return
        startFile = os.path.join(self.templateBaseDir, 'simulation', 'simulation-multi-middle.txt')
        if os.path.isfile(startFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to simulation-multi-middle.txt template. check relative paths")
            print("attempted filepath: ", startFile)
            return

        paramTemplate = []
        startTemplate = []
        endTemplate = []
        with open(startFile) as f:
            for line in f.readlines():
                startTemplate.append(line)

        with open(endFile) as f:
            for line in f.readlines():
                endTemplate.append(line)

        paramTemplate = []
        for pn in paramList:
            paramFreq = pn[0]
            paramDelta = pn[1]
            if pn is not paramList[-1]: #not last
                for line in startTemplate:
                    if re.search('INSERT_FREQUENCY', line):
                        line = re.sub('INSERT_FREQUENCY', paramFreq, line)
                    elif re.search('INSERT_DELTA', line):
                        line = re.sub('INSERT_DELTA', paramDelta, line)  
                    paramTemplate.append(line) 
            else:
                for line in endTemplate:
                    if re.search('INSERT_FREQUENCY', line):
                        line = re.sub('INSERT_FREQUENCY', paramFreq, line)
                    elif re.search('INSERT_DELTA', line):
                        line = re.sub('INSERT_DELTA', paramDelta, line)  
                    paramTemplate.append(line)  
        return paramTemplate


    def getReportDirectoryPath(self, rg, rt):
        #input: partial directory. reportGroup, reportType

        # path in program local test vs. folder as package
        noError = True
        relativePath = os.path.join("code_templates", "report-templates", str(rg), str(rt))
        fullPath = os.path.join(self.reportTemplateDir, str(rg), str(rt))
        if os.path.isdir(relativePath) == True:
            dirPath = relativePath
        elif os.path.isdir(fullPath):
            dirPath = fullPath
        else:
            print("ERROR: templateGen_Simulation.py. path error to report template. check relative paths")
            noError = False
        return dirPath, noError
    
    
    def createReport(self, templateDir, plotNameBase, paramTemplateArr, paramNames, fts, validFts, freq=str(0), units='Hz', zPlotNameBase="", dataTable=False, ModalSol=True):
       #datatables (data table and antenna param data table) have a different format
        if (dataTable == True) and (fts.isnull().all() == True):
            return #catch data table calls that slip through
        #default option only
        if (validFts == ["default"]):
            # template will not have option to modify components
            self.addReportToScript(templateDir, plotNameBase, paramTemplateArr, validFts, freq, units)
            return    
        # no components selected, use a default. df and array input options
        if (fts.isnull().all() == True) or (fts[0]=="default"):
            self.addReportToScript(templateDir, plotNameBase, paramTemplateArr, ["default"], freq, units)
            return
        elif (type(fts)==list) and (fts==["default"]):
            self.addReportToScript(templateDir, plotNameBase, paramTemplateArr, ["default"], freq, units)
            return            

        # component options selected
        sFts, zFts, gainFts, directivityFts, variableFts, antennaParamFts = self.checkValidReportConfig(fts, validFts, paramNames, ModalSol)
        if (len(sFts) > 0):
            self.addReportToScript(templateDir, plotNameBase, paramTemplateArr, sFts, freq, units)
        if (len(zFts) > 0):
            #z plot name is a hard coded version of the s plot name passed in 
            self.addReportToScript(templateDir, zPlotNameBase, paramTemplateArr, zFts, freq, units)
        if (len(gainFts) > 0):
            gPlotName = "Gain Plot " + plotNameBase
            self.addReportToScript(templateDir, gPlotName, paramTemplateArr, gainFts, freq, units)
        if (len(directivityFts) > 0):
            dPlotName = "Directivity Plot " + plotNameBase
            self.addReportToScript(templateDir, dPlotName, paramTemplateArr, directivityFts, freq, units)
        # if (len(dataTableFts) > 0):
        #     dtPlotName = plotNameBase #"data-table-" + plotNameBase
        #     self.addReportToScript(templateDir, dtPlotName, paramTemplateArr, dataTableFts, freq, units)
        if len(variableFts)>0:
            varPlotName = "Variable Table " + plotNameBase
            self.addReportToScript(templateDir, varPlotName, paramTemplateArr, variableFts, freq, units)
        if (len(antennaParamFts) > 0):
            self.addReportToScript(templateDir, plotNameBase, paramTemplateArr, antennaParamFts, freq, units)


    def addReportToScript(self, templateDir, plotNameBase, paramTemplateArr, fts, freq, units):    

        if (fts == ["default"]):
            # for when no output options are selected, but not a non-editable template
            reportTemplateFile = os.path.join(templateDir, 'default-report.txt')
        else:    
            reportTemplateFile = os.path.join(templateDir, 'report.txt')

        if os.path.isfile(reportTemplateFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to report template. check relative paths")
            print("attempted filepath: ", reportTemplateFile)
            return              

        multiFreq = False
        freq = freq.strip()#whitespace
        plotFreq = freq
        plotName = plotNameBase
        
        #check if multiFreq:
        freqSplit = freq.split(",")
        if len(freqSplit) > 1:
            #multi-freq, add other plot after this
            multiFreq = True
            plotFreq = str(freqSplit[0]) 
            plotName = str(plotNameBase) + "-" + str(plotFreq)
        
        with open(reportTemplateFile) as f:
            # go line by line and search for key words
            for line in f.readlines():
                if re.search('INSERT_FREQUENCY', line):
                    li = str(plotFreq) + " " + str(units)
                    line = re.sub('INSERT_FREQUENCY', li, line)
                elif re.search('INSERT_PARAMETER_BASE', line):
                    li = ""
                    for pn in paramTemplateArr:
                        li = li + str(pn)
                    line = li 
                elif re.search('INSERT_REPORT_NAME', line):
                    li = str(plotName)
                    line = re.sub('INSERT_REPORT_NAME', li, line)

                    if li not in self.reportNames: #for exporting by name later
                        self.reportNames.append(li)

                elif re.search("INSERT_COMPONENTS", line):
                    li = ""
                    for f in fts:
                        if f is not fts[-1]:
                            li = li + "\"" + str(f) + "\","
                        else:
                            li = li + "\"" + str(f) + "\""
                    line = re.sub('INSERT_COMPONENTS', li, line)                

                self.templateTxt.append(line)
                self.reportTxt.append(line) #duplicate for batch

        if multiFreq == True:
            self.addSecondaryReport(templateDir, plotNameBase, paramTemplateArr, fts, freqSplit[1:], units)

    def addSecondaryReport(self, templateDir, plotNameBase, paramTemplateArr, fts, freqList, units, componentParams):
        
        reportTemplateFile = os.path.join(templateDir, 'report.txt')

        if os.path.isfile(reportTemplateFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to report template. check relative paths")
            print("attempted filepath: ", reportTemplateFile)
            return              

        for freq in freqList:
            freq = freq.strip()#whitespace
            with open(reportTemplateFile) as f:
                # go line by line and search for key words
                for line in f.readlines():
                    if re.search('INSERT_FREQUENCY', line):
                        li = str(freq) + " " + str(units)
                        line = re.sub('INSERT_FREQUENCY', li, line)
                    elif re.search('INSERT_PARAMETER_BASE', line):
                        li = ""
                        for pn in paramTemplateArr:
                            li = li + str(pn)
                        line = li 
                    elif re.search('INSERT_REPORT_NAME', line):
                        li = str(plotNameBase) + "-" + str(freq)
                        line = re.sub('INSERT_REPORT_NAME', li, line)  
                        
                        if li not in self.reportNames:
                            self.reportNames.append(li)

                    elif re.search("INSERT_COMPONENTS", line):
                        li = ""
                        for f in fts:
                            if f is not fts[-1]:
                                li = li + "\"" + str(f) + "\","
                            else:
                                li = li + "\"" + str(f) + "\""
                        line = re.sub('INSERT_COMPONENTS', li, line)
                        
                    self.templateTxt.append(line)
                    self.reportTxt.append(line) #duplicate for batch


    def addTraceToExistingReport(self, templateDir, plotName, paramTemplateArr, freqList, units):
        
        templateTraceFile = os.path.join(templateDir, 'add-trace.txt')

        if os.path.isfile(templateTraceFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to report template. check relative paths")
            print("attempted filepath: ", templateTraceFile)
            return              

        for freq in freqList:
            with open(templateTraceFile) as f:
                # go line by line and search for key words
                for line in f.readlines():
                    if re.search('INSERT_FREQUENCY', line):
                        freq = freq.strip()#whitespace
                        li = str(freq) + " " + str(units)
                        line = re.sub('INSERT_FREQUENCY', li, line)
                    elif re.search('INSERT_PARAMETER_BASE', line):
                        li = ""
                        for pn in paramTemplateArr:
                            li = li + str(pn)
                        line = li 
                    elif re.search('INSERT_REPORT_NAME', line):
                        li = str(plotName)
                        line = re.sub('INSERT_REPORT_NAME', li, line)  
                        
                        if li not in self.reportNames:
                            self.reportNames.append(li)
                        
                    self.templateTxt.append(line)
                    self.reportTxt.append(line) #duplicate for batch


    def addOpenExistingProjectBase(self, filename):
        txt="import ScriptEnv \n" +\
            "ScriptEnv.Initialize(\"Ansoft.ElectronicsDesktop\")\n"+\
            "oDesktop.RestoreWindow()\n"+\
            "oDesktop.OpenProject(r" + repr(filename) + ")\n"+\
            "oProject = oDesktop.SetActiveProject(\"GeneratedHFSSProject\")\n"+\
            "oDesign = oProject.SetActiveDesign(\"HFSSDesign1\")\n"+\
            "oEditor = oDesign.SetActiveEditor(\"3D Modeler\")\n" 
        self.templateTxt.append(txt)

#######################################################################
# Antenna Parameter Report Options
#######################################################################
 
    def addAntennaParametersReportDataTable(self, paramTemplateArr, paramNames, fts, dataTable=True):
        filepath, noError = self.getReportDirectoryPath("antenna-parameter", "data-table")
        if noError == False: return
        plotname = self.NameAntennaParameterTable
        validFts = ["Peak Directivity (dB)", "Peak Gain (dB)","Radiation Efficiency","Total Efficiency",
                    "Radiated Power (dB)","Incident Power (dB)","Beam Area","Front To Back Ratio"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, dataTable=True)

#######################################################################
# Terminal Solution Data Report Options
#######################################################################

    def addTSRectangularPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s","Rectangular")
        if noError == False: return
        plotname = self.NameTSRectangularPlot
        zPlotNameBase = self.NameTSZRectangularPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTSRectangularStackedPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Rectangular-Stacked")
        if noError == False: return
        plotname = self.NameTSRectangularStackedPlot
        zPlotNameBase = self.NameTSZRectangularStackedPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTSPolarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Polar")
        if noError == False: return
        plotname = self.NameTSPolarPlot
        zPlotNameBase = self.NameTSZPolarPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTSDataTable(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Data-Table")
        if noError == False: return
        plotname = self.NameTSDataTable
        # zPlotNameBase NOT NEEDED
        validFts = ["default"] #uses default components
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts)

    def addTSSmithChart(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Smith-Chart")
        if noError == False: return
        plotname = self.NameTSSmithChart
        zPlotNameBase = self.NameTSZSmithChart
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTS3DRectangularPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "3D-Rectangular")
        if noError == False: return
        plotname = self.NameTS3DRectangularPlot
        zPlotNameBase = self.NameTSZ3DRectangularPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTS3DRectangularBarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "3D-Rectangular-Bar")
        if noError == False: return
        plotname = self.NameTS3DRectangularBarPlot
        zPlotNameBase = self.NameTSZ3DRectangularBarPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTS3DPolarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "3D-Polar")
        if noError == False: return
        plotname = self.NameTS3DPolarPlot
        zPlotNameBase = self.NameTSZ3DPolarPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTS3DSphericalPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "3D-Spherical")
        if noError == False: return
        plotname = self.NameTS3DSphericalPlot
        zPlotNameBase = self.NameTSZ3DSphericalPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTSRectangularContourPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Rectangular-Contour")
        if noError == False: return
        plotname = self.NameTSRectangularContourPlot
        zPlotNameBase = self.NameTSZRectangularContourPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addTSSmithContourPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("terminal-s", "Smith-Contour")
        if noError == False: return
        plotname = self.NameTSSmithContourPlot
        zPlotNameBase = self.NameTSZSmithContourPlot
        validFts = ["Terminal S (dB)", "Terminal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)


#######################################################################
# Modal Solution Data Report Options
#######################################################################

    def addMSRectangularPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal","Rectangular")
        if noError == False: return
        plotname = self.NameMSRectangularPlot
        zPlotNameBase = self.NameMSZRectangularPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMSRectangularStackedPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Rectangular-Stacked")
        if noError == False: return
        plotname = self.NameMSRectangularStackedPlot
        zPlotNameBase = self.NameMSZRectangularStackedPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMSPolarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Polar")
        if noError == False: return
        plotname = self.NameMSPolarPlot
        zPlotNameBase = self.NameMSZPolarPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMSDataTable(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Data-Table")
        if noError == False: return
        plotname = self.NameMSDataTable
        # zPlotNameBase not needed for default
        validFts = ["default"]  #uses the template default
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts)

    def addMSSmithChart(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Smith-Chart")
        if noError == False: return
        plotname = self.NameMSSmithChart
        zPlotNameBase = self.NameMSZSmithChart
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMS3DRectangularPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "3D-Rectangular")
        if noError == False: return
        plotname = self.NameMS3DRectangularPlot
        zPlotNameBase = self.NameMSZRectangularPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMS3DRectangularBarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "3D-Rectangular-Bar")
        if noError == False: return
        plotname = self.NameMS3DRectangularBarPlot
        zPlotNameBase = self.NameMSZ3DRectangularBarPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMS3DPolarPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "3D-Polar")
        if noError == False: return
        plotname = self.NameMS3DPolarPlot
        zPlotNameBase = self.NameMSZ3DPolarPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMS3DSphericalPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "3D-Spherical")
        if noError == False: return
        plotname = self.NameMS3DSphericalPlot
        zPlotNameBase = self.NameMSZ3DSphericalPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMSRectangularContourPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Rectangular-Contour")
        if noError == False: return
        plotname = self.NameMSRectangularContourPlot
        zPlotNameBase = self.NameMSZRectangularContourPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)

    def addMSSmithContourPlot(self, paramTemplateArr, paramNames, fts):
        filepath, noError = self.getReportDirectoryPath("modal", "Smith-Contour")
        if noError == False: return
        plotname = self.NameMSSmithContourPlot
        zPlotNameBase = self.NameMSZSmithContourPlot
        validFts = ["Modal S (dB)", "Modal Z (real, imaginary)"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, zPlotNameBase=zPlotNameBase)


#######################################################################
# Fields Solution Data Report Options
#######################################################################

    def addFRectangularPlot(self):
        pass

    def addFRectangularStackedPlot(self):
        pass

    def addFPolarPlot(self):
        pass

    def addFDataTable(self):
        pass

    def addF3DRectangularPlot(self):
        pass

    def addF3DRectangularBarPlot(self):
        pass

    def addFRectangularContourPlot(self):
        pass

#######################################################################
# Emission Test Data Report Options
#######################################################################

    def addETRectangularPlot(self):
        pass

    def addETRectangularStackedPlot(self):
        pass

    def addETDataTable(self):
        pass

#######################################################################
# Far Fields Data Report Options
#######################################################################

    def addFFRectangularPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "Rectangular")
        if noError == False: return
        plotname = self.NameFFRectangularPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFFRectangularStackedPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "Rectangular-Stacked")
        if noError == False: return
        plotname = self.NameFFRectangularStackedPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFFRadiationPattern(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "Radiation-Pattern")
        if noError == False: return
        plotname = self.NameFFRadiationPattern
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFFDataTable(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "Data-Table")
        if noError == False: return
        plotname = self.NameFFDataTable
        validFts = ["default"]  #uses default template
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFF3DRectangularPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "3D-Rectangular")
        if noError == False: return
        plotname = self.NameFF3DRectangularPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFF3DRectangularBarPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "3D-Rectangular-Bar")
        if noError == False: return
        plotname = self.NameFF3DRectangularBarPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFF3DPolarPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "3D-Polar")
        if noError == False: return
        plotname = self.NameFF3DPolarPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFF3DSphericalPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "3D-Spherical")
        if noError == False: return
        plotname = self.NameFF3DSphericalPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

    def addFFRectangularContourPlot(self, paramTemplateArr, paramNames, fts, f, unit="Hz"):
        filepath, noError = self.getReportDirectoryPath("far-field", "Rectangular-Contour")
        if noError == False: return
        plotname = self.NameFFRectangularContourPlot
        validFts = ["Gain Total", "Gain Phi", "Gain Theta", "Directivity Total", "Directivity Phi", "Directivity Theta"]
        self.createReport(filepath, plotname, paramTemplateArr, paramNames, fts, validFts, f)

#######################################################################
# Antenna Parameters Data Report Options
#######################################################################

    def addAPRectangularPlot(self):
        pass

    def addAPRectangularStackedPlot(self):
        pass

    def addAPDataTable(self):
        pass


#######################################################################
# Add Report Selection from User Input
#######################################################################

    def generateParameterBase(self, startFile, endFile, paramNames):
        if os.path.isfile(startFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to parameter base start template. check relative paths")
            print("attempted filepath: ", startFile)     
            return None
        if os.path.isfile(endFile) == False:
            print("ERROR: templateGen_Simulation.py. path error to parameter base end template. check relative paths")
            print("attempted filepath: ", endFile)     
            return None
        
        paramTemplate = []
        with open(startFile) as f:
            for line in f.readlines():
                startTemplate = line

        with open(endFile) as f:
            for line in f.readlines():
                endTemplate = line

        for pn in paramNames:
            if pn is not paramNames[-1]:
                li = re.sub("INSERT_PARAM_NAME", pn, startTemplate)
            else:
                li = re.sub("INSERT_PARAM_NAME", pn, endTemplate)
            paramTemplate.append(li + "\n")
        return paramTemplate

    def generateModalReportsFromList(self, lst, fts, paramNames):
        if len(lst) < 1:
            return
        #generate the param setup for the simulation report gen
        startFile = os.path.join(self.MSTemplateDir, "parameter-base_start.txt")
        endFile = os.path.join(self.MSTemplateDir, "parameter-base_end.txt")
        paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)
        
        for l in lst:
            if l=="Rectangular Plot":
                self.addMSRectangularPlot(paramTemplateArr, paramNames, fts)
            elif l=="Rectangular Stacked Plot":
                self.addMSRectangularStackedPlot(paramTemplateArr, paramNames, fts)
            elif l=="Polar Plot":
                self.addMSPolarPlot(paramTemplateArr, paramNames, fts)
            elif l=="Data Table (default)":
                self.addMSDataTable(paramTemplateArr, paramNames, fts)
            elif l=="Smith Chart":
                self.addMSSmithChart(paramTemplateArr, paramNames, fts)
            elif l=="3D Rectangular Plot":
                self.addMS3DRectangularPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Rectangular Bar Plot":
                self.addMS3DRectangularBarPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Polar Plot":
                self.addMS3DPolarPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Spherical Plot":
                self.addMS3DSphericalPlot(paramTemplateArr, paramNames, fts)
            elif l=="Rectangular Contour Plot":
                self.addMSRectangularContourPlot(paramTemplateArr, paramNames, fts)
            elif l=="Smith Contour Plot":
                self.addMSSmithContourPlot(paramTemplateArr, paramNames, fts)
            else:
                pass
                # print("ERROR: Modal Report Data graph type not recognized")
                # print(str(l))
                

    def generateTerminalReportsFromList(self, lst, fts, paramNames):
        if len(lst) < 1:
            return
        #generate the param setup for the simulation report gen
        startFile = os.path.join(self.TSTemplateDir, "parameter-base_start.txt")
        endFile = os.path.join(self.TSTemplateDir, "parameter-base_end.txt")
        paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)

        for l in lst:
            if l=="Rectangular Plot":
                self.addTSRectangularPlot(paramTemplateArr, paramNames, fts)
            elif l=="Rectangular Stacked Plot":
                self.addTSRectangularStackedPlot(paramTemplateArr, paramNames, fts)
            elif l=="Polar Plot":
                self.addTSPolarPlot(paramTemplateArr, paramNames, fts)
            elif l=="Data Table (default)":
                self.addTSDataTable(paramTemplateArr, paramNames, fts)
            elif l=="Smith Chart":
                self.addTSSmithChart(paramTemplateArr, paramNames, fts)
            elif l=="3D Rectangular Plot":
                self.addTS3DRectangularPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Rectangular Bar Plot":
                self.addTS3DRectangularBarPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Polar Plot":
                self.addTS3DPolarPlot(paramTemplateArr, paramNames, fts)
            elif l=="3D Spherical Plot":
                self.addTS3DSphericalPlot(paramTemplateArr, paramNames, fts)
            elif l=="Rectangular Contour Plot":
                self.addTSRectangularContourPlot(paramTemplateArr, paramNames, fts)
            elif l=="Smith Contour Plot":
                self.addTSSmithContourPlot(paramTemplateArr, paramNames, fts)
            else:
                pass
                # print("ERROR: Terminal Report Data graph type not recognized")
                # print(str(l))
                

    def generateFarFieldReportsFromList(self, lst, fts, paramNames, f, unit='Hz'):
        if len(lst) < 1:
            return
        #generate the param setup for the simulation report gen
        startFile = os.path.join(self.FFTemplateDir, "parameter-base_start.txt")
        endFile = os.path.join(self.FFTemplateDir, "parameter-base_end.txt")
        paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)

        for l in lst:
            if l=="Rectangular Plot":
                self.addFFRectangularPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="Rectangular Stacked Plot":
                self.addFFRectangularStackedPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="Radiation Pattern":
                self.addFFRadiationPattern(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="Data Table (default)":
                self.addFFDataTable(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="3D Rectangular Plot":
                self.addFF3DRectangularPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="3D Rectangular Bar Plot":
                self.addFF3DRectangularBarPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="3D Polar Plot":
                self.addFF3DPolarPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="3D Spherical Plot":
                self.addFF3DSphericalPlot(paramTemplateArr, paramNames, fts, f, unit)
            elif l=="Rectangular Contour Plot":
                self.addFFRectangularContourPlot(paramTemplateArr, paramNames, fts, f, unit)
            else:
                pass
                # print("ERROR: Terminal Report Data graph type not recognized")
                # print(str(l))

    def generateDataTableReportsFromList(self, modalFts, terminalFts, farfieldFts, paramNames, f, unit='Hz'):
        #generates just the tables from the custom configs

        if (modalFts.isnull().all() == True) and (terminalFts.isnull().all() == True) and (farfieldFts.isnull().all() == True): #nothing in any of the fts dfs
            return

        # validFts are the most common valid features for a report. 
        MSTSValidFts = ["Variables", 
                      "S Parameters (dB)", 
                      "Z Parameters (real, imaginary)"]
        ffValidFts = ["Controllable Parameters", 
                    "Gain Total", "Gain Phi", "Gain Theta",
                     "Directivity Total", "Directivity Phi", "Directivity Theta"]

        if len(modalFts) > 0:
            #generate the param setup for the simulation report gen
            startFile = os.path.join(self.MSTemplateDir, "parameter-base_start.txt")
            endFile = os.path.join(self.MSTemplateDir, "parameter-base_end.txt")
            paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)
            filepath, noError = self.getReportDirectoryPath("modal", "Data-Table")
            if noError == True:
                plotname = self.NameMSDataTable
                zPlotNameBase = self.NameMSZDataTable
                validFts = MSTSValidFts
                self.createReport(filepath, plotname, paramTemplateArr, paramNames, modalFts, validFts, zPlotNameBase=zPlotNameBase, dataTable=True, ModalSol=True)

        if len(terminalFts) > 0:
            #generate the param setup for the simulation report gen
            startFile = os.path.join(self.TSTemplateDir, "parameter-base_start.txt")
            endFile = os.path.join(self.TSTemplateDir, "parameter-base_end.txt")
            paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)
            filepath, noError = self.getReportDirectoryPath("terminal-s", "Data-Table")
            if noError == True: 
                plotname = self.NameTSDataTable
                zPlotNameBase = self.NameTSZDataTable
                validFts = MSTSValidFts
                self.createReport(filepath, plotname, paramTemplateArr, paramNames, terminalFts, validFts, zPlotNameBase=zPlotNameBase, dataTable=True, ModalSol=False)
        
        if len(farfieldFts) > 0:
            #generate the param setup for the simulation report gen
            startFile = os.path.join(self.FFTemplateDir, "parameter-base_start.txt")
            endFile = os.path.join(self.FFTemplateDir, "parameter-base_end.txt")
            paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)
            filepath, noError = self.getReportDirectoryPath("far-field", "Data-Table")
            if noError == True:
                plotname = self.NameFFDataTable
                zPlotNameBase = self.NameFFDataTable
                validFts = ffValidFts
                self.createReport(filepath, plotname, paramTemplateArr, paramNames, farfieldFts, validFts, f, zPlotNameBase=zPlotNameBase, dataTable=True)

    def generateAntennaParameterTableReportsFromList(self, antennaParamTableFts, paramNames):
        if len(antennaParamTableFts) < 1:
            return
        if (antennaParamTableFts.isnull().all() == True): #nothing in the fts dfs
            return

        startFile = os.path.join(self.ATTemplateDir, "parameter-base_start.txt")
        endFile = os.path.join(self.ATTemplateDir, "parameter-base_end.txt")
        paramTemplateArr = self.generateParameterBase(startFile, endFile, paramNames)
        self.addAntennaParametersReportDataTable(paramTemplateArr, paramNames, antennaParamTableFts, dataTable=True)


    def getDefaultOptimizerReports(self):
        modalLst = ["Rectangular Plot"]
        modalFtsLst = ["default"]
        terminalLst = [] #terminal currently not used for default. TODO: add toggle
        terminalFtsLst = ["default"]
        farfieldLst = [] #"3D Polar Plot"
        farfieldFtsLst=["default"]
        dataTableLst = []
        antennaParamFts = ["default"] 
        return modalLst,modalFtsLst, terminalLst, terminalFtsLst, \
                farfieldLst, farfieldFtsLst, dataTableLst, antennaParamFts


#######################################################################
# valid report configuration checks
#######################################################################

    def checkValidReportConfig(self, fts, vfts, paramNames, ModalSol=True):
        # valid features has already been filtered for 'default' 
        #fts: features selected for report
        #vfts: valid features for the report (hard coded)

        validInputFeatures=[] # filter input
        sComponentFts = [] # returned S param
        zComponentFts = [] # returned Z param
        gainComponentFts = [] # returned Gain
        directivityComponentFts = [] # returned directivity
        antennaParamComponentFts = []
        variableFts = [] #variable lists for datatable


        # sanitize inputs (error catch for new additions)
        for f in fts:
            if f in vfts:
                validInputFeatures.append(f)
        # NOTE:
        # the terminal combinations have NOT been tested for the Z components

        for vinfts in validInputFeatures:
            # S param components
            if vinfts == "Modal S (dB)":
                val = "dB(S(1,1))"
                sComponentFts.append(val)
            elif vinfts == "Terminal S (dB)":
                val = "dB(St(port_T1,port_T1))"
                sComponentFts.append(val)

            # Z param components
            elif vinfts == "Modal Z (real, imaginary)":
                val = "mag(Z(1,1))"
                zComponentFts.append(val)
                val = "im(Z(1,1))"
                zComponentFts.append(val)
            elif vinfts == "Terminal Z (real, imaginary)":
                val = "mag(Zt(port_T1,port_T1))"
                zComponentFts.append(val)
                val = "im(Zt(port_T1,port_T1))"
                zComponentFts.append(val)

            # gain components
            elif vinfts == "Gain Total":
                val = "dB(GainTotal)"
                gainComponentFts.append(val)
            elif vinfts == "Gain Phi":
                val = "dB(GainPhi)"
                gainComponentFts.append(val)
            elif vinfts == "Gain Theta":
                val = "dB(GainTheta)"
                gainComponentFts.append(val)
            
            # directivity components
            elif vinfts == "Directivity Total":
                val = "dB(DirTotal)"
                directivityComponentFts.append(val)
            elif vinfts == "Directivity Phi":
                val = "dB(DirPhi)"
                directivityComponentFts.append(val)
            elif vinfts == "Directivity Theta":
                val = "dB(DirTheta)"
                directivityComponentFts.append(val)

            # data table components
            # loop through paramNames and add to lists
            # other vals added above (S Parameters (dB), and Z Parameters ( real, imaginary) for modal and terminal)
            elif vinfts == "Variables": #modal and terminal
                val = "Freq"
                variableFts.append(val)
                for pn in paramNames:
                    variableFts.append(pn)  
            elif vinfts == "S Parameters (dB)":
                if ModalSol == True:
                    val = "dB(S(1,1))"
                    sComponentFts.append(val)
                else:
                    val = "dB(St(port_T1,port_T1))"
                    sComponentFts.append(val)
            elif vinfts == "Z Parameters (real, imaginary)":
                if ModalSol == True:
                    val = "mag(Z(1,1))"
                    zComponentFts.append(val)
                    val = "im(Z(1,1))"
                    zComponentFts.append(val)
                else:
                    val = "mag(Zt(port_T1,port_T1))"
                    zComponentFts.append(val)
                    val = "im(Zt(port_T1,port_T1))"
                    zComponentFts.append(val)
 
            elif vinfts == "Controllable Parameters": #far field 
                val = "Freq"
                variableFts.append(val)
                val = "Phase"
                variableFts.append(val)
                for pn in paramNames:
                    variableFts.append(pn) 


            # antenna param data table
            elif vinfts == "Peak Directivity (dB)":
                val = "dB(PeakDirectivity)"
                antennaParamComponentFts.append(val)
            elif vinfts == "Peak Gain (dB)":
                val = "dB(PeakGain)"
                antennaParamComponentFts.append(val)
            elif vinfts == "Radiation Efficiency":
                val = "RadiationEfficiency"
                antennaParamComponentFts.append(val)
            elif vinfts == "Total Efficiency":
                val = "TotalEfficiency"
                antennaParamComponentFts.append(val)
            elif vinfts == "Radiated Power (dB)":
                val = "dB(RadiatedPower)"
                antennaParamComponentFts.append(val)
            elif vinfts == "Incident Power (dB)":
                val = "dB(IncidentPower)"
                antennaParamComponentFts.append(val)
            elif vinfts == "Beam Area":
                val = "BeamArea"
                antennaParamComponentFts.append(val)
            elif vinfts == "Front To Back Ratio":
                val = "FrontToBackRatio"
                antennaParamComponentFts.append(val)

        return sComponentFts, zComponentFts, gainComponentFts, directivityComponentFts, variableFts, antennaParamComponentFts
    
    #sFts, zFts, gainFts, directivityFts, variableFts, antennaParamFts

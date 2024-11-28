##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'simulation_integrator/COMSOL/templateGen_Simulation.py'
#   Class for COMSOL simulation template generator.
#
#   NOTE: Redoing with the updated ANSYS template to bring everything up to date
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

from datetime import datetime
import os.path


import project.config.antennaCAT_config as c

class SimulationTemplate:
    def __init__(self, projName, projDir):
        self.templateTxt = []
        self.templateFile = ""
        self.projectName = projName        
        self.projectPath = projDir + "/" + self.projectName
        #report directory
        self.reportDir = projDir + "/reports"
        # data directory (for CSV)
        self.dataDir = projDir + "/data"
        #file path for templates and reports
        self.reportTemplateDir = "./src/simulation_integrator/COMSOL/code_templates/report-templates/"

        #report name constants
        ## Antenna Parameter data
        self.NameAntennaParameterTable = "Antenna Params Table"
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

    def setProjectPath(self, p):
        self.projectPath = p
        print(self.projectPath)
    
    def getProjectPath(self):
        return self.projectPath

    def setProjectDir(self, d):
        self.projectDir = d
        self.projectPath = str(self.projectDir) + "/" + str(self.projectName)
    
    def setProjectName(self, n):
        self.projectName = n
        self.projectPath = str(self.projectDir) + "/" + str(self.projectName)

    def loadTemplate(self):
        pass

    def getTemplateScript(self):
        return self.templateTxt

    def addCommentsToTop(self, c=None):
        now = datetime.now()
        tmpStr = "TODO"
        self.templateTxt.append(tmpStr)

    def deleteParticleGroup(self):
        #make more general based on naming conventions
        tmpStr = "TODO"
        self.templateTxt.append(tmpStr)

#######################################################################
# Project Setup
#######################################################################
    def addBaseSimTemplateSetup(self, f,minR, maxR, delta=0.02, numPass=6, numPts=401):
        # projName = self.projectPath + self.projectName
        projPath = "\"" + self.projectPath + "\""
        atnF = "\"" + str(f) + "\""
        simDelta = str(delta)
        simMaxNumPass = str(numPass)
        simMinRange = "\"" + str(minR) + " Hz\""  #always defaults to Hz (i.e 2.4e9 Hz)
        simMaxRange = "\"" + str(maxR) + " Hz\""  #always defaults to Hz (i.e 2.4e9 Hz)
        simNumPoints = str(numPts)

        filepath = self.getSimFilePath("simulation-base.txt")
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    if l == "INSERT_FREQUENCY,":
                        l = atnF + ","
                    elif l == "INSERT_DELTA,":
                        l = simDelta+ ","
                    elif l == "INSERT_NUM_PASSES,":
                        l = simMaxNumPass+ ","
                    elif l == "INSERT_MIN_RANGE,":
                        l = simMinRange+ ","
                    elif l == "INSERT_MAX_RANGE,":
                        l = simMaxRange + ","
                    elif l == "INSERT_NUM_POINTS,":
                        l = simNumPoints+ ","
                    elif str(l) == "TODO":
                        pass
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)

    def addOpenFileTemplate(self):
        #         self.projectName = projName
        # self.projectPath = projDir + "/" + self.projectName
        # projName = self.projectPath + self.projectName
        projPath = "\"" + self.projectPath + "\""

        filepath = self.getSimFilePath("open-file-base.txt")
        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    if str(l) == "TODO":
                        pass
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)

    def addTemplateFromMemory(self, lst):
        for l in lst:
            self.templateTxt.append(l)

    def addSaveProject(self):
        tmpStr = "TODO\n"
        self.templateTxt.append(tmpStr)

    def removeOldSimSetup(self):
        tmpStr = "TODO"
        self.templateTxt.append(tmpStr)

    def getSimFilePath(self, f):
        # path in program local test vs. folder as package
        if os.path.isfile("code_templates/" + str(f)) == True:
            filepath = "code_templates/"+ str(f)
        elif os.path.isfile( "./src/simulation_integrator/COMSOL/code_templates/"+ str(f)):
            filepath = "./src/simulation_integrator/COMSOL/code_templates/"+ str(f)
        else:
            print("ERROR: templateGen_Simulation.py. path error to template. check relative paths")

        return filepath

    def getReportFilePath(self, f):
        # path in program local test vs. folder as package
        if os.path.isfile("code_templates/report-templates/" + str(f)) == True:
            filepath = "code_templates/report-templates/" + str(f)
        elif os.path.isfile(self.reportTemplateDir + str(f)):
            filepath = self.reportTemplateDir + str(f)
        else:
            print("ERROR: templateGen_Simulation.py. path error to report template. check relative paths")
        return filepath

    def addReportToTemplate(self, filepath, filename, plotname, f=0):
        filename = "\"" + str(filename) + "\""  #the template name
        plotname= "\"" + str(plotname) + "\""
        freq = "\"" + str(f) + "\""

        with open(filepath) as f:
            # go line by line and search for key words
            for line in f.readlines():
                tmpArr = ""
                for l in (line.split()):  # remove newline at end, split individual words
                    #print(l)
                    if l == "[INSERT_FREQUENCY],":
                        l = "[" + freq + "],"
                    elif l == "INSERT_SAVE_PATH,":
                        l =  filename + ", "
                    elif l == "INSERT_SAVE_PATH)":
                        l = filename + ")"
                    elif l=="oModule.CreateReport(INSERT_REPORT_NAME,":
                        l = "oModule.CreateReport(" + plotname + ","
                    tmpArr = tmpArr + l + " "
                tmpArr = tmpArr + "\n"
                self.templateTxt.append(tmpArr)

    def addExportReportToTemplate(self, filename, plotname):
        #Function used to replace template to reduce number of files with single line commands
        INSERT_REPORT_NAME = "\"" + plotname +"\""
        INSERT_SAVE_PATH = "\"" + str(filename) + "\""
        txt = "TODO\n"
        self.templateTxt.append(txt)

    def addOpenExistingProjectBase(self, filename):
        PROJECT_NAME = "\"" + filename + "\""
        txt="TODO" 
        self.templateTxt.append(txt)
#######################################################################
# Add code to delete and clear reports 
#######################################################################

    def deleteAndClearReports(self):
        self.templateTxt.append("TODO")
        self.templateTxt.append("\n")
        self.templateTxt.append("TODO")
        self.templateTxt.append("\n")

#######################################################################
# Antenna Parameter Report Options
#######################################################################
 
    def addAntennaParametersReportTable(self, name="Antenna-Parameters-Table.csv"):
        filepath = self.getReportFilePath("report_Antenna-Parameters-Table.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameAntennaParameterTable
        self.addReportToTemplate(filepath, filename, plotname)

    def exportAntennaParametersReportTable(self, name="Antenna-Parameters-Table.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameAntennaParameterTable
        self.addExportReportToTemplate(filename, plotname)


#######################################################################
# Terminal Solution Data Report Options
#######################################################################

    def addTSRectangularPlot(self, name="Terminal_S-Parameter_Rectangular-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-Rectangular.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSRectangularStackedPlot(self, name="Terminal_S-Parameter_Rectangular-Stacked-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-Rectangular-Stacked.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularStackedPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSPolarPlot(self, name="Terminal_S-Parameter_Polar-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-Polar.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSPolarPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSDataTable(self, name="Terminal_S-Parameter_Data-Table.csv"):
        filepath = self.getReportFilePath("report_TS-Data-Table.txt")
        filename = self.dataDir + "\\"  + str(name)
        plotname = self.NameTSDataTable
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSSmithChart(self, name="Terminal_S-Parameter_Smith-Chart.csv"):
        filepath = self.getReportFilePath("report_TS-Smith-Chart.txt")
        filename = self.dataDir + "\\"  + str(name)
        plotname = self.NameTSSmithChart
        self.addReportToTemplate(filepath, filename, plotname)

    def addTS3DRectangularPlot(self, name="Terminal_S-Parameter_3D-Rectangular-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-3D-Rectangular.txt")
        filename = self.dataDir + "\\"  + str(name)
        plotname = self.NameTS3DRectangularPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTS3DRectangularBarPlot(self, name="Terminal_S-Parameter_3D-Rectangular-Bar-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-3D-Rectangular-Bar.txt")
        filename = self.dataDir + "\\"  + str(name)
        plotname = self.NameTS3DRectangularBarPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTS3DPolarPlot(self, name="Terminal_S-Parameter_3D-Polar-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-3D-Polar.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DPolarPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTS3DSphericalPlot(self, name="Terminal_S-Parameter_3D-Spherical-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-3D-Spherical.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DSphericalPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSRectangularContourPlot(self, name="Terminal_S-Parameter_Rectangular-Contour-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-Rectangular-Contour.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularContourPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def addTSSmithContourPlot(self, name="Terminal_S-Parameter_Smith-Contour-Plot.csv"):
        filepath = self.getReportFilePath("report_TS-Smith-Contour.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSSmithContourPlot
        self.addReportToTemplate(filepath, filename, plotname)

    def exportTSRectangularPlot(self, name="Terminal_S-Parameter_Rectangular-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSRectangularStackedPlot(self, name="Terminal_S-Parameter_Rectangular-Stacked-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularStackedPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSPolarPlot(self, name="Terminal_S-Parameter_Polar-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSDataTable(self, name="Terminal_S-Parameter_Data-Table.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSDataTable
        self.addExportReportToTemplate(filename, plotname)

    def exportTSSmithChart(self, name="Terminal_S-Parameter_Smith-Chart.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSSmithChart
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DRectangularPlot(self, name="Terminal_S-Parameter_3D-Rectangular-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DRectangularBarPlot(self, name="Terminal_S-Parameter_3D-Rectangular-Bar-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DRectangularBarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DPolarPlot(self, name="Terminal_S-Parameter_3D-Polar-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DSphericalPlot(self, name="Terminal_S-Parameter_3D-Spherical-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTS3DSphericalPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSRectangularContourPlot(self, name="Terminal_S-Parameter_Rectangular-Contour-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSRectangularContourPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSSmithContourPlot(self, name="Terminal_S-Parameter_Smith-Contour-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameTSSmithContourPlot
        self.addExportReportToTemplate(filename, plotname)

#######################################################################
# Modal Solution Data Report Options
#######################################################################

    def addMSRectangularPlot(self):
        pass

    def addMSRectangularStackedPlot(self):
        pass

    def addMSPolarPlot(self):
        pass

    def addMSDataTable(self):
        pass

    def addMSSmithChart(self):
        pass

    def addMS3DRectangularPlot(self):
        pass

    def addMS3DRectangularBarPlot(self):
        pass

    def addMS3DPolarPlot(self):
        pass

    def addMS3DSphericalPlot(self):
        pass

    def addMSRectangularContourPlot(self):
        pass

    def addMSSmithContourPlot(self):
        pass

    def exportMSRectangularPlot(self):
        pass

    def exportMSRectangularStackedPlot(self):
        pass

    def exportMSPolarPlot(self):
        pass

    def exportMSDataTable(self):
        pass

    def exportMSSmithChart(self):
        pass

    def exportMS3DRectangularPlot(self):
        pass

    def exportMS3DRectangularBarPlot(self):
        pass

    def exportMS3DPolarPlot(self):
        pass

    def exportMS3DSphericalPlot(self):
        pass

    def exportMSRectangularContourPlot(self):
        pass

    def exportMSSmithContourPlot(self):
        pass

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

    def exportFRectangularPlot(self):
        pass

    def exportFRectangularStackedPlot(self):
        pass

    def exportFPolarPlot(self):
        pass

    def exportFDataTable(self):
        pass

    def exportF3DRectangularPlot(self):
        pass

    def exportF3DRectangularBarPlot(self):
        pass

    def exportFRectangularContourPlot(self):
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

    def exportETRectangularPlot(self):
        pass

    def exportETRectangularStackedPlot(self):
        pass

    def exportETDataTable(self):
        pass

#######################################################################
# Far Fields Data Report Options
#######################################################################

    def addFFRectangularPlot(self, f, name="Far-Field_Rectangular-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-Rectangular.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFFRectangularStackedPlot(self, f, name="Far-Field_Rectangular-Stacked-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-Rectangular-Stacked.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularStackedPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFFRadiationPattern(self, f, name="Far-Field_3D-Rectangular-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-Radiation-Pattern.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRadiationPattern
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFFDataTable(self, f, name="Far-Field_Data-Table.csv"):
        filepath = self.getReportFilePath("report_FF-Data-Table.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFDataTable
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFF3DRectangularPlot(self, f, name="Far-Field_3D-Rectangular-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-3D-Rectangular.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DRectangularPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFF3DRectangularBarPlot(self, f, name="Far-Field_3D-Rectangular-Bar-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-3D-Rectangular-Bar.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DRectangularBarPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFF3DPolarPlot(self, f, name="Far-Field_3D-Polar-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-3D-Polar.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DPolarPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFF3DSphericalPlot(self, f, name="Far-Field_3D-Spherical-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-3D-Spherical.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DSphericalPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def addFFRectangularContourPlot(self, f, name="Far-Field_Rectangular-Contour-Plot.csv"):
        filepath = self.getReportFilePath("report_FF-Rectangular-Contour.txt")
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularContourPlot
        self.addReportToTemplate(filepath, filename, plotname, f)

    def exportFFRectangularPlot(self, name="Far-Field_Rectangular-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRectangularStackedPlot(self, name="Far-Field_Rectangular-Stacked-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularStackedPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRadiationPattern(self, name="Far-Field_3D-Rectangular-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRadiationPattern
        self.addExportReportToTemplate(filename, plotname)

    def exportFFDataTable(self, name="Far-Field_Data-Table.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFDataTable
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DRectangularPlot(self, name="Far-Field_3D-Rectangular-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DRectangularBarPlot(self, name="Far-Field_3D-Rectangular-Bar-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DRectangularBarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DPolarPlot(self, name="Far-Field_3D-Polar-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DSphericalPlot(self, name="Far-Field_3D-Spherical-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFF3DSphericalPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRectangularContourPlot(self, name="Far-Field_Rectangular-Contour-Plot.csv"):
        filename = self.dataDir + "\\" + str(name)
        plotname = self.NameFFRectangularContourPlot
        self.addExportReportToTemplate(filename, plotname)

#######################################################################
# Antenna Parameters Data Report Options
#######################################################################

    def addAPRectangularPlot(self):
        pass

    def addAPRectangularStackedPlot(self):
        pass

    def addAPDataTable(self):
        pass

    def exportAPRectangularPlot(self):
        pass

    def exportAPRectangularStackedPlot(self):
        pass

    def exportAPDataTable(self):
        pass

#######################################################################
# Add Report Selection from User Input
#######################################################################

    def generateTerminalReportsFromList(self, lst):
        for l in lst:
            if l=="Rectangular Plot":
                self.addTSRectangularPlot()
            elif l=="Rectangular Stacked Plot":
                self.addTSRectangularStackedPlot()
            elif l=="Polar Plot":
                self.addTSPolarPlot()
            elif l=="Data Table":
                self.addTSDataTable()
            elif l=="Smith Chart":
                self.addTSSmithChart()
            elif l=="3D Rectangular Plot":
                self.addTS3DRectangularPlot()
            elif l=="3D Rectangular Bar Plot":
                self.addTS3DRectangularBarPlot()
            elif l=="3D Polar Plot":
                self.addTS3DPolarPlot()
            elif l=="3D Spherical Plot":
                self.addTS3DSphericalPlot()
            elif l=="Rectangular Contour Plot":
                self.addTSRectangularContourPlot()
            elif l=="Smith Contour Plot":
                self.addTSSmithContourPlot()
            else:
                print("ERROR: Terminal Report Data graph type not recognized")

    def generateFarFieldReportsFromList(self, lst, f):
        for l in lst:
            if l=="Rectangular Plot":
                self.addFFRectangularPlot(f)
            elif l=="Rectangular Stacked Plot":
                self.addFFRectangularStackedPlot(f)
            elif l=="Radiation Pattern":
                self.addFFRadiationPattern(f)
            elif l=="Data Table":
                self.addFFDataTable(f)
            elif l=="3D Rectangular Plot":
                self.addFF3DRectangularPlot(f)
            elif l=="3D Rectangular Bar Plot":
                self.addFF3DRectangularBarPlot(f)
            elif l=="3D Polar Plot":
                self.addFF3DPolarPlot(f)
            elif l=="3D Spherical Plot":
                self.addFF3DSphericalPlot(f)
            elif l=="Rectangular Contour Plot":
                self.addFFRectangularContourPlot(f)
            else:
                print("ERROR: Terminal Report Data graph type not recognized")

#######################################################################
# Add code to export reports to file from user input
#######################################################################

    def exportTerminalReportData(self, lst):
        for l in lst:
            if l=="Rectangular Plot":
                self.exportTSRectangularPlot()
            elif l=="Rectangular Stacked Plot":
                self.exportTSRectangularStackedPlot()
            elif l=="Polar Plot":
                self.exportTSPolarPlot()
            elif l=="Data Table":
                self.exportTSDataTable()
            elif l=="Smith Chart":
                self.exportTSSmithChart()
            elif l=="3D Rectangular Plot":
                self.exportTS3DRectangularPlot()
            elif l=="3D Rectangular Bar Plot":
                self.exportTS3DRectangularBarPlot()
            elif l=="3D Polar Plot":
                self.exportTS3DPolarPlot()
            elif l=="3D Spherical Plot":
                self.exportTS3DSphericalPlot()
            elif l=="Rectangular Contour Plot":
                self.exportTSRectangularContourPlot()
            elif l=="Smith Contour Plot":
                self.exportTSSmithContourPlot()
            else:
                print("ERROR: Terminal Report Data graph type not recognized")

    def exportFarFieldReportData(self, lst):
        for l in lst:
            if l=="Rectangular Plot":
                self.exportFFRectangularPlot()
            elif l=="Rectangular Stacked Plot":
                self.exportFFRectangularStackedPlot()
            elif l=="Radiation Pattern":
                self.exportFFRadiationPattern()
            elif l=="Data Table":
                self.exportFFDataTable()
            elif l=="3D Rectangular Plot":
                self.exportFF3DRectangularPlot()
            elif l=="3D Rectangular Bar Plot":
                self.exportFF3DRectangularBarPlot()
            elif l=="3D Polar Plot":
                self.exportFF3DPolarPlot()
            elif l=="3D Spherical Plot":
                self.exportFF3DSphericalPlot()
            elif l=="Rectangular Contour Plot":
                self.exportFFRectangularContourPlot()
            else:
                print("ERROR: Far Field Report Data graph type not recognized")

if __name__ == "__main__":
    # import sys
    # sys.path.insert(0, './src')
    #base template changed so this can no longer be run in HFSS alone.
    #however, it can be exported for visual inspection
    ST = SimulationTemplate()
    ST.addCommentsToTop("test generation")
    print(ST.getProjectPath())
    f = "2.4GHz"
    #if opening existing project, use lines until 'AddBaseSimTemplateSetup". otherwise comment out
    ST.addOpenExistingProjectBase(filename="C:/Users/LCLin/Desktop//GeneratedHFSSProject.aedt")

    ST.addBaseSimTemplateSetup(f=f,minR="2.0GHz", maxR="6GHz")
    ST.addTSRectangularPlot()
    ST.addTSRectangularStackedPlot()
    ST.addTSPolarPlot()
    ST.addTSDataTable()
    ST.addTSSmithChart()
    ST.addTS3DRectangularPlot()
    ST.addTS3DRectangularBarPlot()
    ST.addTS3DPolarPlot()
    ST.addTS3DSphericalPlot()
    ST.addTSRectangularContourPlot()
    ST.addTSSmithContourPlot()
    ST.addFFRectangularPlot(f)
    ST.addFFRectangularStackedPlot(f)
    ST.addFFRadiationPattern(f)
    ST.addFFDataTable(f)
    ST.addFF3DRectangularPlot(f)
    ST.addFF3DRectangularBarPlot(f)
    ST.addFF3DPolarPlot(f)
    ST.addFF3DSphericalPlot(f)
    ST.addFFRectangularContourPlot(f)
    #ST.ExportFFRectangularContourPlot()
    #ST.deleteAndClearReports()

    print(ST.getTemplateScript())

    #write test
    filepath = "C:/Users/LCLin/Desktop/test-open-and-sim.py" #open the antenna/previous sim script
    file = open(filepath, "w")
    # Saving the array in a text file
    inputTxt = ST.getTemplateScript()
    for l in inputTxt:
        file.write(l)
    file.close()
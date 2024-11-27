##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './src/simulation_integrator/ANSYS/templateGen_ReportExport.py'
#   Class for ANSYS HFSS report export template generator.
#
#   Note: this ONLY exports reports, not generates them
#   This is the complementary file from TG_simulation.py
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import os.path

class ReportExportTemplate:
    def __init__(self, dataDir):
        self.templateTxt = []
        self.reportNameCtr = 0 #use to index report export across ALL mini batches
        
        self.dataDir = dataDir

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

    def getTemplateScript(self):
        return self.templateTxt
    
    def setTemplateScript(self, t):
        self.templateTxt = t
    
    def clearTemplateScript(self):
        self.templateTxt = []

    def incrementExportReportGroupCounter(self):
        self.reportNameCtr = self.reportNameCtr + 1

    def joinCounterToName(self, ctr, nameBase):
        if ctr == False:
            return nameBase
        else:
            return str(self.reportNameCtr) + "-" + nameBase

    def addTemplateFromMemory(self, lst):
        for l in lst:
            self.templateTxt.append(l)

######################################################################
# single line 'template' calls
######################################################################
    def addSaveProject(self):
        tmpStr = "oProject.Save()\n"
        self.templateTxt.append(tmpStr)
    
    def addExportReportToTemplate(self, filename, plotname):
        fname = repr(filename)#[1:-1]
        #Function used to replace template to reduce number of files with single line commands
        txt = "oModule.ExportToFile(\"" + str(plotname) + "\", r" + str(fname) + ")\n"
        self.templateTxt.append(txt) 

    def deleteAndClearReports(self):
        # self.templateTxt.append("oDesign.DeleteFullVariation(\"All\", False)\n")
        self.templateTxt.append("oModule.DeleteAllReports()\n")
    
    def analyzeAll(self):
        tmpStr = "oDesign.AnalyzeAll()\n"
        self.templateTxt.append(tmpStr)

    def reportSetup(self):
        tmpStr = "oModule = oDesign.GetModule(\"ReportSetup\")\n"
        self.templateTxt.append(tmpStr)

    def addClearSimulatedReports(self):
        self.deleteAndClearReports()

    def addRunNewAnalysis(self):
        self.analyzeAll()
    
    def addReportSetup(self):
        self.reportSetup()

#######################################################################
# Antenna Parameter Report Options
#######################################################################

    def exportAntennaParametersReportTable(self, ctr=False, nameBase="Antenna-Parameters-Table.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename =  os.path.join(self.dataDir, str(name))
        plotname = self.NameAntennaParameterTable
        self.addExportReportToTemplate(filename, plotname)


#######################################################################
# Terminal Solution Data Report Options
#######################################################################

    def exportTSRectangularPlot(self, ctr=False, nameBase="Terminal_S-Parameter_Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name)) 
        plotname = self.NameTSRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSRectangularStackedPlot(self, ctr=False, nameBase="Terminal_S-Parameter_Rectangular-Stacked-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSRectangularStackedPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSPolarPlot(self, ctr=False, nameBase="Terminal_S-Parameter_Polar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSDataTable(self, ctr=False, nameBase="Terminal_S-Parameter_Data-Table.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSDataTable
        self.addExportReportToTemplate(filename, plotname)

    def exportTSSmithChart(self, ctr=False, nameBase="Terminal_S-Parameter_Smith-Chart.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSSmithChart
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DRectangularPlot(self, ctr=False, nameBase="Terminal_S-Parameter_3D-Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTS3DRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DRectangularBarPlot(self, ctr=False, nameBase="Terminal_S-Parameter_3D-Rectangular-Bar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTS3DRectangularBarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DPolarPlot(self, ctr=False, nameBase="Terminal_S-Parameter_3D-Polar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTS3DPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTS3DSphericalPlot(self, ctr=False, nameBase="Terminal_S-Parameter_3D-Spherical-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTS3DSphericalPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSRectangularContourPlot(self, ctr=False, nameBase="Terminal_S-Parameter_Rectangular-Contour-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSRectangularContourPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportTSSmithContourPlot(self, ctr=False, nameBase="Terminal_S-Parameter_Smith-Contour-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameTSSmithContourPlot
        self.addExportReportToTemplate(filename, plotname)

#######################################################################
# Modal Solution Data Report Options
#######################################################################

    def exportMSRectangularPlot(self, ctr=False, nameBase="Modal_S-Parameter_Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name)) 
        plotname = self.NameMSRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMSRectangularStackedPlot(self, ctr=False, nameBase="Modal_S-Parameter_Rectangular-Stacked-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSRectangularStackedPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMSPolarPlot(self, ctr=False, nameBase="Modal_S-Parameter_Polar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSPolarPlot
        self.addExportReportToTemplate(filename, plotname)
        pass

    def exportMSDataTable(self, ctr=False, nameBase="Modal_S-Parameter_Data-Table.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSDataTable
        self.addExportReportToTemplate(filename, plotname)

    def exportMSSmithChart(self, ctr=False, nameBase="Modal_S-Parameter_Smith-Chart.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSSmithChart
        self.addExportReportToTemplate(filename, plotname)

    def exportMS3DRectangularPlot(self, ctr=False, nameBase="Modal_S-Parameter_3D-Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMS3DRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMS3DRectangularBarPlot(self, ctr=False, nameBase="Modal_S-Parameter_3D-Rectangular-Bar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMS3DRectangularBarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMS3DPolarPlot(self, ctr=False, nameBase="Modal_S-Parameter_3D-Polar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMS3DPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMS3DSphericalPlot(self, ctr=False, nameBase="Modal_S-Parameter_3D-Spherical-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMS3DSphericalPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMSRectangularContourPlot(self, ctr=False, nameBase="Modal_S-Parameter_Rectangular-Contour-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSRectangularContourPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportMSSmithContourPlot(self, ctr=False, nameBase="Modal_S-Parameter_Smith-Contour-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameMSSmithContourPlot
        self.addExportReportToTemplate(filename, plotname)

#######################################################################
# Fields Solution Data Report Options
#######################################################################

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

    def exportETRectangularPlot(self):
        pass

    def exportETRectangularStackedPlot(self):
        pass

    def exportETDataTable(self):
        pass

#######################################################################
# Far Fields Data Report Options
#######################################################################

    def exportFFRectangularPlot(self, ctr=False, nameBase="Far-Field_Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFFRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRectangularStackedPlot(self, ctr=False, nameBase="Far-Field_Rectangular-Stacked-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFFRectangularStackedPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRadiationPattern(self, ctr=False, nameBase="Far-Field_3D-Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFFRadiationPattern
        self.addExportReportToTemplate(filename, plotname)

    def exportFFDataTable(self, ctr=False, nameBase="Far-Field_Data-Table.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFFDataTable
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DRectangularPlot(self, ctr=False, nameBase="Far-Field_3D-Rectangular-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFF3DRectangularPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DRectangularBarPlot(self, ctr=False, nameBase="Far-Field_3D-Rectangular-Bar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFF3DRectangularBarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DPolarPlot(self, ctr=False, nameBase="Far-Field_3D-Polar-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFF3DPolarPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFF3DSphericalPlot(self, ctr=False, nameBase="Far-Field_3D-Spherical-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFF3DSphericalPlot
        self.addExportReportToTemplate(filename, plotname)

    def exportFFRectangularContourPlot(self, ctr=False, nameBase="Far-Field_Rectangular-Contour-Plot.csv"):
        name = self.joinCounterToName(ctr, nameBase)
        filename = os.path.join(self.dataDir, str(name))
        plotname = self.NameFFRectangularContourPlot
        self.addExportReportToTemplate(filename, plotname)

#######################################################################
# Antenna Parameters Data Report Options
#######################################################################

    def exportAPRectangularPlot(self):
        pass

    def exportAPRectangularStackedPlot(self):
        pass

    def exportAPDataTable(self):
        pass


#######################################################################
# Add code to export reports to file from user input
#######################################################################
    def exportModalReportData(self, lst, ctr=False):
        for l in lst:
            if l=="Rectangular Plot":
                self.exportMSRectangularPlot(ctr=ctr)
            elif l=="Rectangular Stacked Plot":
                self.exportMSRectangularStackedPlot(ctr=ctr)
            elif l=="Polar Plot":
                self.exportMSPolarPlot(ctr=ctr)
            elif l=="Data Table":
                self.exportMSDataTable(ctr=ctr)
            elif l=="Smith Chart":
                self.exportMSSmithChart(ctr=ctr)
            elif l=="3D Rectangular Plot":
                self.exportMS3DRectangularPlot(ctr=ctr)
            elif l=="3D Rectangular Bar Plot":
                self.exportMS3DRectangularBarPlot(ctr=ctr)
            elif l=="3D Polar Plot":
                self.exportMS3DPolarPlot(ctr=ctr)
            elif l=="3D Spherical Plot":
                self.exportMS3DSphericalPlot(ctr=ctr)
            elif l=="Rectangular Contour Plot":
                self.exportMSRectangularContourPlot(ctr=ctr)
            elif l=="Smith Contour Plot":
                self.exportMSSmithContourPlot(ctr=ctr)
            else:
                pass
                # print("ERROR: Terminal Report Data graph type not recognized")

    def exportTerminalReportData(self, lst, ctr=False):
        for l in lst:
            if l=="Rectangular Plot":
                self.exportTSRectangularPlot(ctr=ctr)
            elif l=="Rectangular Stacked Plot":
                self.exportTSRectangularStackedPlot(ctr=ctr)
            elif l=="Polar Plot":
                self.exportTSPolarPlot(ctr=ctr)
            elif l=="Data Table":
                self.exportTSDataTable(ctr=ctr)
            elif l=="Smith Chart":
                self.exportTSSmithChart(ctr=ctr)
            elif l=="3D Rectangular Plot":
                self.exportTS3DRectangularPlot(ctr=ctr)
            elif l=="3D Rectangular Bar Plot":
                self.exportTS3DRectangularBarPlot(ctr=ctr)
            elif l=="3D Polar Plot":
                self.exportTS3DPolarPlot(ctr=ctr)
            elif l=="3D Spherical Plot":
                self.exportTS3DSphericalPlot(ctr=ctr)
            elif l=="Rectangular Contour Plot":
                self.exportTSRectangularContourPlot(ctr=ctr)
            elif l=="Smith Contour Plot":
                self.exportTSSmithContourPlot(ctr=ctr)
            else:
                pass
                # print("ERROR: Terminal Report Data graph type not recognized")

    def exportFarFieldReportData(self, lst, ctr=False):
        for l in lst:
            if l=="Rectangular Plot":
                self.exportFFRectangularPlot(ctr=ctr)
            elif l=="Rectangular Stacked Plot":
                self.exportFFRectangularStackedPlot(ctr=ctr)
            elif l=="Radiation Pattern":
                self.exportFFRadiationPattern(ctr=ctr)
            elif l=="Data Table":
                self.exportFFDataTable(ctr=ctr)
            elif l=="3D Rectangular Plot":
                self.exportFF3DRectangularPlot(ctr=ctr)
            elif l=="3D Rectangular Bar Plot":
                self.exportFF3DRectangularBarPlot(ctr=ctr)
            elif l=="3D Polar Plot":
                self.exportFF3DPolarPlot(ctr=ctr)
            elif l=="3D Spherical Plot":
                self.exportFF3DSphericalPlot(ctr=ctr)
            elif l=="Rectangular Contour Plot":
                self.exportFFRectangularContourPlot(ctr=ctr)
            else:
                pass
                # print("ERROR: Far Field Report Data graph type not recognized")


    def exportReportsByName(self, nameList, ctr=False):
        for n in nameList:
            plotname = self.joinCounterToName(ctr, n)
            filename = os.path.join(self.dataDir, str(plotname) + ".csv")
            self.addExportReportToTemplate(filename, n)
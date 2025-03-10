##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/page_design.py'
#   Main class for design, import, or editing basic antenna/fss designs
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

# system level imports
import os
import sys
import wx.aui
import wx.lib.newevent
import wx.lib.mixins.inspection as wit
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

# from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg 
from matplotlib.figure import Figure

# local imports
import project.config.antennaCAT_config as c
# import helper_func.graphics_helperFuncs as ghf
from gui.page_design.canvas_draw.calculate_and_draw import CalculateAndDraw
import helper_func.fileIO_helperFuncs as fIO
from gui.page_design.notebook_design import DesignNotebook
from gui.page_design.panel_messageDisplay import MessageDisplay

sys.path.insert(0, './project/')
from project.antennaCAT_project import AntennaCATProject

# default frame/panel sizes
#CHANGE IN CONSTANTS.PY FOR CONSISTENCY ACROSS PROJECT
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
PANEL_HEIGHT = c.PANEL_HEIGHT
PANEL_WIDTH = c.PANEL_WIDTH
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

#static vars for cosmetic features
INPUT_BOX_WIDTH = 100

class DesignPage(wx.Panel):
    def __init__(self, parent, DC, PC, SO):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.DC = DC
        self.PC = PC
        self.SO = SO
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        #canvas
        boxCanvasPreview = wx.StaticBox(self, label='Preview')
        # self.figure = matplotlib.figure.Figure(figsize=(5,5), tight_layout=False)
        self.figure = matplotlib.figure.Figure(figsize=(5,5), tight_layout=True)
        self.axes = self.figure.add_subplot(111, projection="3d")
        self.canvas = FigureCanvas(boxCanvasPreview, -1, self.figure)
        self.navToolbar = NavigationToolbar2Wx(self.canvas) #NavigationToolbar2Wx(self.canvas)
        self.navToolbar.Realize() #still didn't fix the buttons changing colors,
        
        
        #design options notebook creation
        boxDesignOptions = wx.StaticBox(self, label='Design Options')
        self.notebook_design = DesignNotebook(boxDesignOptions, self, self.DC, self.PC)
        self.notebook_design.SetMinSize((100, HEIGHT-100))

        #summary box
        boxDesignSummary = wx.StaticBox(self, label='Design Summary:')
        self.designSummaryTxt = MessageDisplay(boxDesignSummary)
        
        #generate button + bindings
        self.btnGenerate = wx.Button(self, label="Generate Script", size=(90, -1))
        self.btnGenerate.Bind(wx.EVT_BUTTON, self.btnGenerateClicked)
        self.btnExport = wx.Button(self, label="Export Script", size=(90, -1))
        self.btnExport.Bind(wx.EVT_BUTTON, self.btnExportClicked)

        # btn sizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        btnSizer.Add(self.btnExport, 0, wx.ALL, border=10)
        btnSizer.Add(self.btnGenerate, 0, wx.ALL, border=10)
        
        # summary sizer
        summarySizer = wx.BoxSizer(wx.VERTICAL)
        summarySizer.AddSpacer(10)
        summarySizer.Add(self.designSummaryTxt, 1, wx.ALL|wx.EXPAND, border=5)
        boxDesignSummary.SetSizer(summarySizer)

        # 'left side sizer'
        boxDesignSizer = wx.BoxSizer(wx.VERTICAL)
        boxDesignSizer.AddSpacer(5)
        boxDesignSizer.Add(self.notebook_design, 0, wx.ALL | wx.EXPAND, border=15)
        boxDesignOptions.SetSizer(boxDesignSizer)

        #preview sizer
        # 'right side sizer'
        canvasSizer = wx.BoxSizer(wx.VERTICAL)
        canvasSizer.AddSpacer(20)
        canvasSizer.Add(self.canvas, 0, wx.CENTER|wx.EXPAND, border=15)  #the 3d graph
        canvasSizer.Add(self.navToolbar, 0,  wx.CENTER)
        boxCanvasPreview.SetSizer(canvasSizer)

        previewSizer = wx.BoxSizer(wx.VERTICAL)
        previewSizer.Add(boxCanvasPreview, 0, wx.ALL | wx.EXPAND, border=5)
        previewSizer.Add(boxDesignSummary, 1, wx.ALL|wx.EXPAND, border=5)
        previewSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND) #, border=10)      

        #main sizer
        pageSizer = wx.BoxSizer(wx.HORIZONTAL)
        pageSizer.Add(boxDesignOptions, 1, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(previewSizer, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)


    def draw3DDesignOnCanvas(self):
        self.axes.clear()
        #TODO:replace this with DrawAntenna class
        #try:
        print("calling draw3DDesignOnCanvas() on page_design")
        cDraw = CalculateAndDraw()
        if self.PC.getAntennaGeneratorBoolean() == True:
            cDraw.calculateGeneratedCoordinates(self.axes, self.DC.getFeatures(), self.DC.getParams())
        elif self.PC.getCustomConductorBoolean() ==True:
            shapeVec =[]
            cDraw.parseImportedConductorDesignCoordinates(self.axes, shapeVec)
        #except Exception as e:
        #    print(e)
        #    self.updateSummaryText("skipping drawing for now from page_design.py. Updating drawing class")
        self.canvas.draw()

        # called from here because EVERYTHING that calls this would call it right after the draw
        # and there's no point in adding more functions 3+ levels deep
        self.updateProjectValues() 


    def btnGenerateClicked(self, evt=None):
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
        self.generateScript() 
        

    def generateScript(self):
        noError = False
        #generate the design script 
        # - saved in self.DC until it's written out somewhere
        #check if sim obj has been selected
        if (self.PC.getSimulationSoftware() == None):
            msg = "no EM simulation software detected. Configure this in settings"
            self.updateSummaryText(msg)
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)
            return noError
        #check if design has been created
        if (self.PC.checkDesignCreated()==True):
            self.SO.designTemplateGen() #saves to DC while creating
            self.PC.setDesignScriptCreatedBool(True)
            self.updateSummaryText("Design script generated")
            noError = True
        else:
            self.updateSummaryText("ERROR: cannot generate template. no design config")            
            noError = False    
        return noError


    def btnExportClicked(self, evt=None):
        if self.PC.getDesignConfigBool() == False:
            self.updateSummaryText("No design detected to export")
            return
        if self.PC.getDesignScriptCreatedBool() == False:
            self.updateSummaryText("Generating script before export")
            noError = self.generateScript()
            if noError == False:
                return
        #get script text
        scriptTxt = self.DC.getDesignScript()
        #write out to the scripts file  in the antennaCAT project
        try:
            pathname = self.PC.getScriptDirectory()
            fileExt = self.SO.getExpectedScriptFileExtension()
            pathname = os.path.join(pathname, "exported-design" + str(fileExt))
            fIO.writeOut(pathname, scriptTxt)
            msg = "file exported to " + str(pathname)
            self.updateSummaryText(msg)
        except Exception as e:
                msg = "Cannot save current data in file " + str(pathname)
                self.updateSummaryText(msg)
                self.updateSummaryText(e)

    def updateSummaryText(self, t):
        self.designSummaryTxt.updateText(str(t))


    def updateProjectValues(self):
        #used to propogate out settings caused by design selections
        self.parent.updateProjectValues()
    
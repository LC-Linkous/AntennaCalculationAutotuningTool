##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/gui_main/gui_main.py'
#   Class for GUI layout and basic functionality
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 30, 2024
##--------------------------------------------------------------------\

import sys
import os
import wx

sys.path.insert(0, './gui')
from gui.gui_main.panel_buttonMenu import ButtonMenuPanel
from gui.gui_main.panel_main import MainPanel
from gui.gui_main.menu_bar import MenuBar

sys.path.insert(0, './simulation_integrator/')
from simulation_integrator.simulation_integrator import SimulationIntegrator
sys.path.insert(0, './project/')
from project.antennaCAT_project import AntennaCATProject

import project.config.antennaCAT_config as c
from project.config.design_config import DesignConfiguration
from project.config.project_config import ProjectConfiguration

# default frame/panel sizes and visuals
#CHANGE IN CONSTANTS.PY FOR CONSISTENCY ACROSS PROJECT
WIDTH = c.WIDTH
HEIGHT = c.HEIGHT
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
SIDEBAR_COLOR = c.SIDEBAR_COLOR
ANTENNACAT_ICON_FILE = c.ANTENNACAT_ICON_FILE


PROG_DIR_LIST = c.PROG_DIR_LIST
PROG_FILES_LIST = c.PROG_FILES_LIST
PROG_TEMP_PATH = c.PROG_TEMP_PATH

#######################################################################
# Classes for basic GUI frame creation
#######################################################################

class GFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, title=title, size=(WIDTH, HEIGHT))
        self.SetIcon(wx.Icon(ANTENNACAT_ICON_FILE, wx.BITMAP_TYPE_PNG))
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.DC = DesignConfiguration()
        self.PC = ProjectConfiguration()
        #this is where the initial object is made. can be changed based on loaded sim config settings
        self.SO = SimulationIntegrator(self.DC, self.PC) 

        mb = MenuBar(self)
        self.SetMenuBar(mb) 
        self.panel_btnMenu = ButtonMenuPanel(self)
        self.panel_mainUI = MainPanel(self, self.DC, self.PC, self.SO)

        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(self.panel_btnMenu, 0, wx.EXPAND)
        self.mainSizer.Add(self.panel_mainUI, 3, wx.EXPAND)
        self.SetSizer(self.mainSizer)


        #config and check calls
        self.loadAntennaCATSystemFiles()


    #btn events called from children
    def onClose(self, evt=None):
        self.Destroy()
    
    def saveProject(self):
        acp = AntennaCATProject(self.DC, self.PC, self.SO)
        acp.saveProject() 

    def saveAsProject(self):
        with wx.FileDialog(self, "Save antennaCAT project", wildcard="AntennaCAT files (*.ancat)|*.ancat",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return   # user cancelled
            pathname = fileDialog.GetPath()
            try:
                acp = AntennaCATProject(self.DC, self.PC, self.SO)
                acp.saveAsProject(pathname)
            except Exception as e:
                print(e)   

    def openSettings(self):
        self.panel_btnMenu.btnSettingsClicked()
    
    def openHome(self):
        self.panel_btnMenu.btnProjectClicked()

    def btnNewProjectClicked(self, evt=None):
        #called from page_project.py
        #select save location
        with wx.FileDialog(self, "Save antennaCAT project", wildcard="AntennaCAT files (*.ancat)|*.ancat",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return   # user cancelled
            pathname = fileDialog.GetPath()
            try:
                acp = AntennaCATProject(self.DC, self.PC, self.SO)
                acp.createNewProject(pathname)
                #open settings page to finish the project setup
                self.panel_btnMenu.btnSettingsClicked()
            except Exception as e:
                print(e) 

    def btnOpenProjectClicked(self, evt=None):
        #called from page_project.py
        #TODO:
            # if edits have been made, 
            # prompt to save or discard current design

        # open file browser
        with wx.FileDialog(self, "Open an AntennaCAT project", wildcard="AntennaCAT files (*.ancat)|*.ancat",
                style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # user cancelled
            # get pathname
            pathname = fileDialog.GetPath()
        #attempt to open
        try:
            self.openProjectCheck(pathname)
        except Exception as e:
            print(e)
           

    def recentProjectClicked (self, pathname):
        #called from page_project notebook
        self.openProjectCheck(pathname)
        

    def openProjectCheck(self, pathname):
        # called by the open file btn and clicking recent from panel
        print("open project selected. this functionality does not exist yet, but save location is used")
        # check that project file and needed directories exist
        acp = AntennaCATProject(self.DC, self.PC, self.SO)
        acp.openExistingProject(pathname) #sets PC

        #apply settings
        self.applyLoadedProjectSettings()

        # trigger design button push to show design page as first page
        self.panel_btnMenu.btnDesignClicked()            

    def applyLoadedProjectSettings(self):
        # no PC pass bc it calls UP
        self.panel_mainUI.applyLoadedProjectSettings()


   
    def loadAntennaCATSystemFiles(self):
        # needs access to self.DC, self.PC, self.SO

        #TODO when AntennaCAT is avilable as an .exe:
            # root folder starts with where the EXE is installed. 
            # shortcut option placed on desktop to exe



        # For when funning AntennaCAT in an IDE
            # currently no extra code needed
            # set path vars in config files
            

        # Folders, cache, and error checks for both options
            # directory checking
                # tmp folder (genreal cache)
                # any EM simulation software configs needed (if templates need versioning)
                # last user information for faster project creation


        for dirPath in PROG_DIR_LIST:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

        for filePath in PROG_FILES_LIST:
            print(filePath)
            if not os.path.exists(filePath):
                with open(filePath, 'w') as file:
                    file.write("")




    def clearProjectCache(self):
        #called from settings folder to reset projects that have recurring issues
        msg = "This action will permanently delete the local settings for this project. \n" +\
             "It cannot be undone. Delete project cache?"

        dlg = wx.MessageDialog(None, msg,'Delete Project Cache',wx.CANCEL|wx.CANCEL_DEFAULT | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            if os.path.exists(PROG_TEMP_PATH):
                os.remove(PROG_TEMP_PATH)
            output_msg = "Project cache has been cleared"
            self.loadAntennaCATSystemFiles()
        else:
            output_msg = "Project cache has not been deleted"

        return output_msg


    def clearAntennaCATCache(self):
        #called from settings folder to reset projects that have recurring issues
        msg = "This action will permanently delete the local cache and custom settings for AntennaCAT. \n" +\
             "It cannot be undone. Reset AntennaCAT settings?"

        dlg = wx.MessageDialog(None, msg,'Reset AntennaCAT Settings',wx.CANCEL|wx.CANCEL_DEFAULT | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            for dirPath in PROG_DIR_LIST:
                if os.path.exists(dirPath):
                    os.remove(dirPath)
            output_msg = "AntennaCAT cache and settings have been reset"
            self.loadAntennaCATSystemFiles()
        else:
            output_msg = "AntennaCAT settings have not been deleted"

        return output_msg
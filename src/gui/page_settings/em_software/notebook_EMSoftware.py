##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/EM_software/notebook_EMSoftware.py'
#   Class for project settings
#
#    TODO: ADD THE HOOKS BACK IN AFTER 2024.0
#
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import wx

import project.config.antennaCAT_config as c
from gui.page_settings.em_software.panel_EMSoftwareConfig import EMSoftwareConfigNotebookPage

 
MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
#executable is the name of the exe, not the full path
ANSYS_EXECUTABLE = c.ANSYS_EXECUTABLE
COMSOL_EXECUTABLE = c.COMSOL_EXECUTABLE
CST_EXECUTABLE = c.CST_EXECUTABLE
EMPIRE_EXECUTABLE = c.EMPIRE_EXECUTABLE
FEKO_EXECUTABLE = c.FEKO_EXECUTABLE

class EMSoftwareNotebook(wx.Notebook):
    def __init__(self, parent, controller):
        wx.Notebook.__init__(self, parent=parent, size=(450, -1))
        self.parent = parent # the widget control, used to control the notebook UI
        self.controller = controller # the control class that's 1 step above

        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        self.defaultEM = None
       
        self.page_ansys = EMSoftwareConfigNotebookPage(self, "ANSYS", executable=ANSYS_EXECUTABLE)
        # self.page_comsol = EMSoftwareConfigNotebookPage(self, "COMSOL", executable=COMSOL_EXECUTABLE)
        # self.page_cst = EMSoftwareConfigNotebookPage(self, "CST", executable=CST_EXECUTABLE)
        # self.page_empire = EMSoftwareConfigNotebookPage(self, "EMPIRE", executable=EMPIRE_EXECUTABLE)
        # self.page_feko = EMSoftwareConfigNotebookPage(self, "FEKO", executable=FEKO_EXECUTABLE)

        self.AddPage(self.page_ansys, "ANSYS")

        # it's easier to comment these out than pull every single file
        # self.AddPage(self.page_comsol, "COMSOL")
        # self.AddPage(self.page_cst, "CST")
        # self.AddPage(self.page_empire, "EMPIRE")
        # self.AddPage(self.page_feko, "FEKO")

        #set default as ANSYS for development
        self.page_ansys.checkMakeDefaultEMSoftware()
        self.setDefaultEM("ANSYS")

    def getDefaultEMSoftware(self):
        return self.defaultEM
    
    def getEMSettings(self):
        #TODO:
        #DF object with 
        # self.EMSoftwareID, self.fullExePath, numLicenses, useSingle, defaultSoftware
        # to save to PC

        return self.getANSYSSettings()




    def getANSYSSettings(self):
       return self.page_ansys.getValues()

    # def getCOMOLSettings(self):
    #    return self.page_comsol.getValues()
    
    # def getCSTSettings(self):
    #     return self.page_cst.getValues()
    
    # def getEMPIRESettings(self):
    #     self.page_empire.getValues()
    
    # def getFEKOSettings(self):
    #     self.page_feko.getValues()

    def setDefaultEM(self, emName):
        self.defaultEM = emName
        #uncheck other boxes
        # if emName == "ANSYS":
        #     self.page_comsol.uncheckMakeDefaultEMSoftware()
        #     self.page_cst.uncheckMakeDefaultEMSoftware()
        #     self.page_empire.uncheckMakeDefaultEMSoftware()
        #     self.page_feko.uncheckMakeDefaultEMSoftware()
        # elif emName == "COMSOL":
        #     self.page_ansys.uncheckMakeDefaultEMSoftware()
        #     self.page_cst.uncheckMakeDefaultEMSoftware()
        #     self.page_empire.uncheckMakeDefaultEMSoftware()
        #     self.page_feko.uncheckMakeDefaultEMSoftware()
        # elif emName == "CST":
        #     self.page_ansys.uncheckMakeDefaultEMSoftware()
        #     self.page_comsol.uncheckMakeDefaultEMSoftware()
        #     self.page_empire.uncheckMakeDefaultEMSoftware()
        #     self.page_feko.uncheckMakeDefaultEMSoftware()
        # elif emName == "EMPIRE":
        #     self.page_ansys.uncheckMakeDefaultEMSoftware()
        #     self.page_comsol.uncheckMakeDefaultEMSoftware()
        #     self.page_cst.uncheckMakeDefaultEMSoftware()
        #     self.page_feko.uncheckMakeDefaultEMSoftware()
        # elif emName == "FEKO":
        #     self.page_ansys.uncheckMakeDefaultEMSoftware()
        #     self.page_comsol.uncheckMakeDefaultEMSoftware()
        #     self.page_cst.uncheckMakeDefaultEMSoftware()
        #     self.page_empire.uncheckMakeDefaultEMSoftware()



    def triggerSettingsPageSaveButtonClick(self):
        self.controller.saveSettingsPage()
            
    def applyLoadedProjectSettings(self, PC):
        self.page_ansys.applyLoadedProjectSettings(PC)
        # self.page_comsol.applyLoadedProjectSettings(PC)
        # self.page_cst.applyLoadedProjectSettings(PC)        
        # self.page_empire.applyLoadedProjectSettings(PC)
        # self.page_feko.applyLoadedProjectSettings(PC)



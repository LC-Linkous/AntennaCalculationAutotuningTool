##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   './src/gui/gui_main/menu_bar.py'
#   Class for frame level menu toolbar
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import wx

class MenuBar(wx.MenuBar):             
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent

        #'File'
        ## new
        fileMenu = wx.Menu() 
        newProject = wx.MenuItem(fileMenu, id=10, text = "&New Project", kind = wx.ITEM_NORMAL) 
        fileMenu.Append(newProject)             
        fileMenu.AppendSeparator()    

        ## open existing
        openProject = wx.MenuItem(fileMenu, id=11, text = "&Open Project", kind = wx.ITEM_NORMAL) 
        fileMenu.Append(openProject)             
        fileMenu.AppendSeparator()    

        ## save
        saveProject = wx.MenuItem(fileMenu, id=12, text = "&Save", kind = wx.ITEM_NORMAL) 
        saveAsProject = wx.MenuItem(fileMenu, id=13, text = "Save As", kind = wx.ITEM_NORMAL) 
        fileMenu.Append(saveProject)   
        fileMenu.Append(saveAsProject)             
        fileMenu.AppendSeparator()    

        ## preferences and settings
        userSettings = wx.MenuItem(fileMenu, id=14, text = "&Settings", kind = wx.ITEM_NORMAL) 
        fileMenu.Append(userSettings)   
        fileMenu.AppendSeparator()     

        ## exit 
        exit = wx.MenuItem(fileMenu, id=15, text = "&Exit", kind = wx.ITEM_NORMAL) 
        fileMenu.Append(exit)   

        # Home
        self.homeMenu = wx.Menu() 

        # Help
        helpMenu = wx.Menu() 
        ## documentation
        documentation = wx.MenuItem(helpMenu, id=30, text = "&Documentation", kind = wx.ITEM_NORMAL) 
        helpMenu.Append(documentation)             
        helpMenu.AppendSeparator()    
        ## about
        about = wx.MenuItem(helpMenu, id=31, text = "&About", kind = wx.ITEM_NORMAL) 
        helpMenu.Append(about)             

        self.Append(fileMenu, '&File')
        self.Append(self.homeMenu, '&Home')
        self.Append(helpMenu, '&Help')

        self.Bind(wx.EVT_MENU, self.submenuHandler) # submenu evts
        self.Bind(wx.EVT_MENU_OPEN, self.menuHandler) #menubar evts

    def menuHandler(self, evt):
        #main menubar evts     
        if evt.GetMenu() == self.homeMenu:
            self.parent.openHome()            

    def submenuHandler (self, evt): 
        #submenu dropdowns
        id = evt.GetId() 
        if id == 10: #new
            self.parent.btnNewProjectClicked()
        elif id == 11: #open
            self.parent.btnOpenProjectClicked()
        elif id == 12: #save
            self.parent.saveProject()
        elif id == 13: #save as
            self.parent.saveAsProject()
        elif id == 14: #preferences
            self.parent.openSettings()
        elif id == 15: #exit
            self.parent.onClose()
        elif id == 20: #home
            self.parent.openHome()
        elif id == 30: #documentation
            print("documentation call not set")
        elif id == 31: #about
            print("about page call not set")

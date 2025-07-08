##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/user_settings/panel_userInformation.py'
#   Class for project settings - user information
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 6, 2025
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR

class AnCATNotebookPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # Author information (optional)
        # project comments 
        boxComment = wx.StaticBox(self, label='Welcome to AntennaCAT!')
        commentScroll = scrolled.ScrolledPanel(boxComment, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        commentScroll.SetAutoLayout(1)
        commentScroll.SetupScrolling()
        self.commentTxt = wx.StaticText(commentScroll, style=wx.TE_MULTILINE|wx.TE_RICH, size=(450, -1))
        self.commentTxt.Wrap(450)
        self.commentTxt.SetBackgroundColour((235,235,235))

        # comments
        commentSizer = wx.BoxSizer(wx.VERTICAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)
        scrollSizer.Add(self.commentTxt, 1, wx.ALL|wx.EXPAND, border=0)
        commentScroll.SetSizer(scrollSizer)
        commentSizer.Add(commentScroll, 1, wx.ALL|wx.EXPAND, border=15)
        boxComment.SetSizer(commentSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxComment, 1, wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(pageSizer)

        self.setCommentText()
    
    def setCommentText(self):
        s = "\nThe Antenna Calculation and Autotuning Tool (AntennaCAT) software suite is a comprehensive " \
        "implementation of machine learning to automate, evaluate, and optimize the antenna design " \
        "process using EM simulation software. It utilizes a combined antenna designer pre-loaded with" \
        " replication studies and internal calculator to accelerate the CAD construction and EM simulation " \
        "of several common topologies, while eliminating model disparity for automated data collection." \
        " In particular, this work includes the capability to create and export structured datasets from " \
        "the aforementioned EM software for iterative improvement and includes an expandable selection " \
        "of optimizers. AntennaCAT is designed with three things in mind: accessibility, adaptability, and experimentation.\n" \


        self.commentTxt.SetLabel(s)


    def getValues(self):
        pass
    
    def applyLoadedProjectSettings(self, PC):
        pass
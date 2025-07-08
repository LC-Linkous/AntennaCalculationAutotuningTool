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

class UserInfoNotebookPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # Author information (optional)
        boxAuthor= wx.StaticBox(self, label='Author Information (Optional)')
        self.fieldAuthor = wx.TextCtrl(boxAuthor, style=wx.TE_MULTILINE|wx.TE_RICH, size=(-1, 40))
     
        # project comments 
        boxComment = wx.StaticBox(self, label='Project Comments')
        commentScroll = scrolled.ScrolledPanel(boxComment, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        commentScroll.SetAutoLayout(1)
        commentScroll.SetupScrolling()
        self.commentTxt = wx.TextCtrl(commentScroll, style=wx.TE_MULTILINE|wx.TE_RICH)


        # sizers
        # author
        authorSizer = wx.BoxSizer(wx.VERTICAL)
        authorSizer.Add(self.fieldAuthor, 0, wx.ALL| wx.EXPAND, border=15)
        boxAuthor.SetSizer(authorSizer)

        # comments
        commentSizer = wx.BoxSizer(wx.VERTICAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)
        scrollSizer.Add(self.commentTxt, 1, wx.ALL|wx.EXPAND, border=0)
        commentScroll.SetSizer(scrollSizer)
        commentSizer.Add(commentScroll, 1, wx.ALL|wx.EXPAND, border=15)
        boxComment.SetSizer(commentSizer)

        ## main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(boxAuthor, 0, wx.ALL | wx.EXPAND, border=5)
        pageSizer.Add(boxComment, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(pageSizer)

    
    def getValues(self):
        authorName = self.fieldAuthor.GetValue()
        comments = self.commentTxt.GetValue()
        return authorName, comments

    def applyLoadedProjectSettings(self, PC):
        pass
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

class LicenseNotebookPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour(MAIN_BACKGROUND_COLOR)

        # Author information (optional)
        # project comments 
        boxComment = wx.StaticBox(self, label='AntennaCAT Licensing')
        commentScroll = scrolled.ScrolledPanel(boxComment, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        commentScroll.SetAutoLayout(1)
        commentScroll.SetupScrolling()
        self.commentTxt = wx.StaticText(commentScroll, style=wx.TE_MULTILINE|wx.TE_RICH, size=(450, -1))
        self.commentTxt.Wrap(200)
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
        s = " Lorem ipsum dolor sit amet, consectetur adipiscing elit." \
        " Fusce metus dolor, ultrices in blandit sit amet, dictum id velit. Nullam scelerisque " \
        "velit bibendum dui placerat, eget euismod ligula malesuada. Vestibulum cursus nulla est," \
        " et feugiat nisl gravida ut. Donec eleifend dui ac lorem ullamcorper tempus. Aenean pharetra ipsum interdum, egestas mauris nec, ultrices odio. Maecenas lobortis, justo ac vehicula finibus, nisl " \
        "turpis vulputate sapien, in tempus mauris felis in enim. Mauris finibus vulputate neque. Vivamus consequat sapien et eros euismod, a dignissim arcu maximus. Aenean pellentesque risus ut sem ullamcorper" \
        " sagittis.Sed nec posuere sem. Curabitur ultrices tellus elit, eu iaculis justo consequat vitae. Nulla laoreet congue rutrum. Orci varius natoque penatibus et magnis dis parturient montes," \
        " nascetur ridiculus mus. Ut et ultricies felis, lacinia aliquet erat. Phasellus rhoncus, odio blandit ornare fermentum, quam dui hendrerit ante, sed molestie lacus tortor iaculis nunc. Sed consectetur " \
        "orci luctus, luctus felis vel, suscipit lectus. Mauris facilisis, arcu ac finibus fermentum, quam odio mollis quam, elementum tempor diam ligula a odio. Nunc congue aliquet pulvinar. Praesent feugiat orci" \
        " quis orci hendrerit, ac malesuada velit ornare. Nam efficitur turpis eu mauris interdum eleifend. Integer varius risus libero, eget auctor felis fringilla tempor. " \
        "Donec fermentum nibh est, at posuere leo mollis ac. Maecenas at tortor leo. Pellentesque consectetur libero ut arcu pulvinar sodales. Mauris fermentum quam tellus, ut eleifend mi condimentum a. "

        self.commentTxt.SetLabel(s)


    def getValues(self):
        pass
    
    def applyLoadedProjectSettings(self, PC):
        pass
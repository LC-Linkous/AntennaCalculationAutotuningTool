##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_settings/user_settings/panel_userInformation.py'
#   Class for project settings - user information
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: July 23, 2025
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
        boxComment = wx.StaticBox(self, label='AntennaCAT Licensing Summary')
        commentScroll = scrolled.ScrolledPanel(boxComment, 0, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        commentScroll.SetAutoLayout(1)
        commentScroll.SetupScrolling()
        self.commentTxt = wx.StaticText(commentScroll, style=wx.TE_MULTILINE|wx.TE_RICH, size=(450, -1))
        self.commentTxt.Wrap(450)
        self.commentTxt.SetBackgroundColour((240,240,240))
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.commentTxt.SetFont(font)

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
        s = "\n\t The core AntennaCAT software has been released under the GNU GENERAL PUBLIC LICENSE Version 2 (GPL-2.0) license." \
        "This license in full is available on the AntennaCAT repo and with a copy of this code in the LICENSE file. " \
        "\n\t HOWEVER, not all software included in this suite has been released under the GPL-2.0 license. Included dependencies and derivative features, such as the " \
        "Antenna Calculator and the optimizer implementations, may have been released by their respective original creators under a different license. " \
        "These dependencies may be under a more restrictive (or less restrictive) license." \
        "AntennaCAT's license does NOT take priority over those software - they are modularly integrated for educational purposes, and not all of" \
        "them were designed for AntennaCAT. Refer to the documentation for links to these dependencies and their respective licenses." \
        "\n\t The AntennaCAT software suite (and associated tools and programs) do NOT provide ANY EM simulation software licenses for EM simulation software tools and " \
        "suites that may be compatible with AntennaCAT. EM simulation software licenses must be purchased from the appropriate vendor, and users are responsible for following" \
        "the regulations and license restrictions for their location and EM Simulation software license. AntennaCAT is provided AS-IS, open source, and FREE, with " \
        "no warranty, and NO support from the EM simulation software companies with software systems that may be compatible with AntennaCAT. Compatibility with " \
        "AntennaCAT does not indicate a partnership or affiliation between the EM simulation software companies and any AntennaCAT software or tools. Software compatibility is subject to change to " \
        "respect the rights and regulations of the respective EM simulation software tool companies and owners." \
        "\n\t" 

        self.commentTxt.SetLabel(s)


    def getValues(self):
        pass
    
    def applyLoadedProjectSettings(self, PC):
        pass
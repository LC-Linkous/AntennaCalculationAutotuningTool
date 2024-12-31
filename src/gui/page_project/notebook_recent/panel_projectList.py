##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   '.src/gui/page_project/notebook_recent/panel_projectList.py'
#   Class for showing linkable antennaCAT project files
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: December 30, 2024
##--------------------------------------------------------------------\

import wx
import wx.lib.scrolledpanel as scrolled
import time

import project.config.antennaCAT_config as c

MAIN_BACKGROUND_COLOR = c.MAIN_BACKGROUND_COLOR
GREY_BACKGROUND_COLOR = c.GREY_BACKGROUND_COLOR


class ProjectListPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        # Set the background color of the panel to grey
        self.SetBackgroundColour(GREY_BACKGROUND_COLOR)

        # Sample data: list of [key, value, date/time]
        self.projectlist = []
        #     ["Project A", "Description for project A", "2024-12-01 14:30:00"],
        #     ["Project B", "Description for project B", "2024-12-02 16:45:00"],
        #     ["Project C", "Description for project C", "2024-12-03 09:00:00"],
        #     ["Project D", "Description for project D", "2024-12-04 12:15:00"],
        #     ["Project E", "Description for project E", "2024-12-05 08:20:00"]
        # ]

        # Create a scrolled panel to hold the items
        designScroll = scrolled.ScrolledPanel(self, 1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        designScroll.SetAutoLayout(1)
        designScroll.SetupScrolling()

        # Create a main vertical sizer for layout
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        # Add header row with font applied
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        project_name_label = wx.StaticText(designScroll, label="Project Name")
        headerSizer.Add(project_name_label, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        path_label = wx.StaticText(designScroll, label="Date Modified")
        headerSizer.Add(path_label, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        scrollSizer.Add(headerSizer, 0, wx.EXPAND | wx.ALL, 5)

        # Create a font with size 14
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        # Check if the project list is empty
        if not self.projectlist:
            # If the list is empty, show a "No recent projects" message
            no_projects_label = wx.StaticText(designScroll, label="No recent projects")
            no_projects_label.SetFont(font)
            scrollSizer.Add(no_projects_label, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        else:
            # Iterate over the list to create a CustomButton for each item
            for project in self.projectlist:
                # Create a custom button
                key, value, timestamp = project
                custom_button = CustomButton(designScroll, key, value, timestamp)
                
                # Add this custom button to the sizer
                scrollSizer.Add(custom_button, 0, wx.EXPAND | wx.ALL, 5)

        # Set the sizer for the scrolled panel
        designScroll.SetSizer(scrollSizer)

        # Create the page sizer and add the scrolled panel to it
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)
        self.pageSizer.Add(designScroll, 1, wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(self.pageSizer)

    def applyLoadedProjectSettings(self, PC):
        pass


# custom button class to display summarized project information
class CustomButton(wx.Panel):
    def __init__(self, parent, key, value, timestamp):
        wx.Panel.__init__(self, parent)

        # Set initial background color (normal state)
        self.SetBackgroundColour(GREY_BACKGROUND_COLOR)
        
        # Create a sizer for the custom button
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create a sizer for the left part of the button (key + value)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create and set the font for the key
        key_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        key_text = wx.StaticText(self, label=key)
        key_text.SetFont(key_font)
        left_sizer.Add(key_text, 0, wx.ALL | wx.ALIGN_LEFT, 3)
        
        # Create and set the font for the value (smaller size)
        value_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        value_text = wx.StaticText(self, label=value)
        value_text.SetFont(value_font)
        left_sizer.Add(value_text, 0, wx.ALL | wx.ALIGN_LEFT, 3)

        # Add left part to the button's sizer
        self.sizer.Add(left_sizer, 1, wx.ALL | wx.EXPAND, 5)
        
        # Create the right side (date/time) label
        timestamp_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        timestamp_text = wx.StaticText(self, label=timestamp)
        timestamp_text.SetFont(timestamp_font)
        
        # Add the right part (date/time) to the button's sizer
        self.sizer.Add(timestamp_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        # Set the sizer for the custom button
        self.SetSizer(self.sizer)

        # Bind events to allow the button to be clicked and highlighted
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_UP, self.on_click)
    
    def on_hover(self, event):
        # Change background color when mouse enters the button area
        self.SetBackgroundColour(wx.Colour(180, 180, 180))  # Lighter grey on hover
        self.Refresh()  # Refresh the button to update the background color
    
    def on_leave(self, event):
        # Revert to original background color when mouse leaves
        self.SetBackgroundColour(GREY_BACKGROUND_COLOR)
        self.Refresh()  # Refresh the button to update the background color
    
    def on_click(self, event):
        # You can handle the button click here, for example:
        print(f"Button clicked: {self.GetChildren()[0].GetLabel()}")
        self.SetBackgroundColour(wx.Colour(150, 150, 150))  # Darker grey on click
        self.Refresh()  # Refresh the button to update the background color


##--------------------------------------------------------------------\
#   Frequency Selective Surface Calculation Autotuning Tool
#   '.gui/page_design/canvas_draw/drawDesign.py'
#   Class for drawing to the matplotlib canvas. 
#       replaces the helper_funcs version
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\


import numpy as np

ZEROS_ARR = [0, -0, 0.0, -0.0] #cover the different ways zeros can be represented (also deals w weird user input)

class DrawDesign: 
    def __init__(self):
        pass
        

    def setupCanvas(self, ax, units="mm"):
        #takes in the axes for plotting in matplotlib chart
        ax.clear()
        self.updateCanvas(ax, units=units)

    def matplotlibColorConversion(self, color):
        #convert from 0-255 scale to 0-1 scale
        #also deals with RGBA to RGB
        col = []
        if (color[0] >= 1) or (color[1] >=1) or (color[1] >=1):
            col = tuple([color[0]/255, color[1]/255, color[2]/255])
        else:
            col = tuple([color[0], color[1], color[2]])

        return col

    def updateCanvas(self, ax, view=[-75, 90, 0], units="mm", equal=True):
        ax.set_xlabel('x_size ('+ str(units) + ')')
        ax.set_ylabel('y_size ('+ str(units) + ')')
        ax.set_zlabel('z_size ('+ str(units) + ')')
        ax.view_init(elev=view[0], azim=view[1], roll=view[2])    #set to look at XY plane (-90,90, 0), with a bit of an angle
        if equal == True:
           ax.axis('equal') #for equal scale so no distortion
        
    def setEnviornmentParams(self, bendAngle=0, offset=[0,0,0], *args):
        self.bendAngle = float(bendAngle)        
        self.k = offset[0]
        self.h = offset[1]
        self.f = offset[2]
        self.offset = offset #(x,y,z) for future feature options
        self.arcCenter = 0


    def setSuperstrateParams(self, superstrateLayers=[], *args):
        self.superstrateLayers = superstrateLayers
        self.superstrateParams = args[0]

    def setConductorParams(self, conductorType=None, conductorFeed=None, conductorLayers=[], *args):
        self.conductorType = conductorType
        self.conductorFeed = conductorFeed
        self.conductorLayers = conductorLayers
        self.conductorParams = args[0]

    def setSubstrateParams(self, substrateLayers=[], *args):
        self.substrateLayers = substrateLayers
        self.substrateParams = args[0]
    
    def setSuperstrateParams(self, superstrateLayers=[], *args):
        return self.superstrateParams

    def getConductorParams(self, conductorType=None, conductorFeed=None, conductorLayers=[], *args):
        return self.conductorParams

    def getSubstrateParams(self, substrateLayers=[], *args):
        return self.substrateParams

    def getPoints(self):
        return self.substratePts, self.conductorPts, self.superstratePts, self.substrateSheetEqs 
    
    def drawAntenna(self, ax, units="mm"):
        #same name as graphics helper funcs that AntennaCAT uses bc they'll be merged eventually
        self.setupCanvas(ax, units)
        if self.bendAngle==0:
             subPts, conPts, supPts = self.drawFlatAntenna(ax, units)
        else:
            subPts, conPts, supPts, subEqs = self.drawCurvedAntenna(ax, units)
        
        self.substratePts = subPts
        self.conductorPts = conPts
        self.superstratePts = supPts
        self.substrateSheetEqs = subEqs

    def drawFlatAntenna(self, ax, units):
        subPts =[]
        conPts=[]
        supPts=[]
        if len(self.substrateLayers) <1:
            print("No substrate layers to draw")
        else:
            #TODO: if/else for selecting shape of substrate 
            subPts  = self.flatRectangleSubstrate(ax)
            ax.axis([(-1.25*self.x_lim)+self.k,  (1.25*self.y_lim)+self.h,    self.k,  (1.25*self.y_lim)+self.h])

        if len(self.conductorLayers) <1:
            print("No conductor layers to draw")
        else:
            #if/else statements here to control what the conductor is (the calculator will be used for some of this)
            if self.conductorType == 'loop':
                #if self.conductorType == 'strip': <- decide in function 
                conPts = self.flatLoopAntenna(ax)

        if len(self.superstrateLayers) <1:
            print("No superstrate layers to draw")
        else:
            #TODO: if/else for selecting shape of substrate 
           supPts = self.flatRectangleSuperstrate(ax)

        # ax.axis([(-1.25*x_lim)+self.k,  (1.25*y_lim)+self.h,    self.k,  (1.25*y_lim)+self.h])
        self.updateCanvas(ax, units=units)

        return subPts, conPts, supPts

    def drawCurvedAntenna(self, ax, units):
        #first layer vars
        subWidth = float(self.substrateParams[0])
        self.d, self.substrateArcLength, self.mainArcRadius, self.mainArc_x, self.mainArc_y = self.calculateFirstArcParams(self.bendAngle, subWidth, self.k, self.h)

        subPts =[]
        conPts=[]
        supPts=[]

        subPEqs =[]
        supEqs=[]


        if len(self.substrateLayers) <1:
            print("No substrate layers to draw")
        else:
            #TODO: if/else for selecting shape of substrate 
            subPts, subEqs = self.curvedRectangleSubstrate(ax) 

        if len(self.conductorLayers) <1:
            print("No conductor layers to draw")
        else:
            #if/else statements here to control what the conductor is (the calculator will be used for some of this)
            if self.conductorType == 'loop':
                #if self.conductorType == 'strip': <- decide in function 
                conPts = self.curvedLoopAntenna(ax)

        if len(self.superstrateLayers) <1:
            print("No superstrate layers to draw")
        else:
            #TODO: if/else for selecting shape of superstrate 
            supPts, supEqs = self.curvedRectangleSuperstrate(ax)

        ax.axis([(-1.25*self.mainArcRadius)+self.k,  (1.25*self.mainArcRadius)+self.h,    self.k,  (1.25*self.mainArcRadius)+self.h])
        self.updateCanvas(ax, units=units)

        return subPts, conPts, supPts, subEqs

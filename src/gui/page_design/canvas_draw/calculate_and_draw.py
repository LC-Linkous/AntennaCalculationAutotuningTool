##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   './gui/page_design/geometry_calculator/calculate_and_draw.py'
#   Class for calculating coordinate points used in the GUI drawing,
#   and some of the simulation polyshape creation
#   Not all points used for drawing are saved for CAD creation
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import numpy as np

ZEROS_ARR = [0, -0, 0.0, -0.0] #cover the different ways zeros can be represented (also deals w weird user input)

class CalculateAndDraw():
    def __init__(self):
        
        # main coord arrays
        # format is [[shape1], [shape2]]. i.e: [[[x,y,z], [x,y,z], [x,y,z]], [[x,y,z],[x,y,z]]]
        self.conductorCoords = []
        self.substrateCoords = []
        self.superstrateCoords = []
        #user set vals
        self.bendAngle = None #angle of deflection for antenna-substrate contact
        self.substrateParams = [] #width,length for rectangles. radx,radx for circles/ovals
        self.substrateLayers = []
        self.conductorType = None
        self.conductorFeed = None
        self.conductorLayers = []
        self.conductorParams = None 
        self.superstrateLayers = []
        self.superstrateParams = None

        #calculated vals for CAD drawing
        self.substrateSheetEqs = [] #format [[A, min_ang, max_ang, offset]]
        self.conductorSheetEqs = []


        # flat coord array backups
        self.flatConductorCoords = []
        self.flatSubstrateCoords = []
        self.flatSuperstrateCoords = []

        #arc drawing params
        self.d = None  #deflection angle provided by user
        self.mainArcRadius = None #radius of top layer substrate arc (used as the reference radius for substrate and conductor layers)
        self.substrateArcLength = None # this applies only to curved materials
        self.N = 45  # num pts to graph in arc
        self.k = 0  # (k,h,f). offset
        self.h = 0
        self.f = 0
        self.offset = 0 #(x,y,z) for future feature options
        self.arcCenter = 0
        self.mainArc_x = []
        self.mainArc_y = []
        self.x_lim = 1
        self.y_lim = 1

    #######################################################################
    # canvas basics
    #######################################################################  
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


    #######################################################################
    # setters and getters for class vars
    #######################################################################   

    def setConductorCords(self, c):
        # used for imported DXF designs.
        # format is [[shape1], [shape2]]. i.e: [[[x,y,z], [x,y,z], [x,y,z]], [[x,y,z],[x,y,z]]]
        self.conductorCoords = c

    def getConductorCoords(self):
        return self.conductorCoords

    def setSubstrateCords(self, c):
        self.substrateCoords = c

    def getSubstrateCoords(self):
        return self.substrateCoords    
    
    def setSuperstrateCords(self, c):
        self.superstrateCoords = c

    def getSuperstrateCoords(self):
        return self.superstrateCoords    
    

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


    #######################################################################
    # main function for generating cordinates
    #
    #   calculateGeneratedDesignCoordinates()
    #       called by the design_page when the calculator/replicator options are used
    #   parseImportedConductorDesignCoordinates()
    #       used when importing the dxf design. parses conductor/substrate/values out
    #   calculateLayerDesignCoordinates()
    #       called when the layers are set. might include generated/imported 
    #   calculateBendCoordinates()
    #       takes existing coordinates and bends them to fit a 2D line
    #   
    #       ... advanced features such as substrate shape to be added
    #######################################################################

    def calculateGeneratedCoordinates(self, ax, features, params):
        # Called by the calculate/replicate button in 'page_design'
        
        aType = features["antenna_type"][0]

        xlims = [0, 10]
        ylims = [0, 10]
        zlims = [-10, 10]

        if (aType == "rectangular_patch") or (aType == "rep_rectangular_patch"):
            l,w = self.generatePatch(ax, features, params)
            # adjust limits for 3D canvas
            xlims = [0, 2.5*l]
            ylims = [0, 2.5*l]
            zlims = [-1.25*l, 1.25*l]          

        elif (aType =="half_wave_dipole") or (aType == "rep_half_wave_dipole"):
            l,a  = self.generateDipole(ax, features, params)
            # adjust limits for 3D canvas
            xlims = [-l/2, l/2]
            ylims = [-l/2, l/2]
            zlims = [-0.75*l, 0.75*l]         

        elif aType =="quarter_wave_monopole":
            l  = self.generateMonopole(ax, features, params)
            # adjust limits for 3D canvas
            xlims = [-l/2, l/2]
            ylims = [-l/2, l/2]
            zlims = [0, 1.25*l]     

        elif aType =="rep_E":
            l,w  = self.generateMicrostripE(ax, features, params)
            xlims = [0,l]
            ylims = [0, w]
            zlims = [-.5*l, .5*l]   

        elif aType =="rep_slotted_r_patch":
            l, w  = self.generateSlottedPatch(ax,features, params)
            xlims = [0,w]
            ylims = [0, w]
            zlims = [-.25*l, .25*l]  
                
        elif aType =="rep_db_serpentine":
            l,w  = self.generateDualBandSerpentine(ax, features, params)
            xlims = [-0.5*w, 0.5*w]
            ylims = [-0.5*w, 0.5*w]
            zlims = [-.25*l, .25*l]  

        elif aType =="rep_circular_loop":
            l,w  = self.generateCircularLoop(ax, features, params)
            xlims = [-l, l]
            ylims = [-l, l]
            zlims = [-1.25*l, 1.25*l]

        else:
            print("unrecognized antenna type in graphics helper funcs: " + str(aType))


        #adjust limits for 3D canvas
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        ax.set_zlim(zlims)
        
        ax.set_xlabel('x_size (mm)')
        ax.set_ylabel('y_size (mm)')
        ax.set_zlabel('z_size (mm)')


    def parseImportedConductorDesignCoordinates(self, ax, shapeVector):
        #unlike other features in AntennaCAT, this only pulls in the shape vector from the custom conductor panel
        # this shape can be applied to many other features.
        # eventually, there will be a 'parse coords' function that will write the conductor cords to memory to be applied to other
        # configurations without needing to be recalcuated
        print("parsing imported conductor pts in calculate_and_draw")


        pass


    def calculateLayerDesignCoordinates(self, features, params):
        pass


    def calculateBendCoordinates(self, features, params):
        pass


    #######################################################################
    # primary functions for drawing generated designs
    #   these generate the coordinates for the FLAT version of the generated
    #   designs from the design page
    #######################################################################

    def generatePatch(self, ax, features, params):
        aType = features["antenna_type"][0]
        feed = features["feed_type"][0]
        h = float(features["substrate_height"][0]) 
        w = float(params["width"][0])
        l = float(params["length"][0])    
        x0 = float(params["x0"][0])
        y0 = float(params["y0"][0])

        #draw ground plane rectangle
        pts = self.drawRectangularPlane(ax, 2*l, 2*w, z=0, color="goldenrod") # groundplane
        self.substrateCoords.append(pts)

        #draw top of patch
        if feed == "microstrip":
            sw = float(params["strip_width"][0])
            g = float(params["gap"][0])
            self.draw2DMicrostripConductor(ax, l, w, h, x0, sw, g, color="orange")
        elif feed =="probe":
            pts = self.drawRectangularPlane(ax, 2*l, 2*w, z=h, corner=[0,0], color="orange")
            self.substrateCoords.append(pts)
            pts = self.drawRectangularPlane(ax, l, w, z=h, corner=[w/2,l/2], color="orange")
            self.conductorCoords.append(pts)
            pts = self.drawCircularPoint(ax, w/2+y0, 1.5*l-x0, h, color="orange")
            self.conductorCoords.append(pts)
        else:
            print("unrecognized feed type for rectangular_patch")
        return l, w


    def generateMonopole(self, ax, features, params, color = "b"):
        aType = features["antenna_type"][0]
        l = float(params["length"][0])    
        rad = float(params["radius"][0])    

        self.drawCylinder(ax, rad, start=0, stop=l, center=[0,0], color=color)

        return l #return val to size the canvas

    def generateDipole(self, ax, features, params, color = "m"):
        aType = features["antenna_type"][0]
        l = float(params["length"][0]) 
        hl = float(params["half_length"][0])    
        rad = float(params["radius"][0])    
        fg = float(params["feed_gap"][0])    

        #draw cylinder x2
        self.drawCylinder(ax, rad, start=(fg/2), stop=(hl+fg/2), center=[0,0], color=color)
        self.drawCylinder(ax, rad, start=(-hl-fg/2), stop=-fg/2, center=[0,0], color=color)

        return l, rad #return val to size the canvas


    def generateMicrostripE(self, ax, features, params, corner=[0,0], color="g"):
        x = float(params["X"][0]) 
        l = float(params["L"][0])    
        ls = float(params["Ls"][0])    
        lg = float(params["Lg"][0])   
        ps = float(params["Ps"][0]) 
        ws = float(params["Ws"][0])    
        w = float(params["W"][0])    
        wg = float(params["Wg"][0])   
        h = float(params["h"][0])
        self.draw2DMicrostripEConductor(ax, x, l, ls, lg, ps, ws, w, wg, h, corner=[0,0], color=color)

        return lg, wg #return val to size the canvas


    def generateSlottedPatch(self, ax, features, params, corner=[0,0], color="indigo"):
        lr = float(params["Lr"][0]) 
        lh = float(params["Lh"][0])    
        lv = float(params["Lv"][0])    
        l = float(params["L"][0])   
        lg = float(params["Lg"][0]) 
        pr = float(params["Pr"][0]) 
        wr = float(params["Wr"][0])    
        wu = float(params["Wu"][0])    
        w = float(params["W"][0])   
        wg = float(params["Wg"][0])
        fx = float(params["fx"][0])    
        fy = float(params["fy"][0])    
        d = float(params["d"][0])   
        self.draw2DSlottedPatchConductor(ax, lr, lh, lv, l, lg, pr, wr, wu, w, wg, fx, fy, d, corner=[0,0], color=color)

        return lg, wg #return val to size the canvas

    def generateDualBandSerpentine(self, ax, features, params, corner=[0,0], color="b"):
        lp = float(params["Lp"][0]) 
        lsub = float(params["Lsub"][0])    
        wp = float(params["Wp"][0])  
        wsub = float(params["Wsub"][0])    
        ps1 = float(params["Ps1"][0])   
        ls1 = float(params["Ls1"][0]) 
        ws1 = float(params["Ws1"][0])    
        ps2 = float(params["Ps2"][0])   
        ls2 = float(params["Ls2"][0]) 
        ws2 = float(params["Ws2"][0])    
        ps3 = float(params["Ps3"][0])   
        ls3 = float(params["Ls3"][0]) 
        ws3 = float(params["Ws3"][0])    
        ps4 = float(params["Ps4"][0])   
        ls4 = float(params["Ls4"][0]) 
        ws4 = float(params["Ws4"][0])    
        lc = float(params["Lc"][0]) 
        fy = float(params["Fy"][0])    
        px = float(params["Px"][0])   
        py = float(params["Py"][0]) 
        d = float(params["d"][0]) 

        self.draw2DDualBandSerpentinePatchConductor(ax, lp, lsub, wp, wsub,
                                                    ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4,
                                                    lc, fy, px, py, d, corner=[0,0], color=color)

        return lsub, wsub #return val to size the canvas

    def generateCircularLoop(self, ax, features, params, corner=[0,0], color="b"):
        outerRad = float(params["outer_radius"][0]) 
        innerRad = float(params["inner_radius"][0])    
        feedWidth = float(params["feed_width"][0])  
        inset = float(params["inset"][0])    
        gapDist = float(params["gap_distance"][0])   
        h = float(features["substrate_height"][0]) 

        self.draw2DCircularLoopConductor(ax, outerRad, innerRad, feedWidth, inset, gapDist, h, corner=[0,0], color=color)

        return (feedWidth+2*outerRad), (feedWidth+2*outerRad) #return val to size the canvas


    #######################################################################
    # Functions for drawing rectangular patch antenna conductors
    #######################################################################

    def draw2DMicrostripConductor(self, ax,  l, w, h, x0, ws, g, corner=[0,0], color="g"):
        #substrate edges
        substratePts = self.rectangle(corner, 2*w, 2*l, h)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        #conductor
        conductorPts = self.rectangularPatchConductor(l, w, h, x0, ws, g)
        x,y,z = self.XYZptsSplit(conductorPts)
        ax.plot(x, y, z, color=color)

        #append points to memory
        self.substrateCoords.append(substratePts)
        self.conductorCoords.append(conductorPts)


    def draw3DStriplineConductor(self, ax, l, w, h, x0, ws, color="g"):
        #version for when conductor has a thickness
        pass

    def rectangularPatchConductor(self, L, W, h, x0, Ws, g):
        #2D coordinates for drawing the patch antenna conductor
        #modified from antenna calculator
        substrate_origin = 0.0
        originW = -(substrate_origin - W*0.5)
        originL = -(substrate_origin - L*0.5) #keep
        W_cut = (W - Ws - g * 2) / 2
        points = [[originW, originL, h], [originW + W, originL, h], [originW + W, originL + L, h],
                [(originW + W_cut + Ws + g * 2), originL + L, h],
                [originW + W_cut + Ws + g * 2, originL + L - x0, h],
                [originW + W_cut + Ws + g, originL + L - x0, h],
                [originW + W_cut + Ws + g, originL + L * 1.5, h],
                [originW + W_cut + g, originL + L * 1.5, h],
                [originW + W_cut + g, originL + L - x0, h],
                [originW + W_cut, originL + L - x0, h],
                [originW + W_cut, originL + L, h],
                [originW, originL + L, h],
                [originW, originL, h]]
        return points

    #######################################################################
    # Functions for drawing the microstrip E
    #######################################################################

    def draw2DMicrostripEConductor(self, ax, xfeed, l, ls, lg, ps, ws, w, wg, h, corner=[0,0], color="g"):
        #ground plane
        substratePts = self.rectangle(corner, wg, lg, 0)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        #conductor
        conductorPts = self.EConductor(x, l, ls, lg, ps, ws, w, wg, h)
        x,y,z = self.XYZptsSplit(conductorPts)
        ax.plot(x, y, z, color=color)
        #pin
        self.drawCylinder(ax, a=.3, start=0, stop=h, center=[wg/2,(lg/2)-xfeed], color="orange")

        #append points to memory
        self.substrateCoords.append(substratePts)
        self.conductorCoords.append(conductorPts)

    def EConductor(self, x, l, ls, lg, ps, ws, w, wg, h):
        #2D coordinates for drawing the microstrip fed E conductor
        outerBranchWidth = w/2-ps-(ws/2)
        innerBranchWidth = 2*ps-ws
        originW = (wg/2)-(w/2) #dealing with offset
        originL = (lg/2)-(l/2) #dealing with offset
        points = [[originW, originL, h], [originW, originL+l, h], 
                  [originW + w, originL + l, h], [originW + w, originL, h],
                  [originW+w-outerBranchWidth, originL, h],
                  [originW+w-outerBranchWidth, originL+ls, h],
                  [originW+w-outerBranchWidth-ws, originL+ls, h],
                  [originW+w-outerBranchWidth-ws, originL, h],
                  [originW+outerBranchWidth+ws, originL, h],
                  [originW+outerBranchWidth+ws, originL+ls, h],
                  [originW+outerBranchWidth, originL+ls, h],
                  [originW+outerBranchWidth, originL, h],
                  [originW, originL, h] ]

        return points


    #######################################################################
    # Functions for drawing the slotted patch
    #######################################################################

    def draw2DSlottedPatchConductor(self, ax, lr, lh, lv, l, lg, pr, wr, wu, w, wg, fx, fy, h, corner=[0,0], color="indigo"):
        #ground plane
        substratePts = self.rectangle(corner, wg, lg, 0)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        #conductor
        substratePts = self.rectangle(corner, wg, lg, h)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        conductorPts = self.slottedPatchConductor(lr, lh, lv, l, lg, pr, wr, wu, w, wg, fx, fy, h)
        x,y,z = self.XYZptsSplit(conductorPts)
        ax.plot(x, y, z, color=color)
        #pin
        pts = self.drawCircularPoint(ax, (wg/2)-(w/2)+(w/2)+fx, (lg/2)-(l/2)+fy, h, color=color)
        self.conductorCoords.append(pts)

        #append points to memory
        self.substrateCoords.append(substratePts)
        self.conductorCoords.append(conductorPts)

    def slottedPatchConductor(self, lr, lh, lv, l, lg, pr, wr, wu, w, wg, fx, fy, h):
        #2D coordinates for drawing the slotted patch antenna conductor
        originW = (wg/2)-(w/2) #dealing with offset
        originL = (lg/2)-(l/2) #dealing with offset

        points = [[originW, originL, h], [originW, originL+l, h], 
                  [originW + w, originL + l, h],
                  [originW + w, originL + l/2 + pr + (wr/2), h], 
                  [originW + w - lr, originL + l/2 + pr + (wr/2), h],
                  [originW + w - lr, originL + l/2 + pr-(wr/2), h],
                  [originW + w, originL + l/2 + pr-(wr/2), h],
                  [originW + w, originL, h],
                  [originW + w/2 - lh/2 + wu, originL, h],
                  [originW + w/2 - lh/2 + wu, originL + lv - wu, h], #
                  [originW + w/2 + lh/2, originL + lv - wu, h],
                  [originW + w/2 + lh/2, originL + lv, h],
                  [originW + w/2 - lh/2, originL + lv, h],
                  [originW + w/2 - lh/2, originL, h],
                  [originW, originL, h] ]

        return points



    #######################################################################
    # Functions for drawing the serpentine patch
    #######################################################################

    def draw2DDualBandSerpentinePatchConductor(self, ax, lp, lsub, wp, wsub,
                                                    ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4,
                                                    lc, fy, px, py, d, corner=[0,0], color="darkblue"):
        #ground plane
        substratePts = self.rectangle([-wsub/2, -lsub/2], wsub, lsub, 0)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        #conductor
        substratePts = self.rectangle([-wsub/2, -lsub/2], wsub, lsub, d)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        conductorPts = self.DBSerpentinePatchConductor(lp, lsub, wp, wsub,
                                                    ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4,
                                                    lc, fy, px, py, d)
        x,y,z = self.XYZptsSplit(conductorPts)
        ax.plot(x, y, z, color=color)

        # shorting pin
        pts = self.drawCircularPoint(ax, ps3-(ws3/2)-px, -10.75+lp-py, d, color=color)
        self.conductorCoords.append(pts)

        # feed pin
        fx = ((ps4-(ws4/2))+(ps3+(ws3/2)))/2
        pts = self.drawCircularPoint(ax, fx, fy, d, color=color) #edit to x strip center
        self.conductorCoords.append(pts)


    def DBSerpentinePatchConductor(self, lp, lsub, wp, wsub,
                                                    ps1, ls1, ws1, ps2, ls2, ws2, ps3, ls3, ws3, ps4, ls4, ws4,
                                                    lc, fy, px, py, d):
        #2D coordinates for drawing the slotted patch antenna conductor
        originW = -10.75 # from paper
        originL = -11 # from paper

        points = [[originW, originL, d], [originW, originL + lp, d],
                  [ps1 - ws1/2, originL + lp, d], 
                  [ps1 - ws1/2, originL + lp - ls1, d],  
                  [ps1 + ws1/2, originL + lp - ls1, d],
                  [ps1 + ws1/2, originL + lp, d],  

                  [ps3 - ws3/2, originL + lp, d], 
                  [ps3 - ws3/2, originL + lp - ls3, d],  
                  [ps3 + ws3/2, originL + lp - ls3, d],
                  [ps3 + ws3/2, originL + lp, d], 

                  [originW + wp, originL + lp, d], 
                  [originW + wp, originL + lp - lc, d], 

                  [ps4 + ws4/2, originL + lp - lc, d], 
                  [ps4 + ws4/2, originL + ls4, d], 
                  [ps4 - ws4/2, originL + ls4, d], 
                  [ps4 - ws4/2, originL, d],

                  [ps2 + ws2/2, originL, d],                   
                  [ps2 + ws2/2, originL + ls2, d], 
                  [ps2 - ws2/2, originL + ls2, d], 
                  [ps2 - ws2/2, originL, d], 
                  [originW, originL, d]]                  

        return points

    #######################################################################
    # Functions for drawing the circular loop
    #######################################################################

    def draw2DCircularLoopConductor(self, ax, outerRad, innerRad, feedWidth, inset, gapDist, h, corner=[0,0], color="g"):
        #ground plane
        gpLength= 1.25*(inset+2*outerRad) 
        substratePts = self.rectangle([-gpLength/2, -gpLength/2], gpLength, gpLength, 0)
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        #conductor
        substratePts = self.rectangle([-gpLength/2, -gpLength/2], gpLength, gpLength, h)#counding rectangle
        x,y,z = self.XYZptsSplit(substratePts)
        ax.plot(x,y,z, color=color)
        conductorPts = self.circularLoopConductor(outerRad, innerRad, feedWidth, inset, gapDist, h)
        x,y,z = self.XYZptsSplit(conductorPts)
        ax.plot(x, y, z, color=color)


    def circularLoopConductor(self, outerRad, innerRad, feedWidth, inset, gapDist, h):
        #2D coordinates for drawing the slotted patch antenna conductor
        originW = 0
        originL = 0

        points = []


        # #draw striplines 
        # r_strip_x = np.linspace((-gapDist/2), (-gapDist/2 - feedWidth), self.N)  
        # l_strip_x = np.linspace((gapDist/2 + feedWidth), (gapDist/2), self.N)                   

        # pts_z_min = np.zeros(self.N)
        # #looking down on to the XZ plane, draw an arc with an opening of the gap distance
        # #looking from the XY plane, this shape should look like an arc flush with the substrate/layers below it

        # r_feed_x = feedRight[0][::-1]
        # r_feed_y = feedRight[1][::-1]

        # l_feed_x = feedLeft[0][::-1]
        # l_feed_y = feedLeft[1][::-1]

        # inner_inset  = inset + (outerRad-innerRad)

        # #running pts - add arc of left feed
        # pts_x = l_feed_x
        # pts_y = l_feed_y
        # pts_z = pts_z_min

        # #loop features
        # o_x, o_y, o_z = self.calcLoopAndArc(outLoopRad, gapDist, feedWidth, inset,  useFeedOffset=True, numPts=int(bendRad*25))##outer loop 
        # i_x, i_y, i_z = self.calcLoopAndArc(inLoopRad, gapDist, feedWidth, inner_inset,  bendRad=bendRad, layerOffset=layerOffset, numPts=int(bendRad*25))##inner loop
        # #draw a star at the start of the arc - used to check for rotation offset
        # # ax.plot(o_x[0], o_y[0], o_z[0],'y*')

        # #running pts - add jump from arc to outer loop, on the outside (not-gap) side of left strip
        # pts_x = np.concatenate((pts_x, o_x), axis=None)
        # pts_y = np.concatenate((pts_y, o_y), axis=None)
        # pts_z = np.concatenate((pts_z, o_z), axis=None)

        # # #running pts - add jump from outer loop to arc, on the outside (not-gap) side of right strip
        # pts_x = np.concatenate((pts_x, r_feed_x), axis=None)
        # pts_y = np.concatenate((pts_y, r_feed_y), axis=None)
        # pts_z = np.concatenate((pts_z, pts_z_min), axis=None)

        # #running pts - add jump from arc to inner loop, on the gap side of right strip
        # pts_x = np.concatenate((pts_x, i_x[::-1]), axis=None)
        # pts_y = np.concatenate((pts_y, i_y[::-1]), axis=None)
        # pts_z = np.concatenate((pts_z, i_z[::-1]), axis=None)

        # #running pts - add jump from inner loop to arc of the left feed, on the gap side of right strip
        # pts_x = np.concatenate((pts_x, l_feed_x[0]), axis=None)
        # pts_y = np.concatenate((pts_y, l_feed_y[0]), axis=None)
        # pts_z = np.concatenate((pts_z, pts_z_min[0]), axis=None)

        # #zip the x,y,z pts together
        # zipped_pts = list(zip(pts_x, pts_y, pts_z))
        # return zipped_pts

        
        # spline_pts.append(zp)

        return points



    #######################################################################
    # Functions for drawing planes
    #######################################################################
    def drawRectangularPlane(self, ax, length, width, z, corner=[0,0], color ="b"):
        pts = self.rectangle(corner, width, length, z)
        x,y,z = self.XYZptsSplit(pts)
        ax.plot(x,y,z, color=color)
        return pts


    def drawOvalPlane(self, length, width, z, color ="b"):
        pass

    def drawCustomPlane(self, pts, z, color="b"):
        pass


    #######################################################################
    # Functions for drawing 3D shapes
    #######################################################################

    def drawCylinder(self, ax, a, start, stop, center=[0,0], color="b"):
        x = center[0]
        y = center[1]
        z = np.linspace(start, stop, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        thetaMat, zMat=np.meshgrid(theta, z)
        xMat = x + a*np.cos(thetaMat)
        yMat = y + a*np.sin(thetaMat)
        ax.plot_surface(xMat, yMat, zMat, alpha=0.75, color=color)

        # zip cords
        pts = zip(xMat, yMat, zMat)
        return pts

    def drawFlatRectangle3DLayer(self, ax, width, length, depth, centerFrontPt, color="b"):        
        w = width
        l = length
        c_x = centerFrontPt[0]
        c_y = centerFrontPt[1] #depth_ctr
        c_z = centerFrontPt[2]
                
        #corner points, clockwise from front left + one to close shape
        #top
        u1 = [c_x-w/2, c_y, c_z+0] #front left
        u2 = [c_x-w/2, c_y, c_z+l]
        u3 = [c_x+w/2, c_y, c_z+l]
        u4 = [c_x+w/2, c_y, c_z+0] #front right
        upper_face_pts = np.array([u1, u2, u3, u4, u1])
        ax.plot(upper_face_pts[:,0], upper_face_pts[:,1] ,upper_face_pts[:,2], color=color)
        #bottom
        l1 = [c_x-w/2, c_y+depth, c_z+0]
        l2 = [c_x-w/2, c_y+depth, c_z+l]
        l3 = [c_x+w/2, c_y+depth, c_z+l]
        l4 = [c_x+w/2, c_y+depth, c_z+0]
        lower_face_pts = np.array([l1, l2, l3, l4, l1])
        ax.plot(lower_face_pts[:,0], lower_face_pts[:,1], lower_face_pts[:,2], color=color)

        #edges
        self.drawConnectingEdge(ax, color, [[u1, l1], [u2, l2], [u3, l3], [u4, l4]])

        return upper_face_pts  #this is the layer that will be extruded (downwards) in the CAD 

    def drawCurvedRectangle3DLayer(self, ax, color, upper_x, upper_y, lower_x, lower_y, min_z, max_z):
        max_z = float(max_z)
        #outer arc coords, inner arc cords
        pts_x = []
        pts_y = []
        #merge outer arc and reverse order of inner arc to draw with one line
        pts_x = np.concatenate((upper_x, lower_x[::-1]), axis=None)
        pts_y = np.concatenate((upper_y, lower_y[::-1]), axis=None)
        #add last point to close polygon
        pts_x = np.append(pts_x, pts_x[0])
        pts_y = np.append(pts_y, pts_y[0])
        n = len(pts_x)
        pts_z_min = np.ones(n)*min_z #to scale to whatever the min value is
        ax.plot(pts_x, pts_y, pts_z_min, color=color) #graph end of shape at z=0 (or min_z)
        pts_z_max = np.ones(n)*max_z #to scale to whatever the min value is. if max_z values are different, this will have a slant
        ax.plot(pts_x, pts_y, pts_z_max, color=color) #graph end of shape at z=max_z

        self.drawConnectingEdge(ax, color, [[[upper_x[0], upper_y[0], min_z],[upper_x[0], upper_y[0], max_z]],
                                        [[lower_x[0], lower_y[0], min_z],[lower_x[0], lower_y[0], max_z]],
                                        [[upper_x[-1], upper_y[-1], min_z],[upper_x[-1], upper_y[-1], max_z]], 
                                        [[lower_x[-1], lower_y[-1], min_z],[lower_x[-1], lower_y[-1], max_z]]])
        

        zipped_pts = list(zip(pts_x, pts_y, pts_z_min))
        return zipped_pts

    #######################################################################
    # Functions for bending 2D shapes
    #######################################################################



    def drawCurvedAntenna(self):
        #use a toggle to get this or the flat version
        #TODO: add funcitonality for drawing on curved substrates

        pass

    def drawCurvedSubstrate(self, ax, features, params):
        pass



    #######################################################################
    # Basic Shape Functions with x,y,z pts
    #######################################################################
    def drawCircularPoint(self, ax, x, y, z, color ="b"):
        ax.plot(x, y, z, 'o', color=color, linewidth=0.2)

    def rectangle(self, c, w, h, z):
        x = c[0]
        y = c[1]
        return [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]]

    def rectangleByCenter(self,c, w, h, z):
        x = c[0]
        y = c[1]
        return [[x-0.5*w, y-0.5*h, z], [x +0.5*w, y-0.5*h, z], [x+0.5*w, y+0.5*h, z], [x-0.5*w, y+0.5*h,z]]

    def circleByCenter(self,c, w, h, z):
        x = c[0]
        y = c[1]
        return [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]]

    def triangle(self,c, w, h, z):
        x = c[0]
        y = c[1]
        return [[x,y,z],[(x - 0.5*w),(y + h),z], [(x + 0.5*w),(y + h),z]]

    def arc(self,c, pc, pt, theta):
        pass



    def nSidedPolygonPts(self,x, y, z, r, n, buf=0):
        # calculate and return points for a n sided figure that will encompass a circle at x,y with radius r with buffer
        # set buf == 0 to draw exactly on the circle
        rad = r + buf
        pts = []
        for i in range(0, n):
            t = 2 * np.pi * i / n
            x1 = (int)(x + rad * np.cos(t))
            y1 = (int)(y + rad * np.sin(t))
            pts.append([x1, y1, z])
        return pts


    #######################################################################
    # Basic Shape Functions
    #######################################################################

    def XYZptsSplit(self,pts):
        x = []
        y = []
        z = []
        ctr = 0
        for i in pts:
            ctr = ctr + 1
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])
        # close figure if needed
        if ctr > 2:
            x.append(x[0])
            y.append(y[0])
            z.append(z[0])
        return x, y, z

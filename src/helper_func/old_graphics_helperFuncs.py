##--------------------------------------------------------------------\
#   Antenna Calculation Autotuning Tool
#   'helper_func/graphics_helperFuncs.py'
#   Helper functions for 3D display of antennas and generic graph needs
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import numpy as np


#TODO:
# when moving to the DRAW ANTENNA CLASS - make a function for returning vars from DF
# so that if names change it's not difficult to rename vars


#######################################################################
# Functions for drawing select antenna designs
#######################################################################
def drawAntenna(ax, features, params, substrateColor="b", conductorColor="y"):
    
    aType = features["antenna_type"][0]

    if (aType == "rectangular_patch") or (aType == "rep_rectangular_patch"):
        l = drawPatch(ax, features, params, substrateColor, conductorColor)

    elif aType =="elliptical_patch":
        l = drawMonopole(ax, features, params, conductorColor)
        
    elif (aType =="half_wave_dipole") or (aType == "rep_half_wave_dipole"):
        l = drawMonopole(ax, features, params, conductorColor)

    elif aType =="quarter_wave_monopole":
        l = drawDipole(ax, features, params, conductorColor)

    elif aType =="rep_E":
        print("the E design has not been added to the graphics library in graphics_helperFuncs yet")

    else:
        print("unrecognized antenna type in graphics helper funcs")

    #adjust limits for 3D canvas
    ax.set_xlim(0, 2.5*l)
    ax.set_ylim(0, 2.5*l)
    ax.set_zlim(-1.25*l, 1.25*l)

    
    ax.set_xlabel('x_size (mm)')
    ax.set_ylabel('y_size (mm)')
    ax.set_zlabel('z_size (mm)')


def drawCurvedAntenna():
    #use a toggle to get this or the flat version
    #TODO: add funcitonality for drawing on curved substrates

    pass

def drawCurvedSubstrate(ax, features, params):
    pass



def drawPatch(ax, features, params, substrateColor="b", conductorColor="y"):
    aType = features["antenna_type"][0]
    feed = features["feed_type"][0]
    h = float(features["substrate_height"][0]) 
    w = float(params["width"][0])
    l = float(params["length"][0])    
    x0 = float(params["x0"][0])
    y0 = float(params["y0"][0])
    sw = float(params["strip_width"][0])

  
    drawRectangularPlane(ax, 2*l, 2*w, z=0, color="goldenrod") # groundplane
    if feed == "microstrip":
        draw2DStriplineConductor(ax, l, w, h, x0, sw, color="orange")
    elif feed =="probe":
        drawRectangularPlane(ax, 2*l, 2*w, z=h, center=[0,0], color="orange")
        drawRectangularPlane(ax, l, w, z=h, center=[w/2,l/2], color="orange")
        drawCircularPoint(ax, l+x0, w-y0, h, color="orange")
    else:
        print("unrecognized feed type for rectangular_patch")
    
    return l #return val to size the canvas


def drawMonopole(ax, features, params, conductorColor):
    aType = features["antenna_type"][0]
    feed = features["feed_type"][0]
    h = float(features["substrate_height"][0]) 
    w = float(params["width"][0])
    l = float(params["length"][0])    
    x0 = float(params["x0"][0])
    y0 = float(params["y0"][0])
    sw = float(params["strip_width"][0])


    #draw cyl x2

    return l #return val to size the canvas

def drawDipole(ax, features, params, conductorColor):
    aType = features["antenna_type"][0]
    feed = features["feed_type"][0]
    h = float(features["substrate_height"][0]) 
    w = float(params["width"][0])
    l = float(params["length"][0])    
    x0 = float(params["x0"][0])
    y0 = float(params["y0"][0])
    sw = float(params["strip_width"][0])


    #draw groundplane
    #draw cylinder

    return l #return val to size the canvas
                
#######################################################################
# Functions for drawing planes
#######################################################################
def drawRectangularPlane(ax, length, width, z, center=[0,0], color ="b"):
    pts = rectangle(center, width, length, z)
    x,y,z = XYZptsSplit(pts)
    ax.plot(x,y,z, color=color)


def drawOvalPlane(length, width, z, color ="b"):
    pass

def drawCustomPlane(pts, z, color="b"):
    pass

#######################################################################
# Functions for drawing 3D shapes
#######################################################################

def drawCylinder(ax, a, start, stop, color="b"):
    z = np.linspace(start, stop, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    thetaMat, zMat=np.meshgrid(theta, z)
    xMat = a*np.cos(thetaMat)
    yMat = a*np.sin(thetaMat)
    ax.plot_surface(xMat, yMat, zMat, alpha=0.5)

def drawRectangularBox(ax, a, l, color="b"):
    pass


#######################################################################
# Functions for drawing rectangular patch antenna conductors
#######################################################################

def draw2DStriplineConductor(ax, l, w, h, x0, ws, color="g", c=[0,0]):
    #substrate edges
    subpts = rectangle(c, 2*w, 2*l, h)
    x,y,z = XYZptsSplit(subpts)
    ax.plot(x,y,z, color=color)
    #conductor
    pts = rectangularPatchConductor(l, w, h, x0, ws)
    x,y,z = XYZptsSplit(pts)
    ax.plot(x, y, z, color=color)

def draw3DStriplineConductor(ax, l, w, h, x0, ws, color="g"):
    #version for when conductor has a thickness
    pass

def rectangularPatchConductor(L,W,h,x0,Ws):
    #2D coordinates for drawing the patch antenna conductor
    #modified from antenna calculator
    substrate_origin = 0.0
    originW = -(substrate_origin - W*0.5)
    originL = -(substrate_origin - L*0.5) #keep
    g = Ws / 3
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
# Basic Shape Functions with x,y,z pts
#######################################################################
def drawCircularPoint(ax, x, y, z, color ="b"):
    ax.plot(x, y, z, 'o', color=color, linewidth=0.2)

def rectangle(c, w, h, z):
    x = c[0]
    y = c[1]
    return [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]]

def rectangleByCenter(c, w, h, z):
    x = c[0]
    y = c[1]
    return [[x-0.5*w, y-0.5*h, z], [x +0.5*w, y-0.5*h, z], [x+0.5*w, y+0.5*h, z], [x-0.5*w, y+0.5*h,z]]

def circleByCenter(c, w, h, z):
    x = c[0]
    y = c[1]
    return [[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z]]

def triangle(c, w, h, z):
    x = c[0]
    y = c[1]
    return [[x,y,z],[(x - 0.5*w),(y + h),z], [(x + 0.5*w),(y + h),z]]

def arc(c, pc, pt, theta):
    pass



def nSidedPolygonPts(x, y, z, r, n, buf=0):
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

def XYZptsSplit(pts):
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


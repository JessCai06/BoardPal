from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.baseSquare = [(-1,-1, 0),(1,1, 0),(-1,1, 0),(1,-1, 0)]
    app.camTheta = 270
    app.r = 2
    app.graphCenter = (0,0)
    
# the cx, cy is the center of the graph
def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r*math.cos(math.radians(theta)),
            cy - r*math.sin(math.radians(theta)))

def drawCameraNavigator(app):
    box_size = 100
    drawRect(app.width - box_size - 10, 10, box_size, box_size, opacity = 10)
    circle_radius = box_size/2
    drawCircle(app.width - box_size - 10 + circle_radius, 10+circle_radius, circle_radius, opacity = 10)
    camera_location = getRadiusEndpoint(app.width - box_size - 10 + circle_radius, 10+circle_radius,circle_radius, app.camTheta)
    drawCircle(*(camera_location),3)
    drawLine(app.width - box_size - 10, 10+circle_radius,app.width -10, 10+circle_radius)
    drawLine(app.width - box_size - 10+circle_radius, 10,app.width - box_size - 10+circle_radius, 10+box_size)


def redrawAll(app):
    drawCameraNavigator(app)
    # Draws an circle centered at (200, 150) with radius 50
    margin_bottom = int(app.width/20)
    margin_top = margin_bottom + 3*margin_bottom
    drawPolygon(app.width - margin_top, int(app.height/2), margin_top, int(app.height/2), margin_bottom, int(app.height*3/4),app.width - margin_bottom, int(app.height*3/4), fill = "gray",opacity = 50)

def onKeyHold (app,key):
    if "right" in key:
        app.camTheta += 2
    elif "left" in key:
        app.camTheta -= 2

def main():
    runApp()

main()

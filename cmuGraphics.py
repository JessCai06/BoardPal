from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
import math
import random

def onAppStart(app):
    app.camTheta = (0, 0, 0)
    app.r = 50
    app.center = (0,0,0)

    baseSquare = [(-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0), 
                  # 4           5           6           7
                  (-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1)]
    order = [[0,1,2,3],
             [0,1,5,4],
             [2,3,7,6],
             [0,3,7,4],
             [1,2,6,5],
             [4,5,6,7]]
    print(app.center)
    app.cube = ShapeObject(app.center, baseSquare, order)
    for face in app.cube.faces:
        print(face.getEdges())

# Helper methods
def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r * math.cos(math.radians(theta)),
            cy - r * math.sin(math.radians(theta)))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def transformToViewport(app, point):
    thetaX, thetaY, thetaZ = app.camTheta  # Unpack rotation angles
    x, y, z = point

    rotated_x = x * math.cos(math.radians(thetaZ)) - y * math.sin(math.radians(thetaZ))
    rotated_y = x * math.sin(math.radians(thetaZ)) + y * math.cos(math.radians(thetaZ))

    # Apply y-axis rotation
    rotated_x = rotated_x * math.cos(math.radians(thetaY)) + z * math.sin(math.radians(thetaY))
    rotated_z = -rotated_x * math.sin(math.radians(thetaY)) + z * math.cos(math.radians(thetaY))

    # Apply x-axis rotation
    final_x = rotated_x * math.cos(math.radians(thetaX)) - rotated_y * math.sin(math.radians(thetaX))
    final_y = rotated_x * math.sin(math.radians(thetaX)) + rotated_y * math.cos(math.radians(thetaX))

    # Translate to the center of the screen for viewport
    viewport_x = app.width/2 + final_x * app.r  # Scaling for visibility
    viewport_y = app.height/2 + final_y * app.r
    return (viewport_x, viewport_y)


def redrawAll(app):
    #draw points
    for point in app.cube.points:
        viewport_point = transformToViewport(app, point)
        drawCircle(viewport_point[0], viewport_point[1], 5, fill="red")
    #draw lines
    for face in app.cube.faces:
        for edge in face.getEdgePoints():
            print ("line" , edge)

def onKeyHold(app, key):
    thetaX, thetaY, thetaZ = app.camTheta  
    if "right" in key:
        app.camTheta = (thetaX + 2, thetaY, thetaZ)
    elif "left" in key:
        app.camTheta = (thetaX - 2, thetaY, thetaZ)
    elif "up" in key:
        app.camTheta = (thetaX, (thetaY + 2) % 360, thetaZ)
    elif "down" in key:
        app.camTheta = (thetaX, (thetaY - 2) % 360, thetaZ)
    elif "w" in key:
        app.camTheta = (thetaX, thetaY, (thetaZ + 2) % 360)
    elif "s" in key:
        app.camTheta = (thetaX, thetaY, (thetaZ - 2) % 360)

    if "+" in key or "=" in key:
        app.r += 10
    elif "-" in key or "_" in key:
        app.r -= 10

def main():
    runApp(width=400, height=400)

main()

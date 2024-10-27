from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
import math

def onAppStart(app):

    app.editorMode = False
    app.selectedDotIndex = 0
    app.camTheta = (0, 0, 0)
    app.graphCenter = (0,0)
    app.r = 120
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    baseSquare = [(-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0), 
                  # 4           5           6           7
                  (-1, -1, 2), (-1, 1, 2), (1, 1, 2), (1, -1, 2)]
    order = [[0,1,2,3],
             [0,1,5,4],
             [2,3,7,6],
             [0,3,7,4],
             [1,2,6,5],
             [4,5,6,7]]
    app.cube = ShapeObject((0,0,0), baseSquare, order)
    app.viewport_point_List = []
    updateViewport(app)

def updateViewport(app):
    app.viewport_point_List = []
    for i in range(len(app.cube.points)):
        point = app.cube.points[i]
        viewport_point = transformToViewport(app, point)
        app.viewport_point_List.append(viewport_point)

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def onMousePress(app, mouseX, mouseY):
    cx,cy = app.viewport_point_List[app.selectedDotIndex]
    print(cx, cy)
    if distance(mouseX,mouseY,cx,cy) > 5:
        for i in range(len(app.viewport_point_List)):
            (x,y) = app.viewport_point_List[i]
            if distance(mouseX,mouseY,x,y) < 5:
                app.selectedDotIndex = i
        (x,y) = app.viewport_point_List[app.selectedDotIndex]

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
    viewport_x = app.viewportCenter[0] + final_x * app.r  # Scaling for visibility
    viewport_y = app.viewportCenter[1] + final_y * app.r
    return (viewport_x, viewport_y)

def drawEditor(app):
    drawRect(app.width-app.editorWidth,0,app.editorWidth,app.height,fill="powderBlue",opacity=80)
    drawLabel("Editor", app.width-app.editorWidth + 100+ 20, 20,size = 30)
    drawLabel(app.cube.points[app.selectedDotIndex], app.width-app.editorWidth + 100+ 20, 100,size = 16)
    selectedCoord = app.viewport_point_List[app.selectedDotIndex]
    print(selectedCoord)
    drawLine(*selectedCoord,  selectedCoord[0]+70,  selectedCoord[1], fill='Red',
        lineWidth=6, dashes=False, opacity=80, rotateAngle=0,
        visible=True, arrowStart=False, arrowEnd=True)
    drawLine(*selectedCoord,  selectedCoord[0],  selectedCoord[1]-70, fill='Blue',
        lineWidth=6, dashes=False, opacity=80, rotateAngle=0,
        visible=True, arrowStart=False, arrowEnd=True)
    drawLine(*selectedCoord,  selectedCoord[0]+60,  selectedCoord[1]-30, fill='green',
        lineWidth=6, dashes=False, opacity=80, rotateAngle=0,
        visible=True, arrowStart=False, arrowEnd=True)

def redrawAll(app):
    #draw points
    for i in range(len(app.viewport_point_List)):
        point = app.viewport_point_List[i]
        fill = "lightSalmon"
        if i == app.selectedDotIndex:
            fill = "red"
        drawCircle(*point, 5, fill=fill)
    #draw lines
    for face in app.cube.faces:
        for edge in face.getEdges():
            drawLine(*app.viewport_point_List[edge[0]],*app.viewport_point_List[edge[1]])
    
    if app.editorMode:
        drawEditor(app)
        drawLabel("Editor Mode (press E to exit)",(app.width- app.editorWidth)/2, 20)
    else:
        drawLabel("Viewport Mode (press E to enter editor mode)",app.width/2, 20)

def onKeyPress(app, key):
    if key == "e":
        app.editorMode = not app.editorMode
        if app.editorMode:
            app.viewportCenter = ((app.width-app.editorWidth)/2,app.height/2)
        else:
            app.viewportCenter = ((app.width)/2,app.height/2)
    
    updateViewport(app)

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

    updateViewport(app)

def main():
    runApp(width=1000, height=800)

main()

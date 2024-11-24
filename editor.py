from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
from shapeCollectionObject import shapeCollectionObject
import math
import random

def onAppStart(app):

    initiateWelcome(app)
    app.editorMode = False
    app.selectedDotIndex = 0
    app.camTheta = (45, 45, 45)
    app.r = 50
    #editor attributes
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    #the shape object
    app.collection = shapeCollectionObject()
    app.collection.addShape(ShapeObject((0,0,0),0,1))
    app.viewport_point_List = []
    updateViewport(app)

def initiateWelcome(app):
    pass

def updateViewport(app):
    app.viewport_point_List = []
    for i in range(len(app.collection.shapes[0].points)):
        point = app.collection.shapes[0].points[i]
        viewport_point = transformToViewport(app, point)
        app.viewport_point_List.append(viewport_point)

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def onMousePress(app, mouseX, mouseY):
    cx, cy = app.viewport_point_List[app.selectedDotIndex]

    #1 handles clicks onto the shape
    if distance(mouseX, mouseY, cx, cy) > 5 and ((not app.editorMode) or (app.editorMode and mouseX <= app.width - app.editorWidth)):
        for i in range(len(app.viewport_point_List)):
            (x, y) = app.viewport_point_List[i]
            if distance(mouseX, mouseY, x, y) < 5:
                app.selectedDotIndex = i
        (x, y) = app.viewport_point_List[app.selectedDotIndex]
    
    if app.editorMode:

        inputIdx = inputEditorButton(app,mouseX,mouseY)
        #exit button
        if distance(mouseX, mouseY, app.width - 40 - app.editorWidth, 30) <= 25:
            print("Exit clicked")
            app.editorMode = False  
            app.viewportCenter = ((app.width)/2,app.height/2)
        #x y z input bars
        elif inputIdx[0] != -1:
            x,y,z = app.collection.shapes[0].points[app.selectedDotIndex]
            if inputIdx[0] == 0:
                newPoint = (x + inputIdx[1], y,z)
            elif inputIdx[0] == 1:
                newPoint = (x, y + inputIdx[1], z)    
            else:
                newPoint = (x, y , z+ inputIdx[1])  
            app.collection.shapes[0].points[app.selectedDotIndex] = newPoint
            print("Before rearrangeFaces:", app.collection.shapes[0].faces)
            app.collection.shapes[0].rearrangeFaces()
            print("After rearrangeFaces:", app.collection.shapes[0].faces)

            print((x,y,z), newPoint)
    else:
        if distance(mouseX, mouseY, app.width - 40, 30) <= 25:
            print("Editor entered")
            app.editorMode = True  
            app.viewportCenter = ((app.width-app.editorWidth)/2,app.height/2)
    updateViewport(app)


def inputEditorButton(app, x, y):
    button_height = 50
    button_margin = 60
    button_x_start = app.width - app.editorWidth + 80
    button_x_end = button_x_start + app.editorWidth - 110
    minus_x_center = app.width - app.editorWidth + 100
    plus_x_center = app.width - app.editorWidth + 200
    button_y_start_base = 200

    #this is the x y and z buttons that changes the coordinate
    for button in range(3):
        button_y_start = button_y_start_base + button * button_margin
        button_y_end = button_y_start + button_height

        if button_y_start <= y <= button_y_end:
            if (x - minus_x_center) ** 2 + (y - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
                return (button, -1)  # Minus button clicked
            elif (x - plus_x_center) ** 2 + (y - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
                return (button, +1)  
                
    return (-1, 0)

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
    drawLabel("Editor", app.width-app.editorWidth + 100+ 20, 70,size = 35)
    
    shift = 50
   # Coordinates of the current list
    selectedPoint = app.collection.shapes[0].points[app.selectedDotIndex]
    selectFaces = app.collection.shapes[0].getFaces(app.selectedDotIndex)
    drawLabel(selectedPoint, app.width - app.editorWidth + 120, 100+ shift, size=16, bold=True)
    drawLabel("X, Y, Z", app.width - app.editorWidth + 120, 80 + shift, size=16)
    drawLabel("The selected point is in faces: " + str(selectFaces), app.width - app.editorWidth + 120 , 120 + shift)

    # For each coordinate (X, Y, Z), draw plus, minus buttons and display the value
    selectedCoord = app.viewport_point_List[app.selectedDotIndex]
    coordList = ["X", "Y", "Z"]
    button_height = 50
    button_margin = 60

    for i, coord in enumerate(coordList):
        rounded = 20
        drawRect(app.width-app.editorWidth +  rounded+2,225 + i * button_margin - rounded+.8,40,2* rounded-.8,fill = "skyblue")
        drawCircle(app.width - app.editorWidth +  rounded + 8, 225 + i * button_margin,  rounded, fill="skyblue")
        drawCircle(app.width - app.editorWidth + 52, 225 + i * button_margin,  rounded, fill="skyblue")
        drawRect(app.width - app.editorWidth + 80, 200 + i * button_margin, app.editorWidth - 110, button_height, fill="lightGray", opacity=50)
        drawLabel(coordList[i], app.width-app.editorWidth+40,225+i*60, size = 30, fill = "black", opacity = 80)
        drawCircle(app.width - app.editorWidth + 100, 225 + i * button_margin, 15, fill="lightsalmon")
        drawLabel("-", app.width - app.editorWidth + 100, 225 + i * button_margin, size=20, bold=True, fill="red")
        drawLabel(f"{selectedPoint[i]}", app.width - app.editorWidth + 150, 225 + i * button_margin, size=20, bold=True)
        drawCircle(app.width - app.editorWidth + 200, 225 + i * button_margin, 15, fill="lightgreen")
        drawLabel("+", app.width - app.editorWidth + 200, 225 + i * button_margin, size=20, bold=True, fill="green")

def redrawAll(app):
    #draw points
    for i in range(len(app.viewport_point_List)):
        point = app.viewport_point_List[i]
        fill = "lightSalmon"
        if i == app.selectedDotIndex:
            fill = "red"
        drawCircle(*point, 5, fill=fill)
    #intermediate points






    #draw lines
    for faceidx in range(len(app.collection.shapes[0].faces)):
        r, g, b= random.randint(0,255), random.randint(0,255),random.randint(0,255)
        polygon = []
        #draws faces:
        selectFaces = app.collection.shapes[0].getFaces(app.selectedDotIndex)
        face = app.collection.shapes[0].faces[faceidx]
        for i in face.order:
            polygon.append(app.viewport_point_List[i][0])
            polygon.append(app.viewport_point_List[i][1])
        #print(app.colors, faceidx, len(app.colors))
        drawPolygon(*polygon, fill = rgb(*app.collection.shapes[0].faces[faceidx].color), opacity = 50)
        # draws lines
        for edge in face.getEdges():
            drawLine(*app.viewport_point_List[edge[0]],*app.viewport_point_List[edge[1]])

    if app.editorMode:
        drawEditor(app)
        drawCircle(app.width - 40 - app.editorWidth, 30, 25, fill="Salmon")
        drawLabel("Exit", app.width - 40 - app.editorWidth, 30, size=12, bold=True, fill="maroon")
        drawLabel("Editor Mode (press Exit to exit editor mode)",(app.width- app.editorWidth)/2, 20)
    else:
        drawCircle(app.width - 40, 30, 25, fill='lightSkyBlue')
        drawLabel("Editor", app.width - 40, 30, size=12, bold=True, fill="darkblue")
        drawLabel("Viewport Mode (press Editor button to enter editor mode)",app.width/2, 20)

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

runApp(width=1000, height=800)

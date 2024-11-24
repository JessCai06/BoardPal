from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
from shapeCollectionObject import shapeCollectionObject
import math
import random

def onAppStart(app):

    initiateWelcome(app)
    app.editorMode = False
    app.selectedDotIndex = (0,0)
    app.camTheta = (45, 45, 45)
    app.r = 50
    #editor attributes
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    #the shape object
    app.collection = shapeCollectionObject()
    app.collection.addShape(ShapeObject((0,0,0),0,1))
    app.viewport_point_List = {}
    updateViewport(app)

def initiateWelcome(app):
    pass

def updateViewport(app):
    app.viewport_point_List = {}
    for j, shape in enumerate(app.collection.shapes):
        tempShapeviewList = []
        for i in range(len(shape.points)):
            point = shape.points[i]
            viewport_point = transformToViewport(app, point)
            tempShapeviewList.append(viewport_point)
        app.viewport_point_List[j] = tempShapeviewList

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def onMousePress(app, mouseX, mouseY):
    selectedShapeIndex, selectedDotIndex = app.selectedDotIndex

    shapeClicked = False
    for shapeIndex, viewPoints in app.viewport_point_List.items():
        for dotIndex, (cx, cy) in enumerate(viewPoints):
            if distance(mouseX, mouseY, cx, cy) < 5:
                app.selectedDotIndex = (shapeIndex, dotIndex)
                shapeClicked = True
                break
        if shapeClicked:
            break

    if app.editorMode:
        inputIdx = inputEditorButton(app, mouseX, mouseY)

        if distance(mouseX, mouseY, app.width - 40 - app.editorWidth, 30) <= 25:
            app.editorMode = False
            app.viewportCenter = ((app.width) / 2, app.height / 2)
        elif inputIdx[0] != -1:
            shapeIndex, dotIndex = app.selectedDotIndex
            shape = app.collection.shapes[shapeIndex]
            x, y, z = shape.points[dotIndex]

            if inputIdx[0] == 0:
                newPoint = (x + inputIdx[1], y, z)
            elif inputIdx[0] == 1:
                newPoint = (x, y + inputIdx[1], z)
            else:
                newPoint = (x, y, z + inputIdx[1])

            shape.points[dotIndex] = newPoint
            shape.rearrangeFaces()
    else:
        if distance(mouseX, mouseY, app.width - 40, 30) <= 25:
            app.editorMode = True
            app.viewportCenter = ((app.width - app.editorWidth) / 2, app.height / 2)

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
    drawRect(app.width - app.editorWidth, 0, app.editorWidth, app.height, fill="powderBlue", opacity=80)
    drawLabel("Editor", app.width - app.editorWidth + 120, 70, size=35)

    shapeIndex, dotIndex = app.selectedDotIndex
    selectedPoint = app.collection.shapes[shapeIndex].points[dotIndex]
    selectFaces = app.collection.shapes[shapeIndex].getFaces(dotIndex)

    drawLabel(selectedPoint, app.width - app.editorWidth + 120, 150, size=16, bold=True)
    drawLabel("X, Y, Z", app.width - app.editorWidth + 120, 130, size=16)
    drawLabel(f"The selected point is in faces: {selectFaces}", app.width - app.editorWidth + 120, 170)

    coordList = ["X", "Y", "Z"]
    button_height = 50
    button_margin = 60

    for i, coord in enumerate(coordList):
        y = 225 + i * button_margin
        drawRect(app.width - app.editorWidth + 22, y - 25, 40, 50, fill="skyblue")
        drawCircle(app.width - app.editorWidth + 28, y, 20, fill="skyblue")
        drawCircle(app.width - app.editorWidth + 62, y, 20, fill="skyblue")
        drawRect(app.width - app.editorWidth + 80, y - 25, app.editorWidth - 110, button_height, fill="lightGray", opacity=50)
        drawLabel(coordList[i], app.width - app.editorWidth + 40, y, size=30, fill="black")
        drawCircle(app.width - app.editorWidth + 100, y, 15, fill="lightsalmon")
        drawLabel("-", app.width - app.editorWidth + 100, y, size=20, bold=True, fill="red")
        drawLabel(f"{selectedPoint[i]}", app.width - app.editorWidth + 150, y, size=20, bold=True)
        drawCircle(app.width - app.editorWidth + 200, y, 15, fill="lightgreen")
        drawLabel("+", app.width - app.editorWidth + 200, y, size=20, bold=True, fill="green")


def redrawAll(app):
    for shapeIndex, viewPoints in app.viewport_point_List.items():
        for dotIndex, point in enumerate(viewPoints):
            fill = "lightSalmon"
            if (shapeIndex, dotIndex) == app.selectedDotIndex:
                fill = "red"
            drawCircle(*point, 5, fill=fill)
            print(shapeIndex, viewPoints)

        shape = app.collection.shapes[shapeIndex]
        for face in shape.faces:
            polygon = [(viewPoints[vertexIndex][0], viewPoints[vertexIndex][1]) for vertexIndex in face.order]
            drawPolygon(*[coord for vertex in polygon for coord in vertex], fill=rgb(*face.color), opacity=50)

            for edge in face.getEdges():
                drawLine(
                    *viewPoints[edge[0]],
                    *viewPoints[edge[1]]
                )


    if app.editorMode:
        drawEditor(app)
        drawCircle(app.width - 40 - app.editorWidth, 40, 25, fill="Salmon")
        drawLabel("Exit", app.width - 40 - app.editorWidth, 40, size=12, bold=True, fill="maroon")
        drawLabel("Editor Mode (press Exit to exit editor mode)", (app.width - app.editorWidth) / 2, 20)

        drawCircle(app.width - 40 - app.editorWidth, 110, 25, fill='lightSkyBlue')
        drawLabel("Add", app.width - 40 - app.editorWidth, 110, size=12, bold=True, fill="darkblue")
    else:
        drawCircle(app.width - 40, 40, 25, fill='lightSkyBlue')
        drawLabel("Editor", app.width - 40, 40, size=12, bold=True, fill="darkblue")
        drawLabel("Viewport Mode (press Editor button to enter editor mode)", app.width / 2, 20)

def onKeyHold(app, key):
    thetaX, thetaY, thetaZ = app.camTheta  
    if "8" in key:
        app.collection.addShape(ShapeObject((0,0,0),1,3))
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

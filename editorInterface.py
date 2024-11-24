from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
from shapeCollectionObject import shapeCollectionObject
from buttonHandler import ButtonHandler
import math
import random

def onAppStart(app):
    app.mode = "viewport"
    app.buttonList = []
    initiateWelcome(app)
    initiateEditor(app)

def initiateWelcome(app):
    app.collection = shapeCollectionObject()
    app.keyDisabled = False
    app.collection.addShape(ShapeObject((0,0,0),1,0))

def initiateEditor(app):
    app.selectedDotIndex = (0,0)
    app.camTheta = (45, 45, 45)
    app.r = 50
    app.keyDisabled = False
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    app.viewport_point_List = {}
    updateViewport(app)

def onMousePress(app, mouseX, mouseY):
    eventHandler(app)
    if app.mode == "viewport":
        for button in app.buttonList:
            #entering into editor mode
            if button.isClicked(mouseX, mouseY):
                app.mode = "editorMan"
    elif app.mode == "editorMan":
        for button in app.buttonList:
            #entering into editor mode
            if button.isClicked(mouseX, mouseY):
                if button.name == "exit":
                    app.mode = "viewport"
    elif app.mode == "editorAddShape":
        pass

def eventHandler(app):
    app.buttonList = []

    if app.mode == "viewport":
        app.keyDisabled = False
        editor_button = ButtonHandler(buttonType="circle",cx=app.width - 40,cy=40,radius=25,name = "")
        app.buttonList.append(editor_button)

    elif app.mode == "editorMan":
        app.keyDisabled = False
        exit_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40 - app.editorWidth,
            cy=40,
            radius=25,
            name = "exit"
        )
        app.buttonList.append(exit_button)

    elif app.mode == "editorAddShape":
        app.keyDisabled = True
        confirm_button = ButtonHandler(
            buttonType="rectangle",
            x=app.width - app.editorWidth + 20,
            y=300,
            width=app.editorWidth - 40,
            height=50
        )
        app.buttonList.append(confirm_button)

def redrawAll(app):
    if app.mode == "viewport":
        drawViewport(app)
    elif app.mode == "editorMan":
        drawViewport(app)
        drawEditorForManipulation(app)
    elif app.mode == "editorAddShape":
        drawViewport(app)
        drawRect(0, 0, app.width, app.height, fill="black", opacity=50)
        drawAddShapePanel(app)   

def drawAddShapePanel(app):
    panelX = app.width - app.editorWidth
    drawRect(panelX, 0, app.editorWidth, app.height, fill="lightBlue", opacity=100)
    drawLabel("Add New Shape", panelX + app.editorWidth / 2, 40, size=25, bold=True)

    # Category buttons (Standard / Prism)
    categoryY = 100
    buttonWidth = (app.editorWidth - 40) // 2
    drawRect(panelX + 20, categoryY, buttonWidth, 50, fill="skyblue", border="black", borderWidth=2)
    drawLabel("Standard", panelX + 20 + buttonWidth / 2, categoryY + 25, size=14, bold=True)

    drawRect(panelX + 40 + buttonWidth, categoryY, buttonWidth, 50, fill="skyblue", border="black", borderWidth=2)
    drawLabel("Prism", panelX + 40 + buttonWidth / 2 + buttonWidth, categoryY + 25, size=14, bold=True)

    # Shape buttons (Pyramid, Cube, etc.)
    shapeY = 180
    shapeOptions = ["Pyramid", "Cube", "Hexagon", "Pentagon"]
    buttonHeight = 50
    for i, shape in enumerate(shapeOptions):
        drawRect(panelX + 20, shapeY + i * (buttonHeight + 10), app.editorWidth - 40, buttonHeight, fill="lightGray",
                 border="black", borderWidth=2)
        drawLabel(shape, panelX + app.editorWidth / 2, shapeY + i * (buttonHeight + 10) + buttonHeight / 2, size=14, bold=True)

    # Confirm button
    confirmY = shapeY + len(shapeOptions) * (buttonHeight + 10) + 20
    drawRect(panelX + 20, confirmY, app.editorWidth - 40, 50, fill="green")
    drawLabel("Confirm", panelX + app.editorWidth / 2, confirmY + 25, size=16, bold=True, fill="white")

def drawEditorForManipulation(app):
    drawRect(app.width - app.editorWidth, 0, app.editorWidth, app.height, fill="powderBlue", opacity=80)
    drawLabel("Editor", app.width - app.editorWidth + 120, 40, size=35)

    shapeIndex, dotIndex = app.selectedDotIndex
    selectedShape = app.collection.shapes[shapeIndex]
    selectedPoint = selectedShape.points[dotIndex]
    selectFaces = selectedShape.getFaces(dotIndex)

    y_start = 80
    x_start = app.width - app.editorWidth + 20
    button_width = (app.editorWidth - 60) // len(app.collection.shapes)
    button_height = 50

    for i, shape in enumerate(app.collection.shapes):
        x = x_start + i * (button_width + 10)

        drawRect(x + 10, y_start, button_width - 20, button_height, fill="skyblue")
        drawCircle(x + 10, y_start + button_height / 2, button_height / 2, fill="skyblue")
        drawCircle(x + button_width - 10, y_start + button_height / 2, button_height / 2, fill="skyblue")

        if shapeIndex == i:
            drawRect(x + 10, y_start, button_width - 20, button_height, fill=None, border="red", borderWidth=2)
            drawCircle(x + 10, y_start + button_height / 2, button_height / 2, fill=None, border="red", borderWidth=2)
            drawCircle(x + button_width - 10, y_start + button_height / 2, button_height / 2, fill=None, border="red", borderWidth=2)

        drawLabel(f"Shape {i + 1}", x + button_width / 2, y_start + button_height / 2, size=14, bold=True)

    y_point = y_start + 100
    drawLabel(f"Currently selected point: {selectedPoint}", app.width - app.editorWidth + 20, y_point, size=14, align="left")
    drawLabel(f"Faces: {selectFaces}", app.width - app.editorWidth + 20, y_point + 20, size=12, align="left")

    coordList = ["X", "Y", "Z"]
    for i, coord in enumerate(coordList):
        y = y_point + 60 + i * 50
        drawLabel(coord, app.width - app.editorWidth + 40, y, size=16, bold=True)
        drawCircle(app.width - app.editorWidth + 100, y, 15, fill="lightsalmon")
        drawLabel("-", app.width - app.editorWidth + 100, y, size=14, bold=True, fill="red")
        drawCircle(app.width - app.editorWidth + 200, y, 15, fill="lightgreen")
        drawLabel("+", app.width - app.editorWidth + 200, y, size=14, bold=True, fill="green")



############################################## 
############################################## MISC
############################################## 

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

def onKeyHold(app, key):
    if not app.keyDisabled:
        thetaX, thetaY, thetaZ = app.camTheta  
        if "8" in key:
            app.collection.addShape(ShapeObject((0,0,0),1,0))
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

def updateViewport(app):
    app.viewport_point_List = {}
    for j, shape in enumerate(app.collection.shapes):
        tempShapeviewList = []
        for i in range(len(shape.points)):
            point = shape.points[i]
            viewport_point = transformToViewport(app, point)
            tempShapeviewList.append(viewport_point)
        app.viewport_point_List[j] = tempShapeviewList

def drawViewport(app):
    drawCircle(app.width - 40, 40, 25, fill='lightSkyBlue')
    drawLabel("Editor", app.width - 40, 40, size=12, bold=True, fill="darkblue")
    for shapeIndex, viewPoints in app.viewport_point_List.items():
        for dotIndex, point in enumerate(viewPoints):
            fill = "lightSalmon"
            if (shapeIndex, dotIndex) == app.selectedDotIndex:
                fill = "red"
            drawCircle(*point, 5, fill=fill)

        shape = app.collection.shapes[shapeIndex]
        for face in shape.faces:
            polygon = [(viewPoints[vertexIndex][0], viewPoints[vertexIndex][1]) for vertexIndex in face.order]
            drawPolygon(*[coord for vertex in polygon for coord in vertex], fill=rgb(*face.color), opacity=50)

            for edge in face.getEdges():
                drawLine(*viewPoints[edge[0]], *viewPoints[edge[1]])

runApp(width=1000, height=800)





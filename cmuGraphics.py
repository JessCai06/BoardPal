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
    #editor attributes
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    app.inputBarSelect = -1
    app.inputText = ""

    #the shape object
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
            x,y,z = app.cube.points[app.selectedDotIndex]
            if inputIdx[0] == 0:
                newPoint = (x + inputIdx[1], y,z)
            elif inputIdx[0] == 1:
                newPoint = (x, y + inputIdx[1], z)    
            else:
                newPoint = (x, y , z+ inputIdx[1])  
            app.cube.points[app.selectedDotIndex] = newPoint
            print("Before rearrangeFaces:", app.cube.faces)
            app.cube.rearrangeFaces()
            print("After rearrangeFaces:", app.cube.faces)

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

    for button in range(3):
        button_y_start = button_y_start_base + button * button_margin
        button_y_end = button_y_start + button_height

        if button_y_start <= y <= button_y_end:
            if (x - minus_x_center) ** 2 + (y - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
                return (button, -1)  # Minus button clicked
            elif (x - plus_x_center) ** 2 + (y - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
                return (button, +1)  # Plus button clicked
                
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
    drawLabel("Editor", app.width-app.editorWidth + 100+ 20, 20,size = 30)
    
   # Coordinates of the current list
    selectedPoint = app.cube.points[app.selectedDotIndex]
    selectFaces = app.cube.getFaces(app.selectedDotIndex)
    drawLabel(selectedPoint, app.width - app.editorWidth + 120, 100, size=16, bold=True)
    drawLabel("X, Y, Z", app.width - app.editorWidth + 120, 80, size=16)
    drawLabel("The selected point is in faces: " + str(selectFaces), app.width - app.editorWidth + 120, 120)

    # For each coordinate (X, Y, Z), draw plus, minus buttons and display the value
    selectedCoord = app.viewport_point_List[app.selectedDotIndex]
    coordList = ["X", "Y", "Z"]
    button_height = 50
    button_margin = 60

    for i, coord in enumerate(coordList):
        drawLabel(coord, app.width - app.editorWidth + 15, 200 + i * button_margin, size=30)
        drawRect(app.width - app.editorWidth + 80, 200 + i * button_margin, app.editorWidth - 110, button_height, fill="lightGray", border="blue", opacity=50)
        drawCircle(app.width - app.editorWidth + 100, 225 + i * button_margin, 15, fill="lightGray", border="red")
        drawLabel("-", app.width - app.editorWidth + 100, 225 + i * button_margin, size=20, bold=True, fill="red")
        drawLabel(f"{selectedPoint[i]}", app.width - app.editorWidth + 150, 225 + i * button_margin, size=20, bold=True)
        drawCircle(app.width - app.editorWidth + 200, 225 + i * button_margin, 15, fill="lightGray", border="green")
        drawLabel("+", app.width - app.editorWidth + 200, 225 + i * button_margin, size=20, bold=True, fill="green")

    coordList = ["X", "Y", "Z"]
    for button in range(3):
        border = "blue"
        if app.inputBarSelect != -1 and app.inputBarSelect == button:
            border = "gold"
        drawLabel(coordList[button], app.width-app.editorWidth+15,200+button*60, size = 30)
        drawRect(app.width-app.editorWidth+80,200+button*60,app.editorWidth-110,50,fill = "lightGray", border = border, opacity = 50)

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
        drawCircle(app.width - 40 - app.editorWidth, 30, 25, fill="Salmon")
        drawLabel("Exit", app.width - 40 - app.editorWidth, 30, size=12, bold=True, fill="maroon")
        drawLabel("Editor Mode (press Exit to exit editor mode)",(app.width- app.editorWidth)/2, 20)
    else:
        drawCircle(app.width - 40, 30, 25, fill='lightSkyBlue')
        drawLabel("Editor", app.width - 40, 30, size=12, bold=True, fill="darkblue")
        drawLabel("Viewport Mode (press Editor button to enter editor mode)",app.width/2, 20)

def onKeyPress(app, key):
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
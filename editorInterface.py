from cmu_graphics import *
from ShapeObject import ShapeObject
from FaceObject import FaceObject
from shapeCollectionObject import shapeCollectionObject
from buttonHandler import ButtonHandler
import math
import random
import re

def onAppStart(app):
    app.mode = "viewport"
    app.buttonList = []
    app.defaultNewShape = (1,2)
    initiateWelcome(app)
    initiateEditor(app)

def initiateWelcome(app):
    app.collection = shapeCollectionObject()
    app.keyDisabled = False
    #app.collection.addShape(ShapeObject((0,0,0),1,0))

def initiateEditor(app):
    app.selectedDotIndex = (0,0)
    app.camTheta = (45, 45, 45)
    app.r = 50
    app.keyDisabled = False
    app.viewportCenter = (app.width/2,app.height/2)
    app.editorWidth = 250
    app.viewport_point_List = {}
    updateViewport(app)

def inputEditorButton(app, mouseX, mouseY):
    button_height = 50
    button_margin = 60
    button_x_start = app.width - app.editorWidth + 80
    button_x_end = button_x_start + app.editorWidth - 110
    minus_x_center = app.width - app.editorWidth + 100
    plus_x_center = app.width - app.editorWidth + 200
    button_y_start_base = 200

    # Check X, Y, Z buttons
    for button in range(3):  # X, Y, Z buttons
        button_y_start = button_y_start_base + button * button_margin
        button_y_end = button_y_start + button_height

        # Check for minus button (-)
        if (mouseX - minus_x_center) ** 2 + (mouseY - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
            return (button, -1)  # Minus button clicked

        # Check for plus button (+)
        elif (mouseX - plus_x_center) ** 2 + (mouseY - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
            return (button, +1)  # Plus button clicked

    return (-1, 0)  

def inputEditorButton(app, mouseX, mouseY):
    button_height = 50
    button_margin = 60
    button_x_start = app.width - app.editorWidth + 80
    button_x_end = button_x_start + app.editorWidth - 110
    minus_x_center = app.width - app.editorWidth + 100
    plus_x_center = app.width - app.editorWidth + 200
    button_y_start_base = 200

    # Check X, Y, Z buttons
    for button in range(3):  # X, Y, Z buttons
        button_y_start = button_y_start_base + button * button_margin
        button_y_end = button_y_start + button_height

        # Check for minus button (-)
        if (mouseX - minus_x_center) ** 2 + (mouseY - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
            return (button, -1)  # Minus button clicked

        # Check for plus button (+)
        elif (mouseX - plus_x_center) ** 2 + (mouseY - (button_y_start + button_height // 2)) ** 2 <= 15 ** 2:
            return (button, +1)  # Plus button clicked

    return (-1, 0)  

def onMousePress(app, mouseX, mouseY):
    eventHandler(app)  # Update the button list based on the current mode

    if app.mode == "viewport":
        for button in app.buttonList:
            if button.isClicked(mouseX, mouseY):
                app.mode = "editorMan"  

    elif app.mode == "editorMan":
        shapeClicked = False

        # Handle shape button clicks
        for button in app.buttonList:
            if button.isClicked(mouseX, mouseY):
                if button.buttonType == "circle" and button.name == "addshape" and len(app.collection.shapes) <= 1:
                    app.mode = "editorAddShape" 
                elif button.buttonType == "circle" and button.name == "merge" and len(app.collection.shapes) == 2 and app.collection.canMerge():
                    app.collection.mergeAll()
                    app.selectedDotIndex = (0,0)
                    app.mode = "editorMan" 
                elif button.buttonType == "circle" and button.name == "deleteshape":
                    print(len(app.collection.shapes))
                    app.collection.removeShape(app.selectedDotIndex[0])
                    app.selectedDotIndex = (0,0)
                elif button.buttonType == "circle" and button.name == "exit":
                    app.mode = "viewport"  
                elif button.buttonType == "rectangle" and button.name == "shapeSelector":
                    app.selectedDotIndex = (button.shapeIndex, app.selectedDotIndex[1])  
                    shapeClicked = True
                    break

        if not shapeClicked:
            # Handle clicks on shape points
            for shapeIndex, viewPoints in app.viewport_point_List.items():
                for dotIndex, (cx, cy) in enumerate(viewPoints):
                    if distance(mouseX, mouseY, cx, cy) < 5:
                        app.selectedDotIndex = (shapeIndex, dotIndex)
                        shapeClicked = True
                        break
                if shapeClicked:
                    break

        inputIdx = inputEditorButton(app, mouseX, mouseY)
        if inputIdx[0] != -1:
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

    elif app.mode == "editorAddShape":
        for button in app.buttonList:
            if button.isClicked(mouseX, mouseY):
                print(button.buttonType, button.name)
                if button.buttonType == "rectangle" and button.name == "Generate shape via AI":
                    app.mode = "loading"
                    userInput = app.getTextInput("Enter a description of a 3D shape (e.g., '3D octagonal prism') - the more detailed the better!")
                    parsedThing = retrievingJson(userInput)
                    if parsedThing != None:
                        points, order = parsedThing
                        print("this is the points", points)
                        print("this is the order", order)
                        newShape = ShapeObject((0,0,0), points, order)
                        app.collection.addShape(newShape)
                        app.mode = "editorMan"
                    else:
                        print("BAD BAD BAD")
                elif button.buttonType == "rectangle" and button.name == "Create!":
                    app.collection.addShape(ShapeObject((0, 0, 0), *app.defaultNewShape))
                    app.mode = "editorMan" 
                elif button.buttonType == "rectangle" and type(button.name) == tuple:
                    app.defaultNewShape = button.name
    elif app.mode == "ERROR":
        pass

    updateViewport(app)  

def parse_points_and_order(input_string):
    # Find the start and end indices for the "points" and "order" sections
    points_start = input_string.find('"points": [') + len('"points": [')
    points_end = input_string.find(']', points_start)
    
    order_start = input_string.find('"order": [') + len('"order": [')
    order_end = input_string.rfind(']')
    
    # Extract the substrings containing the points and order
    points_str = input_string[points_start:points_end]
    order_str = input_string[order_start:order_end]
    
    # Parse points: Split by "), (" and remove the surrounding parentheses and extra spaces
    points = []
    points_list = points_str.split('), (')
    for point in points_list:
        # Remove any surrounding spaces and parentheses, then convert to a tuple of floats
        point = point.strip(' ()')
        point_tuple = tuple(map(float, point.split(',')))
        points.append(point_tuple)
    
    # Parse order: Split by '], [' and convert to lists of integers
    order = []
    order_list = order_str.split('], [')
    for group in order_list:
        # Remove any surrounding spaces and brackets, then split by commas and convert to integers
        group = group.strip(' []')
        group_list = list(map(int, group.split(',')))
        order.append(group_list)
        print(group_list)
    
    return points, order

def retrievingJson(user_input):

    print("Welcome to the 3D Shape Generator!")
    result = generate_3d_shape(user_input)
    print(result)
    try:
        if "points" in result and "order" in result:
            points, order = parse_points_and_order(result)
            print(points, order)
            return points, order
        else:
            print("\nThe response contains guidelines or an unexpected format:")
            print(result)
    except json.JSONDecodeError:
        # Print guidelines or plain text if the result is not JSON
        print("\nThe response from OpenAI:")
        print(result)

def eventHandler(app):
    app.buttonList = []  
    if len(app.collection.shapes) == 0:
        app.mode = "editorAddShape"
    if len(app.collection.shapes) == 1:
        app.collection.shapes[0].moveCenter((0,0,0))

    if app.mode == "viewport":
        app.keyDisabled = False
        editor_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40,
            cy=40,
            radius=25,
            name="editor"
        )
        app.buttonList.append(editor_button)

    elif app.mode == "editorMan":
        app.keyDisabled = False
        exit_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40 - app.editorWidth,
            cy=40,
            radius=25,
            name="exit"
        )
        app.buttonList.append(exit_button)

        add_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40 - app.editorWidth,
            cy=100,
            radius=25,
            name="addshape"
        )
        app.buttonList.append(add_button)

        delete_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40 - app.editorWidth,
            cy=160,
            radius=25,
            name="deleteshape"
        )
        app.buttonList.append(delete_button)
    
        merge_button = ButtonHandler(
            buttonType="circle",
            cx=app.width - 40 - app.editorWidth,
            cy=220,
            radius=25,
            name="merge"
        )
        app.buttonList.append(merge_button)

        # Add shape selector buttons
        button_width = (app.editorWidth - 60) 
        button_height = 50
        x_start = app.width - app.editorWidth + 20
        y_start = 80

        for i, shape in enumerate(app.collection.shapes):
            shape_button = ButtonHandler(
                buttonType="rectangle",
                x=x_start + i * (button_width + 10),
                y=y_start,
                width=button_width,
                height=button_height,
                name="shapeSelector",
                shapeIndex=i
            )
            app.buttonList.append(shape_button)

    elif app.mode == "editorAddShape":
        panelX = app.width - app.editorWidth

        # Standard Shapes Buttons
        categoryY = 170
        standardShapes = ["Pyramid", "Cube"]
        buttonHeight = 30
        shapeY = categoryY + 30
        for i, shape in enumerate(standardShapes):
            textWidth = len(shape) * 10
            button = ButtonHandler(
                buttonType="rectangle",
                x=panelX + 20,
                y=shapeY + i * (buttonHeight + 5),
                width=textWidth,
                height=buttonHeight,
                name=(0,i)
            )
            app.buttonList.append(button)

        # Prisms Buttons
        prismY = shapeY + len(standardShapes) * (buttonHeight + 5) + 20
        prismShapes = ["Triangular", "Square", "Hexagonal", "Pentagonal"]
        prismY += 30
        for i, shape in enumerate(prismShapes):
            textWidth = len(shape) * 10
            button = ButtonHandler(
                buttonType="rectangle",
                x=panelX + 20,
                y=prismY + i * (buttonHeight + 5),
                width=textWidth,
                height=buttonHeight,
                name=(1,i)
            )
            app.buttonList.append(button)
        
                # Confirm Button
        confirmY = prismY + len(prismShapes) * (buttonHeight + 5) + 20
        confirmButton = ButtonHandler(
            buttonType="rectangle",
            x=panelX + 20,
            y=confirmY,
            width=app.editorWidth,
            height=40,
            name="Generate shape via AI"
        )
        app.buttonList.append(confirmButton)

        # Confirm Button
        confirmButton = ButtonHandler(
            buttonType="rectangle",
            x=panelX + 20,
            y=app.height-200,
            width=app.editorWidth +100,
            height=40,
            name="Create!"
        )
        app.buttonList.append(confirmButton)

def redrawAll(app):
    print(app.mode)
    for s in app.collection.shapes:
        print(s)
    if len(app.collection.shapes) == 0:
        drawViewport(app)
        drawRect(0, 0, app.width, app.height, fill="black", opacity=50)
        drawAddShapePanel(app)
    else:   
        if app.mode == "loading":
            drawRect(0, 0, app.width, app.height, fill="black", opacity=50)
            drawLabel("Loading API response....", app.width/2, app.height/2, size = 30, fill = "white")
        elif app.mode == "viewport":
            drawViewport(app)
            drawCircle(app.width - 40, 40, 25, fill='lightSkyBlue')
            drawLabel("Editor", app.width - 40, 40, size=12, bold=True, fill="darkblue")
        elif app.mode == "editorMan":
            drawViewport(app)
            drawCircle(app.width - 40 - app.editorWidth, 40, 25, fill="Salmon")
            drawLabel("Exit", app.width - 40 - app.editorWidth, 40, size=12, bold=True, fill="maroon")
            #can't add a shape when there are 2 or more shapes already
            if len(app.collection.shapes) >= 2:
                drawCircle(app.width - 40 - app.editorWidth, 100, 25, fill='lightGray')
                drawLabel("Add", app.width - 40 - app.editorWidth, 100, size=12, bold=True, fill="Gray")
            else: 
                drawCircle(app.width - 40 - app.editorWidth, 100, 25, fill='lightSkyBlue')
                drawLabel("Add", app.width - 40 - app.editorWidth, 100, size=12, bold=True, fill="darkblue")
            #merge button
            if len(app.collection.shapes) == 2 and app.collection.canMerge():
                print("why is this not printing")
                print("this is the shared list", app.collection.getSharedFaces())
                drawCircle(app.width - 40 - app.editorWidth, 220, 25, fill='lightSkyBlue')
                drawLabel("Merge", app.width - 40 - app.editorWidth, 220, size=12, bold=True, fill="darkblue")
            else: 
                drawCircle(app.width - 40 - app.editorWidth, 220, 25, fill='lightGray')
                drawLabel("Merge", app.width - 40 - app.editorWidth, 220, size=12, bold=True, fill="Gray")
            drawCircle(app.width - 40 - app.editorWidth, 160, 25, fill='lightSkyBlue')
            drawLabel("Delete", app.width - 40 - app.editorWidth, 160, size=12, bold=True, fill="darkblue")
            drawEditorForManipulation(app)
        elif app.mode == "editorAddShape":
            drawViewport(app)
            drawRect(0, 0, app.width, app.height, fill="black", opacity=50)
            drawAddShapePanel(app)   

def drawAddShapePanel(app):
    panelX = app.width - app.editorWidth
    drawRect(panelX, 0, app.editorWidth, app.height, fill=rgb(128, 196, 233), opacity=100)
    drawLabel("Editor", panelX + app.editorWidth / 2, 40, size=25, bold=True)
    drawLabel("Add New Shape", panelX + app.editorWidth / 2, 80, size=20, bold=True)

    centerY = 120
    drawLabel("Spawn Point:", panelX + 20, centerY, size=14, align="left", bold=True)
    spawn = app.collection.getNewSpawnPoint(ShapeObject((0, 0, 0), *app.defaultNewShape))
    drawLabel(spawn, panelX + 150, centerY, size=14, bold=True)

    # Standard Shapes Section
    categoryY = centerY + 50
    drawLabel("Standard Shapes", panelX + 20, categoryY, size=16, bold=True, align="left")

    standardShapes = ["Pyramid", "Cube"]
    buttonHeight = 30
    shapeY = categoryY + 30
    for i, shape in enumerate(standardShapes):
        textWidth = len(shape) * 10 
        fill = rgb(255, 246, 233)
        if app.defaultNewShape == (0,i):
            fill = "orange"
        drawRect(panelX + 20, shapeY + i * (buttonHeight + 5), textWidth, buttonHeight, fill=fill)
        drawLabel(shape, panelX + 20 + textWidth / 2, shapeY + i * (buttonHeight + 5) + buttonHeight / 2, size=12, bold=True)

    # Prisms Section
    prismY = shapeY + len(standardShapes) * (buttonHeight + 5) + 20
    drawLabel("Prisms", panelX + 20, prismY, size=16, bold=True, align="left")

    prismShapes = ["Triangular", "Square", "Hexagonal", "Pentagonal"]
    prismY += 30
    for i, shape in enumerate(prismShapes):
        textWidth = len(shape) * 10 
        fill = rgb(255, 246, 233)
        if app.defaultNewShape == (1,i):
            fill = "orange"
        drawRect(panelX + 20, prismY + i * (buttonHeight + 5), textWidth, buttonHeight, fill=fill)
        drawLabel(shape, panelX + 20 + textWidth / 2, prismY + i * (buttonHeight + 5) + buttonHeight / 2, size=12, bold=True)

    confirmY = prismY + len(prismShapes) * (buttonHeight + 5) + 20
    drawRect(panelX + 20, confirmY, app.editorWidth - 40, 40, fill=rgb(255, 127, 62), border="black", borderWidth=2)
    drawLabel("Generate shape via AI", panelX + app.editorWidth / 2, confirmY + 20, size=14, bold=True, fill="white")
    # Confirm Button
    confirmY = prismY + len(prismShapes) * (buttonHeight + 5) + 20
    drawRect(panelX + 20, app.height-200, app.editorWidth - 40, 40, fill=rgb(255, 127, 62), border="black", borderWidth=2)
    drawLabel("Create!", panelX + app.editorWidth / 2, app.height-180, size=14, bold=True, fill="white")

def drawEditorForManipulation(app):
    drawRect(app.width - app.editorWidth, 0, app.editorWidth, app.height, fill="powderBlue", opacity=80)
    drawLabel("Editor", app.width - app.editorWidth + 120, 40, size=35)

    shapeIndex, dotIndex = app.selectedDotIndex
    selectedShape = app.collection.shapes[shapeIndex]
    selectedPoint = selectedShape.points[dotIndex]
    selectFaces = selectedShape.getFacesAdjacentToPoint(dotIndex)

    y_start = 80
    x_start = app.width - app.editorWidth + 40
    button_width = (app.editorWidth - 100) // len(app.collection.shapes)
    button_height = 50

    for i, shape in enumerate(app.collection.shapes):
        x = x_start + i * (button_width + 40)

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
        drawCircle (10,10,100)
        drawLabel(selectedPoint[i], app.width - app.editorWidth + 10, y, size=14, bold=True, fill="red")
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

import requests
import json

# Your OpenAI API key
API_KEY = "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"

# OpenAI API endpoint for chat completions
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_3d_shape(user_input):
    """
    Sends a request to OpenAI to generate a 3D shape based on user input.

    :param user_input: A description of the desired 3D shape.
    :return: JSON response containing points and order or guidelines for improvement.
    """
    # Prepare the request payload
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"You are a 3D shape generator assistant. The user wants to generate a 3D shape based on the following description: {user_input}. If the description is sufficient, respond strictly with the JSON representation of the shape in the following format: {{ \"points\": [(x1, y1, z1), (x2, y2, z2), ...], \"order\": [[index1, index2, index3, ...], ...] }}. Do not include any extra text, explanations, or instructions. If the description is insufficient or invalid, respond only with 'Invalid description'."
                )
            }
        ],
        "temperature": 0.7
    }

    # Set up headers for authentication and content type
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send the POST request to the OpenAI API
    response = requests.post(API_URL, headers=headers, json=payload)

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    else:
        return f"Error: {response.status_code} - {response.text}"


runApp(width=1000, height=800)





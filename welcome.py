from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.currentPage = "welcome"  # Default page is the welcome page
    app.selectedCategory = None

    # Setup for shape editing
    app.editorMode = False
    app.selectedDotIndex = 0
    app.camTheta = (45, 45, 45)
    app.graphCenter = (0, 0)
    app.r = 50

    # Editor attributes
    app.viewportCenter = (app.width / 2, app.height / 2)
    app.editorWidth = 250

def drawWelcomePage(app):
    # Title
    drawLabel("ShapeShifter", app.width / 2, 100, size=40, bold=True, align='center')

    # Buttons
    drawRect(app.width / 2 - 150, 200, 300, 80, fill='orange')  # "Standard Shapes"
    drawLabel("Standard Shapes", app.width / 2, 240, size=20, align='center')

    drawRect(app.width / 2 - 150, 300, 300, 80, fill='blue')  # "Prisms"
    drawLabel("Prisms", app.width / 2, 340, size=20, align='center')

def drawShapeOptionsPage(app):
    if app.selectedCategory == "Standard Shapes":
        options = ["Pyramid", "Cube", "Hexagon", "Pentagon"]
    elif app.selectedCategory == "Prisms":
        options = ["Triangle", "Square", "Hexagon", "Pentagon"]

    drawLabel(f"Choose a {app.selectedCategory}", app.width / 2, 50, size=30, bold=True, align='center')

    # Display options as a centered list
    for i, option in enumerate(options):
        y = 150 + i * 60
        drawRect(app.width / 2 - 150, y - 30, 300, 50, fill='lightgray')
        drawLabel(option, app.width / 2, y, size=20, align='center')

def onMousePress(app, mouseX, mouseY):
    if app.currentPage == "welcome":
        if 200 <= mouseY <= 280:  # "Standard Shapes" button
            app.currentPage = "shapeOptions"
            app.selectedCategory = "Standard Shapes"
        elif 300 <= mouseY <= 380:  # "Prisms" button
            app.currentPage = "shapeOptions"
            app.selectedCategory = "Prisms"
    elif app.currentPage == "shapeOptions":
        # Check which shape option was selected
        options = ["Pyramid", "Cube", "Hexagon", "Pentagon"] if app.selectedCategory == "Standard Shapes" else ["Triangle", "Square", "Hexagon", "Pentagon"]
        for i, option in enumerate(options):
            y = 150 + i * 60
            if y - 30 <= mouseY <= y + 30:
                print(f"You selected: {option}")
                app.currentPage = "editor"  # Transition to editor page
                # You can extend this to pass selected shape data

def redrawAll(app):
    if app.currentPage == "welcome":
        drawWelcomePage(app)
    elif app.currentPage == "shapeOptions":
        drawShapeOptionsPage(app)
    elif app.currentPage == "editor":
        # Placeholder: Replace with your editor rendering
        drawLabel("Editor Mode", app.width / 2, app.height / 2, size=40, bold=True, align='center')

runApp(width=1000, height=600)

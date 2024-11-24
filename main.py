from welcome import *
from editor import *

def onAppStart(app):
    # Start with the welcome page
    app.currentPage = "welcome"
    onAppStartWelcome(app)  # Initialize welcome page settings
    onAppStartEditor(app)  # Preload editor settings if needed

def redrawAll(app):
    if app.currentPage == "welcome":
        redrawAllWelcome(app)  # Draw the welcome page
    elif app.currentPage == "editor":
        redrawAllEditor(app)  # Draw the editor page

def onMousePress(app, mouseX, mouseY):
    if app.currentPage == "welcome":
        onMousePressWelcome(app, mouseX, mouseY)
    elif app.currentPage == "editor":
        onMousePressEditor(app, mouseX, mouseY)

runApp(width=800, height=600)

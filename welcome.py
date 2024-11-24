from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.currentPage = "welcome"  # Default page is the welcome page
    app.selectedCategory = None

def drawWelcomePage(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill="lightBlue")

    # Title
    drawLabel("SHAPESHIFTER", app.width / 2, app.height / 3, size=50, bold=True, align="center", fill="black")

    # Subtitle
    drawLabel("What would you like to start with?", app.width / 2, app.height / 2, size=20, bold=False, align="center", fill="black")

    # Buttons
    buttonWidth = 150
    buttonHeight = 50
    buttonSpacing = 20
    centerX = app.width / 2
    centerY = app.height / 2 + 100

    # Shape Button
    drawRect(centerX - buttonWidth - buttonSpacing / 2, centerY - buttonHeight / 2, buttonWidth, buttonHeight, fill="skyblue")
    drawLabel("Shape", centerX - buttonWidth - buttonSpacing / 2 + buttonWidth / 2, centerY, size=20, bold=True, fill="black")

    # File Button
    drawRect(centerX + buttonSpacing / 2, centerY - buttonHeight / 2, buttonWidth, buttonHeight, fill="skyblue")
    drawLabel("File?", centerX + buttonSpacing / 2 + buttonWidth / 2, centerY, size=20, bold=True, fill="black")

def redrawAll(app):
    drawWelcomePage(app)

runApp(width=1000, height=600)

from cmu_graphics import *
from ShapeObject import ShapeObject

def onAppStart(app):
    """
    Initializes the app with a ShapeObject, flattens it, and maps the points to 2D.
    """
    # Create a cube-shaped object
    cube = ShapeObject((0, 0, 0), category=0, option=3)  # A cube (Square Prism)
    app.center_face = cube.flattenTo2D()  # Retrieve the center face after flattening

    # Use the first point of the center face as the hinge
    hinge_start = app.center_face.getUsedPoints()[0]
    app.points_2d = cube.map_3d_to_2d(app.center_face.getUsedPoints(), hinge_start)

def redrawAll(app):
    """
    Draws the mapped 2D points on the canvas and connects them with lines.
    """
    # Draw title and instructions
    drawLabel('Mapped 2D Points from 3D Center Face', 200, 20, size=16)

    # Draw each point as a circle
    for x, y in app.points_2d:
        drawCircle(x + 200, y + 200, 5, fill='red')  # Offset by 200, 200 to center on canvas

    # Connect the points to form a polygon
    if len(app.points_2d) > 1:
        for i in range(len(app.points_2d)):
            x1, y1 = app.points_2d[i]
            x2, y2 = app.points_2d[(i + 1) % len(app.points_2d)]  # Wrap around to first point
            drawLine(x1 + 200, y1 + 200, x2 + 200, y2 + 200, fill='black', lineWidth=2)

def main():
    runApp(width=400, height=400)

main()

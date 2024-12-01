from cmu_graphics import *
from ShapeObject import ShapeObject  # Ensure your ShapeObject and FaceObject are in this file

def onAppStart(app):
    """
    Initializes the app with a 3D shape, flattens its faces, and prepares the 2D points for display.
    """
    # Create a shape (e.g., a cube or a prism)
    app.shape = ShapeObject((0, 0, 0), category=1, option=0)  # Example: Square prism

    # Flatten the shape and get the center face
    app.shape.flattenTo2D()

def redrawAll(app):
    """
    Draws all the flattened points on the canvas.
    """
    # Draw the title
    drawLabel('Flattened 2D Faces', 200, 20, size=16)

    # Draw each flattened point
    for face in app.shape.faces2D:
        if face:
            print(face)
            print("order", len(face.order), face.order)
            print("use2D", len(face.used2D), face.used2D)
            print("Edges", len(face.getEdges()), face.getEdges())
            print("adjac", len(face.adjacencies), face.adjacencies)
            print()
            for p in face.used2D:
                if p:
                    x, y = p
                    drawCircle(x*50 + 200, y*50 + 200, 5, fill='red')  # Offset by (200, 200) to center on the canvas
            for edge in face.getEdges():
                drawLine(*[edge[0]], *viewPoints[edge[1]])

def main():
    runApp(width=400, height=400)

main()

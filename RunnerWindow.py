from ursina import *

app = Ursina()

# Define vertices for a cube
vertices = [
    [-1, -1, -1],  # Bottom-left-back  (0)
    [1, -1, -1],   # Bottom-right-back (1)
    [1, 1, -1],    # Top-right-back    (2)
    [-1, 1, -1],   # Top-left-back     (3)
    [-1, -1, 1],   # Bottom-left-front (4)
    [1, -1, 1],    # Bottom-right-front(5)
    [1, 1, 1],     # Top-right-front   (6)
    [-1, 1, 1],    # Top-left-front    (7)
]

# Define triangles for a cube
triangles = [
    [0, 1, 2, 3], [3,2,1,0],  # Back face
]

# Create the mesh with the cube vertices and triangles
mesh = Mesh(vertices=vertices, triangles=triangles, mode='triangle')

# Create the entity and set up the camera
entity = Entity(model=mesh)
EditorCamera()

app.run()

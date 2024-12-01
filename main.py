from cmu_graphics import *
from ShapeObject import ShapeObject  # Assuming your ShapeObject and FaceObject are in shape_object.py

def map_3d_to_2d(points_3d, hinge_edge, scale=100, offset=(200, 200)):
    hinge_start, hinge_end = hinge_edge
    hinge_vector = [hinge_end[i] - hinge_start[i] for i in range(3)]
    hinge_length = (sum(v**2 for v in hinge_vector))**0.5

    def project_point(point):
        point_vector = [point[i] - hinge_start[i] for i in range(3)]
        parallel_factor = sum(point_vector[i] * hinge_vector[i] for i in range(3)) / hinge_length**2
        parallel_proj = [parallel_factor * hinge_vector[i] for i in range(3)]
        perpendicular_vector = [point_vector[i] - parallel_proj[i] for i in range(3)]
        perpendicular_length = (sum(v**2 for v in perpendicular_vector))**0.5
        x_2d = parallel_factor * hinge_length
        y_2d = perpendicular_length if perpendicular_vector[2] >= 0 else -perpendicular_length
        return (x_2d * scale + offset[0], y_2d * scale + offset[1])

    return [project_point(point) for point in points_3d]

def tupToList(t):
    return [coord for point in t for coord in point]

def onAppStart(app):
    cube = ShapeObject((0, 0, 0), category=1, option=1)  # A cube
    app.center_face = cube.flattenTo2D()  # Retrieve the center face after flattening
    app.faces_to_draw = []  # List of all faces to draw
    app.visited = set()

    # Recursive function to flatten and collect faces
    def flatten_face(face, offset):
        if face in app.visited:
            return
        app.visited.add(face)

        # Select hinge edge and map the face
        hinge_edge = [face.getUsedPoints()[0], face.getUsedPoints()[1]]
        face_2d = map_3d_to_2d(face.getUsedPoints(), hinge_edge, scale=100, offset=offset)
        app.faces_to_draw.append(face_2d)

        # Recursively flatten adjacent faces
        for adj_face in face.adjacencies:
            if adj_face is not None and adj_face not in app.visited:
                flatten_face(adj_face, offset)

    # Start flattening from the center face
    flatten_face(app.center_face, offset=(200, 200))

def redrawAll(app):
    for face_2d in app.faces_to_draw:
        drawPolygon(*tupToList(face_2d), fill='cyan', border='black')

def main():
    runApp()

main()

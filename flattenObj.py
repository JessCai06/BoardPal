import math

class Shape2DObject:
    def __init__(self, faces):
        """
        Initialize a 2D shape object.

        :param faces: List of faces, where each face is a list of 2D points (tuples).
                      Example: [[(x1, y1), (x2, y2), (x3, y3)], ...]
        """
        self.faces = faces  # Each face is a list of (x, y) tuples
        self.points = self._extractUniquePoints()

    def _extractUniquePoints(self):
        """
        Extract unique points from the provided faces and assign them indices.

        :return: List of unique 2D points (tuples).
        """
        unique_points = {}
        current_index = 0

        for face in self.faces:
            for point in face:
                if point not in unique_points:
                    unique_points[point] = current_index
                    current_index += 1

        # Re-index the points in order
        return [point for point, _ in sorted(unique_points.items(), key=lambda item: item[1])]

    def getEdges(self):
        """
        Get all unique edges from the 2D shape.

        :return: List of unique edges as tuples of point indices.
        """
        edges = set()
        for face in self.faces:
            for i in range(len(face)):
                start = face[i]
                end = face[(i + 1) % len(face)]
                edges.add(tuple(sorted((start, end))))
        return list(edges)

    def translate(self, dx, dy):
        """
        Translate the entire 2D shape by (dx, dy).

        :param dx: Translation along the x-axis.
        :param dy: Translation along the y-axis.
        """
        self.points = [(x + dx, y + dy) for x, y in self.points]
        self.faces = [[(x + dx, y + dy) for x, y in face] for face in self.faces]

    def rotate(self, angle):
        """
        Rotate the shape around the origin by a given angle.

        :param angle: Angle in degrees.
        """
        radians = math.radians(angle)
        cos_theta, sin_theta = math.cos(radians), math.sin(radians)

        def rotate_point(x, y):
            return x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta

        self.points = [rotate_point(x, y) for x, y in self.points]
        self.faces = [[rotate_point(x, y) for x, y in face] for face in self.faces]

    def scale(self, factor):
        """
        Scale the shape by a given factor.

        :param factor: Scaling factor.
        """
        self.points = [(x * factor, y * factor) for x, y in self.points]
        self.faces = [[(x * factor, y * factor) for x, y in face] for face in self.faces]

    def __str__(self):
        """
        String representation of the 2D shape.
        """
        face_strs = ["Face: " + " -> ".join(f"({x}, {y})" for x, y in face) for face in self.faces]
        return "\n".join(face_strs)

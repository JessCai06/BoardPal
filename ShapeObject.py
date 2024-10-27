from FaceObject import FaceObject

class ShapeObject:
    def __init__(self, posx, posy, points, order):
        self.x = posx
        self.y = posy
        self.points = points
        self.faces = []
        for face in order:
           self.faces.append(face)

        
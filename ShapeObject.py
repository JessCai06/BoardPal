from typing import Any
from FaceObject import FaceObject

class ShapeObject:
    def __init__(self, pos, points, order):
        self.x, self.y, self.z = pos
        self.points = []
        for coord in points:
            temp = (coord[0]+self.x, coord[1]+self.y,coord[2]+self.z)
            self.points.append(temp)
        self.faces = []
        for i in range(len(order)):
            face = order[i]
            tempFace = FaceObject(i,self.points,face)
            self.faces.append(tempFace)


        
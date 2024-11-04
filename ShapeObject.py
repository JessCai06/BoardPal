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

    def getFaces(self, indexInPoints):
        if indexInPoints < 0:
            return -1
        facesThisPointIsIn = []
        for face in self.faces:
            if indexInPoints in face.order:
                facesThisPointIsIn.append(face.index)
        return facesThisPointIsIn

    def replacePoint(self, indexInPoints, newPoint):
        self.points[indexInPoints] = newPoint
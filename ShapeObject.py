from typing import Any
from FaceObject import FaceObject

class ShapeObject:
    def __init__(self, pos, points, order):
        self.x, self.y, self.z = pos
        self.points = points
        self.faces = []
        for i in range(len(order)):
            print(i)
            face = order[i]
            tempFace = FaceObject(i,self.points,face)
            self.faces.append(tempFace)



    

        
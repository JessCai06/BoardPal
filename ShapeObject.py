import numpy as np
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

    def getFaces(self, pointIndex):
        if pointIndex < 0:
            return -1
        facesThisPointIsIn = []
        for face in self.faces:
            if pointIndex in face.order:
                facesThisPointIsIn.append(face.index)
        return facesThisPointIsIn
    
    def mergeFaces(self, coplanarFaces):
        merged = coplanarFaces.pop()
        mergeOrder = set(merged.order)
        for face in coplanarFaces:
            for i in face.order:
                mergeOrder.add(i)
            self.faces.remove(face)
        for i in range(len(self.faces)):
            face.index = i
        self.faces.append(FaceObject(len(self.faces), self.points, list(mergeOrder)))

    def user_change_this_Point (self, pointIndex, newPoint):
        oldFaces = self.getFaces(pointIndex)
        coplanarFaces = []
        # we want to see which faces we need to change
        for index in oldFaces:
            print("\t\told faces", oldFaces)
            faceobj = self.faces[index]

            if not faceobj.isCoplanar(newPoint):
                faceobj.order.remove(pointIndex)
                remnantPoints = faceobj.closest2Points(newPoint)
                newOrder = [pointIndex]+remnantPoints
                print("new ORDER", newOrder)
                newFace = FaceObject (len(self.faces),self.points,newOrder)
                self.faces.append(newFace)
            # else:
            #     # if the face object and the new point is coplanar:
            #     # faceobj.append(pointIndex)
            #     coplanarFaces.append(faceobj)
        if len(coplanarFaces)> 1:
            self.mergeFaces(coplanarFaces)
                
        self.points[pointIndex] = newPoint

# normal testing cases
baseSquare = [(-1, -1, 0), (-1, 1, 0), (1, 1, 0), (1, -1, 0), 
                # 4           5           6           7
                (-1, -1, 2), (-1, 1, 2), (1, 1, 2), (1, -1, 2)]
order = [[0,1,2,3],
            [0,1,5,4],
            [2,3,7,6],
            [0,3,7,4],
            [1,2,6,5],
            [4,5,6,7]]
cube = ShapeObject((0,0,0), baseSquare, order)
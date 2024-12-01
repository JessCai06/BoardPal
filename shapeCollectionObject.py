from ShapeObject import ShapeObject
from FaceObject import FaceObject
import math
import random
import copy

class shapeCollectionObject:
    """
    this class handles merging shapes & other shenanigans
    NOTE: merge only works when there are 2 shapes in this collection.
    you may only add a shape when you have 1 or less shapes
    """
    def __init__(self):
        self.shapes = []

    def getNewSpawnPoint(self,shape):
        if len(self.shapes) == 0 :
            return (0,0,0)
        elif len(self.shapes) == 1:
            return (0, 0, int(self.shapes[0].calculateRadius() + self.shapes[0].z + shape.calculateRadius())) 
        return (-1,-1,-1)
    
    def canMerge(self):
        if len(self.shapes) <= 1:
            return False
        shared = self.getSharedFaces()
        print("can merge ", len(shared) > 0)
        return len(shared) > 0

    def mergeAll(self):
        if not self.canMerge():
            print("ERROR: can't merge")
            return 
        self.mergeShape()
        self.shapes.pop()
        for shape in self.shapes:
            print(shape)

    def getSharedFaces(self):
        shared = set()
        for face1 in self.shapes[0].faces:
            for face2 in self.shapes[1].faces:
                if face1 != None and face1 == face2:
                    print(len(face1.order), " ---- ",len(face2.order))
                    print(face1 , " and ", face2, " are the same")
                    shared.add(face1)
        return shared

    def getAllPoints(self):
        temp = copy.deepcopy(self.shapes[0].points)
        for p in self.shapes[1].points:
            if p not in temp:
                temp.append(p)
        return temp

    def mergeShape(self):
        shared = self.getSharedFaces()
        if len(shared) == 0:
            return 
        print("shared faces", shared)
        print("original length of shape 0:", len(self.shapes[0].faces))
        print("original length of shape 1:", len(self.shapes[1].faces))
        for face in shared:
            self.shapes[0].faces.remove(face)
            self.shapes[1].faces.remove(face)
        # we want all the deduplicated points
        allPoints = self.getAllPoints()
        self.shapes[0].points=allPoints
        print(len(allPoints), allPoints)
        maxindex = self.findMaxIndex(self.shapes[0].faces)
        for i in range(len(self.shapes[1].faces)):
            oldFace = self.shapes[1].faces[i]
            newfaceIndex = maxindex + i+1
            newOrder = []
            actualPoints = []
            for order in oldFace.order:
                actualPoints.append(self.shapes[1].points[order])
            for point in actualPoints:
                newOrder.append(allPoints.index(point))
            newFace = FaceObject(newfaceIndex, allPoints,newOrder)
            self.shapes[0].faces.append(newFace)
        
    def findMaxIndex (self, lis):
        maxx = -1
        for f in lis:
            if f.index > maxx:
                maxx = f.index
        return maxx

    def removeShape(self, index):
        if len(self.shapes) == 0 or index > len(self.shapes):
            return
        if len(self.shapes) == 1:
            self.shapes.pop()
        else:
            self.shapes.pop(index)        

    def addShape(self, shape):
        if len(self.shapes) == 0 :
            self.shapes.append(shape)
        elif len(self.shapes) < 2:
            newSpawn = self.getNewSpawnPoint(shape)
            shape.moveCenter(newSpawn)
            self.shapes.append(shape)


collection = shapeCollectionObject()
s1 = ShapeObject((0,0,0), 1,0)
collection.addShape(s1)
s2 = ShapeObject((0,0,4), 1,0)
collection.addShape(s2)
print(collection.canMerge())
collection.mergeAll()
print(collection.shapes[0])
        
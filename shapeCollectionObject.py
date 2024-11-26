from ShapeObject import ShapeObject
from FaceObject import FaceObject
import math
import random

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
        elif len(self.shapes) < 2:
            newSpawn = (0, 0, int(self.shapes[0].calculateRadius() + shape.calculateRadius())) 
            return newSpawn
        return (-1,-1,-1)
    
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
        
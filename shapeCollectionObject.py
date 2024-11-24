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

    def addShape(self, shape):
        if len(self.shapes) == 0 :
            self.shapes.append(shape)
        elif len(self.shapes) < 2:
            newSpawn = (0, 0, self.shapes[0].calculateRadius) 
            shape.moveCenter(newSpawn)
            self.shapes.append(shape)
        
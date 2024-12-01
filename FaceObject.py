import random 

class FaceObject:
    """
    this class represents the pure logical structure of a face, or plane
    of a shape. The purpose of this class: 1) manipulate the points/verticies
    of the shape corresponding to user interaction 2) be able to connect logic
    to the graphic output of ursina.
    """
    def __init__(self, i, points, order):
        """
        points is very important and delicate: this will be passed when creating a 
        ShapeObject. 
        1) **it's very important that it is an ALIAS to the original points 
        in initiating the points object so that every time the shape is offset/ moved, 
        the FaceObject will move with it.
        2) **it is also important to note that faceobject should never make changes to
        the points list, changes should only be made in shapeobject - since this is a 
        larger collection of points of the WHOLE SHAPE instead of only the face
        order: shows the points that this faceobject will use, and the order it
        will be read in from. 
        len(order) == the shape type (ie. 3 triangle, 4 rectangle, 5 etc)
        """
        self.index = i
        self.points = points
        self.order = order
        r, g, b= random.randint(0,255), random.randint(0,255),random.randint(0,255)
        self.color = (r,g,b)
        self.adjacencies = []

    def getEdges(self):
        edges = []
        for i in range(len(self.order)-1):
            line = (self.order[i], self.order[i+1])
            edges.append(line)
        edges.append((self.order[0], self.order[-1]))
        return edges
    
    def getUsedPoints(self):
        temp = []
        for e in self.order:
            temp.append(self.points[e])
        return temp
    
    def getEdgePairs(self):
        edge = self.getEdges()
        temp = []
        for e in edge:
            s = (min(*e), max(*e))
            temp.append(s)
        return temp

    def getSharedEdges(self, other):
        mine = self.getEdgePairs()
        yours = other.getEdgePairs()
        shared = []
        for i, pair1 in enumerate(mine):
            for j, pair2 in enumerate(yours):
                if pair1 == pair2:
                    shared.append((i,j))
        return shared

    def __eq__(self, other):
        if other is None or len(self.order) != len(other.order):
            return False
        return set(self.getUsedPoints()) == set(other.getUsedPoints())

    def __repr__(self):
        edges_str = ', '.join([f"({self.points[edge[0]]}  - {self.points[edge[1]]})" for edge in self.getEdges()])
        return f"FaceObject >>>> index={self.index}, order={self.order}, edges=[{edges_str}])"
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(self.getUsedPoints())))

    
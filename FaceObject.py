
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

    def getEdges(self):
        edges = []
        for i in range(len(self.order)):
            edges.append(tuple(self.order[i], self.order[i+1]))
            print(edges)
        print("rest of order", self.order)
        edges.append(tuple(self.order[0], self.order[-1]))
        return edges

    def getEdgePoints(self):
        edges = self.getEdges()
        edgePoints = []
        for edge in edges:
            edgePoints.append(self.points[edge[0]],self.points[edge[1]])
        return edgePoints

    def __eq__(self, other):
        #if they have the same number of points (quad == triangle)
        if len(self.order) != len(self.order):
            return False
        #if all of their points are the same
        for edge in self.getEdgePoints():
            if edge not in other.getEdgePoints():
                return False
        return True

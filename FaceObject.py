
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
        for i in range(len(self.order)-1):
            line = (self.order[i], self.order[i+1])
            edges.append(line)
        edges.append((self.order[0], self.order[-1]))
        return edges
    
    def distance3D (self,p1,p2):
        return sum((p1[i] - p2[i])**2 for i in range(3))**0.5

    def closest2Points(self, point):
        face_points = [self.points[i] for i in self.order]
        distances = []
        
        for fp in face_points:
            dist = self.distance3D(fp, point)
            distances.append((fp, dist))

        for i in range(len(distances)):
            for j in range(i + 1, len(distances)):
                if distances[i][1] > distances[j][1]:
                    distances[i], distances[j] = distances[j], distances[i]
        a = self.points.index(distances[0][0])
        b = self.points.index(distances[1][0])
        print("closest two points", a,b)
        return [a,b]


    # references: I am using the formula given by this website https://www.cuemath.com/geometry/coplanar/
    def isCoplanar(self, point):
        """
        this checks if the last point is co-planar with the rest of the points in the faceobject
        """
        #this is very unlikely but here - we assume there are only two points
        if len(self.order) <= 2:
            return True 
        
        points = [self.points[i] for i in self.order]
        # since we only change one of the points at one time, assume that the all previous points are coplanar.
        p0, p1, p2 = points[len(points)-3:]

        v1 = [p1[i] - p0[i] for i in range(3)]
        v2 = [p2[i] - p0[i] for i in range(3)]
        v3 = [point[i] - p0[i] for i in range(3)]

        normal = [
        v1[1] * v2[2] - v1[2] * v2[1],  #  x
        v1[2] * v2[0]- v1[0] * v2[2],  # y
        v1[0] * v2[1] - v1[1] * v2[0],  # z
            ]
        #print(normal)
        result = 0
        for i in range(3):
            result += normal[i] * v3[i]

        return result == 0
    
    def __eq__(self, other):
        #if they have the same number of points (quad == triangle)
        if len(self.order) != len(self.order):
            return False
        #if all of their points are the same
        for edge in self.getEdgePoints():
            if edge not in other.getEdgePoints():
                return False
        return True

    def __str__(self):
        edges_str = ', '.join([f"({edge[0]}, {edge[1]})" for edge in self.getEdges()])
        return f"FaceObject(index={self.index}, order={self.order}, edges=[{edges_str}])"

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

    def getFaces(self, indexInPoints):
        if indexInPoints < 0:
            return -1
        facesThisPointIsIn = []
        for face in self.faces:
            if indexInPoints in face.order:
                facesThisPointIsIn.append(face.index)
        return facesThisPointIsIn

# references: I am using the formula given by this website https://www.cuemath.com/geometry/coplanar/
    def isCoplanar(self, points):
        """
        this checks if the last point of the list
        is co-planar with the rest of the points in the faceobject
        """
        if len(points) < 4:
            return True  
        
        # since we only change one of the points at one time, assume that the all previous points are coplanar.
        p0 = points[0]
        p1 = points[1]
        p2 = points[2]
        p3 = points[3]

        v1 = self.listDifference(p1,p0)
        v2 = self.listDifference(p2,p0)
        #the last list difference
        v3 = self.listDifference(p3,p0)

        normal = self.cross(v1, v2)

        product = 0
        for i in range(len(normal)):
            product += normal[i] * v3[i]
        return product == 0
    
    def cross(self, v1, v2):
        #LIST HAS TO HAVE LEN OF 3
        return [
            v1[1] * v2[2] - v1[2] * v2[1],  
            v1[2] * v2[0] - v1[0] * v2[2],  
            v1[0] * v2[1] - v1[1] * v2[0]   
        ]

    def listDifference(self, a, b):
        empty = []
        for i in range(3):
            empty.append(a[i]-b[i])
        return empty

    def rearrangeFaces(self):
        new_faces = []
        for face in self.faces:
            # Gather the points for this face
            face_points = [self.points[i] for i in face.order]

            if self.isCoplanar(face_points):
                new_faces.append(face)  
            else:
                for i in range(2, len(face.order)):
                    triangle_order = [face.order[0], face.order[i-1], face.order[i]]
                    new_faces.append(FaceObject(face.index, self.points, triangle_order))
        self.faces = new_faces 
        print(self.faces) 

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
cube.rearrangeFaces()

arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])


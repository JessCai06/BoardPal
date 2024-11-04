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

    def isCoplanar(self, points):
        # Helper method to check coplanarity of four points in 3D
        if len(points) < 4:
            return True  # Triangular face is always coplanar
        p0, p1, p2, p3 = points[:4]

        # Vectors for cross product
        v1 = np.array(p1) - np.array(p0)
        v2 = np.array(p2) - np.array(p0)
        v3 = np.array(p3) - np.array(p0)

        # Compute normal vector via cross product
        normal = np.cross(v1, v2)
        return np.dot(normal, v3) == 0

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
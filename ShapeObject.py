from FaceObject import FaceObject
import math

class ShapeObject:
    def __init__(self, pos, category, option):
        self.x, self.y, self.z = pos
        shapie_dict = self.generateShapeData(category, option)
        points = shapie_dict["points"]
        order = shapie_dict["order"]
        self.points = []
        for coord in points:
            print(coord)
            temp = (coord[0]+self.x, coord[1]+self.y,coord[2]+self.z)
            self.points.append(temp)
        self.faces = []
        for i in range(len(order)):
            face = order[i]
            tempFace = FaceObject(i,self.points,face)
            self.faces.append(tempFace)

    def getFaces(self, indexInPoints):
        facesThisPointIsIn = []
        for face in self.faces:
            if indexInPoints in face.order:
                facesThisPointIsIn.append(face.index)
        return facesThisPointIsIn
    
    def find_midpoint(coord1, coord2):
        if len(coord1) != len(coord2):
            raise ValueError("Coordinates must have the same number of dimensions")
        return tuple((c1 + c2) / 2 for c1, c2 in zip(coord1, coord2))

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

    def generateShapeData(self, category, option):
        """
        3D points and face
        param
            category (str): "standard" or "prism"
            option (int): 0 (triangle/pyramid), 1 (cube/square), 2 (hex), 3 (pent)
        """
        print(category)
        #STANDARD
        if category == 0:
            # Standard shapes: Pyramid, Cube, Hexagonal Prism, Pentagonal Prism
            if option == 0: 
                points = [
                    (0, 0, 3),  # Apex
                    (-1, -1, 0), (1, -1, 0), (0, 1, 0)  # Base vertices
                ]
                order = [
                    [0, 1, 2],  # Apex to base side 1
                    [0, 2, 3],  # Apex to base side 2
                    [0, 3, 1],  # Apex to base side 3
                    [1, 2, 3]   # Base face
                ]
            elif option == 1:  # Cube
                points = [
                    (-2, -2, -2), (-2, 2, -2), (2, 2, -2), (2, -2, -2),
                    (-2, -2, 2), (-2, 2, 2), (2, 2, 2), (2, -2, 2)
                ]
                order = [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # Top and bottom faces
                    [0, 1, 5, 4], [1, 2, 6, 5],  # Side faces
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ]
            elif option == 2:  # Hexagonal Prism
                # Base hexagon (z = -2), mirrored at z = 2
                points = [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), -2) for i in range(6)
                ] + [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), 2) for i in range(6)
                ]
                order = [
                    [0, 1, 2, 3, 4, 5],  # Bottom face
                    [6, 7, 8, 9, 10, 11],  # Top face
                ] + [[i, (i + 1) % 6, (i + 1) % 6 + 6, i + 6] for i in range(6)]  # Side faces
            elif option == 3:  # Pentagonal Prism
                # Base pentagon (z = -2), mirrored at z = 2
                points = [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), -2) for i in range(5)
                ] + [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), 2) for i in range(5)
                ]
                order = [
                    [0, 1, 2, 3, 4],  # Bottom face
                    [5, 6, 7, 8, 9],  # Top face
                ] + [[i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5] for i in range(5)]  
        #PRISM
        elif category == 1:
            # Prisms: Triangular, Square, Hexagonal, Pentagonal
            if option == 0:  # Triangular Prism
                points = [
                    (-1, -1, -2), (1, -1, -2), (0, 1, -2),  # Base 1 (z = -2)
                    (-1, -1, 2), (1, -1, 2), (0, 1, 2)  # Base 2 (z = 2)
                ]
                order = [
                    [0, 1, 2], [3, 4, 5],  # Bottom and top faces
                    [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]  # Side faces
                ]
            elif option == 1:  # Square Prism
                points = [
                    (-1, -1, -2), (1, -1, -2), (1, 1, -2), (-1, 1, -2),  # Base 1 (z = -2)
                    (-1, -1, 2), (1, -1, 2), (1, 1, 2), (-1, 1, 2)  # Base 2 (z = 2)
                ]
                order = [
                    [0, 1, 2, 3], [4, 5, 6, 7],  # Bottom and top faces
                    [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]  # Side faces
                ]
            elif option == 2:  # Hexagonal Prism (same as standard)
                points = [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), -2) for i in range(6)
                ] + [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), 2) for i in range(6)
                ]
                order = [
                    [0, 1, 2, 3, 4, 5],  # Bottom face
                    [6, 7, 8, 9, 10, 11],  # Top face
                ] + [[i, (i + 1) % 6, (i + 1) % 6 + 6, i + 6] for i in range(6)]  # Side faces
            elif option == 3:  # Pentagonal Prism (same as standard)
                points = [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), -2) for i in range(5)
                ] + [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), 2) for i in range(5)
                ]
                order = [
                    [0, 1, 2, 3, 4],  # Bottom face
                    [5, 6, 7, 8, 9],  # Top face
                ] + [[i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5] for i in range(5)]  # Side faces
        else:
            raise ValueError("Invalid category")

        return {"points": points, "order": order}



cube = ShapeObject((0,0,0), 0,1)
cube.rearrangeFaces()



from FaceObject import FaceObject
from flattenObj import Shape2DObject
import math
import copy

class ShapeObject:
    def __init__(self, pos, category, option):
        self.x, self.y, self.z = pos
        shape_data = copy.deepcopy(self.generateShapeData(category, option))
        self.points = [(x + self.x, y + self.y, z + self.z) for x, y, z in shape_data["points"]]
        self.faces = [
            FaceObject(index, self.points, face)
            for index, face in enumerate(shape_data["order"])
        ]
        self.moveCenter(pos)

    def __repr__(self):
        return f"center at {self.x, self.y, self.z} --- and points at {self.points}"

    def moveCenter(self, newPos):
        offsetX, offsetY, offsetZ = newPos[0] - self.x, newPos[1] - self.y, newPos[2] - self.z
        self.x, self.y, self.z = newPos
        tempPoints = []
        for point in self.points:
            x, y, z = point
            tempPoints.append((x + offsetX, y + offsetY, z + offsetZ))
        self.points = tempPoints
        for face in self.faces:
            face.points = tempPoints

    def getFacesAdjacentToPoint(self, indexInPoints):
        return [face.index for face in self.faces if indexInPoints in face.order]
    
    def getEdges(self):
        edgeSet = set()  
        for face in self.faces:
            for start_idx, end_idx in face.getEdges():
                start = self.points[start_idx]
                end = self.points[end_idx]
                edge = tuple(sorted((start, end)))  
                edgeSet.add(edge)

        return list(edgeSet)  

    def isCoplanar(self, points):
        if len(points) < 4:
            return True
        v1 = self.vectorDifference(points[1], points[0])
        v2 = self.vectorDifference(points[2], points[0])
        v3 = self.vectorDifference(points[3], points[0])
        normal = self.crossProduct(v1, v2)
        return sum(normal[i] * v3[i] for i in range(3)) == 0

    def vectorDifference(self, a, b):
        return [a[i] - b[i] for i in range(3)]

    def crossProduct(self, v1, v2):
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        ]

    def calculateRadius(self):
        return max(
            math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2 + (z - self.z) ** 2)
            for x, y, z in self.points
        )

    def rearrangeFaces(self):
        new_faces = []
        for face in self.faces:
            face_points = [self.points[i] for i in face.order]
            if self.isCoplanar(face_points):
                new_faces.append(face)
            else:
                for i in range(2, len(face.order)):
                    new_faces.append(FaceObject(
                        face.index, self.points, [face.order[0], face.order[i - 1], face.order[i]]
                    ))
        self.faces = new_faces        

    def flattenTo2D(self):
        visited_faces = set()
        flattened_faces = []
        stack = [(self.faces[0], (0, 0))]
    
    def bloom(self, hi):
        pass

    def generateShapeData(self, category, option):

        """
        3D points and face
        param
            category (str): "standard" or "prism"
            option (int): 0 (triangle/pyramid), 1 (cube/square), 2 (hex), 3 (pent)
        """
        #STANDARD
        if category == 0:
            if option == 0: 
                points = [
                    (0, 0, 3),  
                    (-1, -1, 0), (1, -1, 0), (0, 1, 0)  
                ]
                order = [
                    [0, 1, 2],  
                    [0, 2, 3],  
                    [0, 3, 1],  
                    [1, 2, 3]   
                ]
            elif option == 1:  # Cube
                points = [
                    (-2, -2, -2), (-2, 2, -2), (2, 2, -2), (2, -2, -2),
                    (-2, -2, 2), (-2, 2, 2), (2, 2, 2), (2, -2, 2)
                ]
                order = [
                    [0, 1, 2, 3], [4, 5, 6, 7],  
                    [0, 1, 5, 4], [1, 2, 6, 5],  
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ]
            elif option == 2:  
                points = [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), -2) for i in range(6)
                ] + [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), 2) for i in range(6)
                ]
                order = [
                    [0, 1, 2, 3, 4, 5], 
                    [6, 7, 8, 9, 10, 11], 
                ] + [[i, (i + 1) % 6, (i + 1) % 6 + 6, i + 6] for i in range(6)]  
            elif option == 3:  
                points = [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), -2) for i in range(5)
                ] + [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), 2) for i in range(5)
                ]
                order = [
                    [0, 1, 2, 3, 4], 
                    [5, 6, 7, 8, 9],  
                ] + [[i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5] for i in range(5)]  
        #PRISM
        elif category == 1:
            if option == 0:  
                points = [
                    (-1, -1, -2), (1, -1, -2), (0, 1, -2),  
                    (-1, -1, 2), (1, -1, 2), (0, 1, 2)  
                ]
                order = [
                    [0, 1, 2], [3, 4, 5],  
                    [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]  
                ]
            elif option == 1:  # Square Prism
                points = [
                    (-1, -1, -2), (1, -1, -2), (1, 1, -2), (-1, 1, -2),  
                    (-1, -1, 2), (1, -1, 2), (1, 1, 2), (-1, 1, 2) 
                ]
                order = [
                    [0, 1, 2, 3], [4, 5, 6, 7],  
                    [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]  
                ]
            elif option == 2:  
                points = [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), -2) for i in range(6)
                ] + [
                    (math.cos(i * math.pi / 3), math.sin(i * math.pi / 3), 2) for i in range(6)
                ]
                order = [
                    [0, 1, 2, 3, 4, 5],  
                    [6, 7, 8, 9, 10, 11],  
                ] + [[i, (i + 1) % 6, (i + 1) % 6 + 6, i + 6] for i in range(6)]  
            elif option == 3:  # Pentagonal Prism (same as standard)
                points = [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), -2) for i in range(5)
                ] + [
                    (math.cos(i * 2 * math.pi / 5), math.sin(i * 2 * math.pi / 5), 2) for i in range(5)
                ]
                order = [
                    [0, 1, 2, 3, 4],  
                    [5, 6, 7, 8, 9],  
                ] + [[i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5] for i in range(5)] 
        else:
            raise ValueError("Invalid category")

        return {"points": points, "order": order}
    

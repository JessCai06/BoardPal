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

        ##################
        self.center2D = None
        self.faces2D = copy.deepcopy(self.faces)

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
        """
        this is what happens when you move a point and some of the"""
        new_faces = []
        for face in self.faces:
            face_points = [self.points[i] for i in face.order]
            if self.isCoplanar(face_points):
                new_faces.append(face)
            else:
                for i in range(2, len(face.order)):
                    new_faces.append(FaceObject(len(self.faces), self.points, [face.order[0], face.order[i - 1], face.order[i]]))
        self.faces = new_faces        

#um so, if its a full 3d shape, then every single edge of any face should be adjacent to some other face
#
    def flattenTo2D(self):
        stack = copy.deepcopy(self.faces)
        self.faces2D = []
        center = stack.pop()
        #A,B is the reference edge you are using
        a,b = (center.getEdges()[0])

        #A is origin (0,0) B is (distance AB, 0)
        A, B = self.points[a], self.points[b]
        for i, order in enumerate(center.order):
            C = self.points[order]
            center.used2D[i] = (self.constructFlattenedC(A,B,C))
        print(center.used2D)
        self.bloom(center, stack)
        self.center2D = center
        self.faces2D.append(center)

    def bloom(self, center, stack):
        # depending on the number of edges you have, you would have pointers to the "next node" of the 
        if len(stack) == 0:
            return
        if center == None:
            return
        print()
        print(" center: ", center)
        edgePairs = center.getEdges()
        adjacencies = [None] * len(edgePairs)

        # Process each face in the stack
        i = 0
        while i < len(stack):
            face = stack[i]
            print(face)
            # this shared thing is a dictionary that gives the shared index of the edge 
            # key = index of edge in center, value = index of edge in the other face
            center.getSharedEdges(face)
            shared_edge = center.getSharedEdges(face)
            print("SHARED EDGES", shared_edge)
            if len (shared_edge) > 0:
                # we want to build a parallel list that corresponds another face object with this particular edge of the face.
                for centerEidx, pair1 in shared_edge:
                    print(centerEidx, pair1)
                    adjacencies[centerEidx] = face 
                    a = center.used2D[center.order.index(pair1[0])] 
                    b = center.used2D[center.order.index(pair1[1])] 
                    # we need to look through the list. the shared edge is the hinge - WE CAN ASSUME THAT THE 
                    #NEEDED PAIRS ALREADY EXIST IN THE DICTIONARY BECAUSE IT'S SHARED WITH THE CENTER, AND ALL
                    #POINTS IN THE CENTER IS DEFINED ALREADY
                    for j, order in enumerate(face.order):
                        c = face.points[order]
                        bigC = self.constructFlattenedHinge(face.points[pair1[0]], face.points[pair1[1]],c,a,b)
                        face.used2D[j] = bigC

                stack.pop(i)  
            else:
                i += 1  
        center.adjacencies = adjacencies
        for face in adjacencies:
            self.bloom(face, stack)  
            self.faces2D.append(face)

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
    
    def __repr__(self):
        points_str = ', '.join([f"({x}, {y}, {z})" for x, y, z in self.points])
        faces_str = ', '.join([f"{face.index}" for face in self.faces])
        return (
            f"ShapeObject:\n"
            f"  Faces: [{faces_str}]"
        )

    def calculate_3d_distance(self, point1, point2):
        x1, y1, z1 = point1
        x2, y2, z2 = point2

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        return math.sqrt(dx**2 + dy**2 + dz**2)

    def calculate_angle_CAB(self,A, B, C):
        # Vectors AB and AC
        vector_AB = [B[i] - A[i] for i in range(3)]
        vector_AC = [C[i] - A[i] for i in range(3)]

        # Dot product of AB and AC
        dot_product = sum(vector_AB[i] * vector_AC[i] for i in range(3))

        # Magnitudes of AB and AC
        magnitude_AB = math.sqrt(sum(v**2 for v in vector_AB))
        magnitude_AC = math.sqrt(sum(v**2 for v in vector_AC))

        # Avoid division by zero
        if magnitude_AB == 0 or magnitude_AC == 0:
            raise ValueError("One or both vectors have zero magnitude, cannot compute angle.")

        # Cosine of the angle CAB
        cos_angle = dot_product / (magnitude_AB * magnitude_AC)
        cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to avoid domain errors in acos

        # Calculate the angle in radians
        angle_CAB = math.acos(cos_angle)

        return angle_CAB

    def constructFlattenedHinge(self,A,B,C, a, b):
        """
        precondition: ABC are all 3D coordinates, hinge (2d coordinates) is a,b which is the hinge you want to base C off of
        """
        if C == A:
            return a
        if C == B:
            return b
        #1) calculate distance from A to C
        distance = self.calculate_3d_distance(A,C)
        #2) theta CAB
        theta = self.calculate_angle_CAB(A,B,C)
        #3) construct the new 2D point from A with distance
        x = round(distance * math.cos(theta)+a[0])
        y = round(distance * math.sin(theta)+a[1])
        print(x,y)
        return (x,y)

    def constructFlattenedC(self,A,B,C):
        """
        precondition: ABC are all 3D coordinates
        """
        if C == A:
            return (0,0)
        if C==B:
            return (round(self.calculate_3d_distance(A,B)),0)
        #1) calculate distance from A to C
        distance = self.calculate_3d_distance(A,C)
        #2) theta CAB
        
        theta = self.calculate_angle_CAB(A,B,C)
        #3) construct the new 2D point from A with distance
        x = round(distance * math.cos(theta))
        y = round(distance * math.sin(theta))
        return (x,y)


def test_flatten_to_2d():
    """
    Tests the flattenTo2D method by printing the center face and its adjacencies,
    as well as verifying the 2D mapped points of the center face.
    """
    # Create a cube-shaped object
    cube = ShapeObject((0, 0, 0), category=0, option=1)  # A cube (Square Prism)

    print("\nInitial Cube Faces:")
    for face in cube.faces:
        print(face)

    print("\nFlattening the cube to 2D")
    center_face = cube.flattenTo2D()

    print("\nCenter Face After Flattening:")
    print(cube.center2D, cube.center2D.adjacencies)

    print("\nAdjacency Relationships (Spiraling Out):")
    for face in cube.faces2D:
        if face:
            print(f"Face {face.index}:")
            print(face.adjacencies)
            for i, adjacent_face in enumerate(face.adjacencies):
                if adjacent_face is None:
                    print(f" Edge {i}: No adjacency")
                else:
                    print(f" Edge {i}: Adjacent to Face {adjacent_face.index}")
# Run the test
if __name__ == "__main__":
    test_flatten_to_2d()


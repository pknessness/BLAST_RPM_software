import math
import pygame

t = 0
timeFrame = 10
manualStop = -1
axes = [(1,0,0),(0,1,0),(0,0,1)]

points = []

def generateAngle():
    global t
    x = math.sin(t/5 - 10)*2 + 2.5
    #y = math.sin(3*t + 19) * 360 + 180
    z = math.sin(t/7 + 11)*2 + 2.5
    x = 0
    y = 0
    #z = 120/(50*t+1)
    result = (x, y, z)
    return result

def project(vector, w, h, fov, distance):
    factor = math.atan(fov / 2 * math.pi / 180) / (distance + vector.z)
    x = vector.x * factor * w + w / 2
    y = -vector.y * factor * w + h / 2
    return pygame.math.Vector3(x, y, vector.z)

def rotate_vertices(vertices, angle, axis):
    #print(f"angle: {angle}, axis {axis}")
    return [v.rotate(angle, axis) for v in vertices]
def scale_vertices(vertices, s):
    return [pygame.math.Vector3(v[0]*s[0], v[1]*s[1], v[2]*s[2]) for v in vertices]
def translate_vertices(vertices, t):
    return [v + pygame.math.Vector3(t) for v in vertices]
def project_vertices(vertices, w, h, fov, distance):
    return [project(v, w, h, fov, distance) for v in vertices]

class Mesh():

    def __init__(self, vertices, faces):
        self.__vertices = [pygame.math.Vector3(v) for v in vertices]
        self.__faces = faces

    def rotate(self, angle, axis):
        self.__vertices = rotate_vertices(self.__vertices, angle, axis)
    def scale(self, s):
        self.__vertices = scale_vertices(self.__vertices, s)
    def translate(self, t):
        self.__vertices = translate_vertices(self.__vertices, t)

    def calculate_average_z(self, vertices):
        return [(i, sum([vertices[j].z for j in f]) / len(f)) for i, f in enumerate(self.__faces)]

    def get_face(self, index):
        return self.__faces[index]
    def get_vertices(self):
        return self.__vertices

    def create_polygon(self, face, vertices):
        return [(vertices[i].x, vertices[i].y) for i in [*face, face[0]]]
       
class Vector():

    def __init__(self, root, point):
        self.root = root
        self.point = point
        self.__line = [(0, 1)]
        

    def rotate(self, angle, axis):
        self.root, self.point = rotate_vertices([self.root, self.point], angle, axis)

    def rotateOnRoot(self, angle, axis):
        #x, self.point = rotate_vertices([self.root, self.point], angle, axis)
        print(type(self.root))
        #displace = [self.root.x,self.root.y,self.root.z]
        truePoint = self.point - self.root
        self.point = truePoint.rotate(angle,axis) + self.root
        return self
    def scale(self, s):
        self.root, self.point = scale_vertices([self.root, self.point], s)
    def translate(self, t):
        self.root, self.point = translate_vertices([self.root, self.point], t)

    def calculate_average_z(self, vertices):
        return [(i, sum([vertices[j].z for j in f]) / len(f)) for i, f in enumerate(self.__line)]

    def length(self):
        return math.sqrt((self.root.x - self.point.x)**2 + (self.root.y - self.point.y)**2 + (self.root.z - self.point.z)**2)

    def get_line(self):
        return self.__line[0]
    def get_vertices(self):
        return[self.root, self.point]
    
    def get_vector(self):
        return self.point

    def create_polygon(self, face, vertices):
        return [(vertices[i].x, vertices[i].y) for i in [*face, face[0]]]
       
class Scene:
    def __init__(self, meshes, vectors, fov, distance):
        self.meshes = meshes
        self.vectors = vectors
        #print(type(self.vectors[0]))
        self.fov = fov
        self.distance = distance 
        self.euler_angles = [0, 0, 0]

    def transform_vertices(self, vertices, width, height):
        transformed_vertices = vertices
        #axis_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        # for angle, axis in reversed(list(zip(list(self.euler_angles), axis_list))):
        #     transformed_vertices = rotate_vertices(transformed_vertices, angle, axis)
        #generatedAngles = generateAngle()
        # for i in range(3):
        #     transformed_vertices = rotate_vertices(transformed_vertices, generatedAngles[i], axis_list[i])
        points.append([])
        for i in range(len(transformed_vertices)):
            #print(f"points{points} len{len(points) - 1} i{i}")
            adsi = tuple(transformed_vertices[i])
            points[len(points)-1].append(adsi)
        transformed_vertices = project_vertices(transformed_vertices, width, height, self.fov, self.distance)
        return transformed_vertices

    def draw(self, surface):
        
        polygons = []
        for mesh in self.meshes:
            generatedAngles = generateAngle()
            for i in range(3):
                print(f"gen:{generatedAngles[i]}")
                mesh.rotate(generatedAngles[i],axes[i])
            transformed_vertices = self.transform_vertices(mesh.get_vertices(), *surface.get_size())
            avg_z = mesh.calculate_average_z(transformed_vertices)
            for z in avg_z:
            #for z in sorted(avg_z, key=lambda x: x[1], reverse=True):
                pointlist = mesh.create_polygon(mesh.get_face(z[0]), transformed_vertices)
                polygons.append((pointlist, z[1]))
                #pygame.draw.polygon(surface, (128, 128, 192), pointlist)
                #pygame.draw.polygon(surface, (0, 0, 0), pointlist, 3)
                
        for vector in self.vectors:
            print(vector)
            transformed_vertices = self.transform_vertices(vector.get_vertices(), *surface.get_size())
            vector.point.y -= 0.01
            avg_z = vector.calculate_average_z(transformed_vertices)
            for i in range(3):
                #print(f"gen:{generatedAngles[i]}")
                vector.rotate(generatedAngles[i],axes[i])
            for z in avg_z:
            #for z in sorted(avg_z, key=lambda x: x[1], reverse=True):
                pointlist = vector.create_polygon(vector.get_line(), transformed_vertices)
                polygons.append((pointlist, z[1]))
                #pygame.draw.polygon(surface, (128, 128, 192), pointlist)
                #pygame.draw.polygon(surface, (0, 0, 0), pointlist, 3)

        for poly in sorted(polygons, key=lambda x: x[1], reverse=True):
            pygame.draw.polygon(surface, (128, 128, 192), poly[0])
            #print(len(poly[0]))
            if(len(poly[0]) != 3):
                pygame.draw.polygon(surface, (0, 0, 0), poly[0], 3)
            else:
                pygame.draw.polygon(surface, (200, 50, 100), poly[0], 3)
        

vertices = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), (-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5)]
faces = [(0,1,2,3), (1,5,6,2), (5,4,7,6), (4,0,3,7), (3,2,6,7), (1,0,4,5)]

#cube_origins = [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (-1, 1, 0), (-1, 0, 0)]



meshes = []
cube = Mesh(vertices, faces)
#cube.scale((0.5, 0.5, 0.5))
cube.translate((0,0,0))
meshes.append(cube)
    
vectors = []
for vec in vertices:
    vector = Vector((0,0,0), (0,0,0))
    vector.scale((0.5, 0.5, 0.5))
    vector.translate(vec)
    vectors.append(vector)

scene = Scene(meshes, vectors, 90, 5)

pygame.init()
window = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(timeFrame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((255, 255, 255))
    scene.draw(window)
    scene.euler_angles[1] += 1
    t += 1.0/timeFrame
    if(manualStop != -1 and t > manualStop):
        break
    pygame.display.flip()

#print("--POINTS--\n")
#print(points)
pointsVelocity = []
for i in range(len(points) - 1):
    pointsVelocity.append([])
    for j in range(8):
        veloX = points[i + 1][j][0] - points[i][j][0]
        veloY = points[i + 1][j][1] - points[i][j][1]
        veloZ = points[i + 1][j][2] - points[i][j][2]
        pointsVelocity[i].append((veloX,veloY,veloZ))
        #pointsVelocity[i][j] = points[i + 1][j] - points[i][j]

#print("\n--POINTS VELO--\n")
#print(pointsVelocity)
pointsAcceleration = []
for i in range(len(pointsVelocity) - 1):
    pointsAcceleration.append([])
    for j in range(8):
        accelX = pointsVelocity[i + 1][j][0] - pointsVelocity[i][j][0]
        accelY = pointsVelocity[i + 1][j][1] - pointsVelocity[i][j][1] + 9.81
        accelZ = pointsVelocity[i + 1][j][2] - pointsVelocity[i][j][2]
        pointsAcceleration[i].append((accelX,accelY,accelZ))
        
#print("\n--POINTS ACCEL--\n")
#print(pointsAcceleration)

netAccel = [0,0,0,0,0,0,0,0]
for j in range(8):
    for i in range(len(pointsAcceleration)):
        netAccel[j] += math.sqrt((pointsAcceleration[i][j][0] ** 2) + (pointsAcceleration[i][j][1] ** 2) + (pointsAcceleration[i][j][2] ** 2))
     
print("\n--NET ACCEL--\n")   
#print(netAccel)
pygame.quit()
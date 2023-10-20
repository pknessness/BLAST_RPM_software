import math, pygame, copy

t = 0
timeFrame = 10
manualStop = -1

points = []

def generateAngle():
    global t
    x = math.sin(t/5 - 10) * 360 + 180
    #y = math.sin(3*t + 19) * 360 + 180
    z = math.sin(t/7 + 11) * 360 + 180
    y = 0
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

    def __init__(self, vertices, faces, modifiableVector = False):
        self.__vertices = [pygame.math.Vector3(v) for v in vertices]
        self.__faces = faces
        self.modVector = modifiableVector

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
       
class Scene:
    def __init__(self, meshes, fov, distance):
        self.meshes = meshes
        self.fov = fov
        self.distance = distance 
        self.euler_angles = [0, 0, 0]

    def transform_vertices(self, vertices, width, height, rotate = True):
        transformed_vertices = vertices
        axis_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        # for angle, axis in reversed(list(zip(list(self.euler_angles), axis_list))):
        #     transformed_vertices = rotate_vertices(transformed_vertices, angle, axis)
        generatedAngles = generateAngle()
        for i in range(3):
            if(rotate == True):
                transformed_vertices = rotate_vertices(transformed_vertices, generatedAngles[i], axis_list[i])
                print(f"Gangle:{generatedAngles[j]} Gaxis:{axis_list[j]}")
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
            
            #if(mesh.modVector == False):
            transformed_vertices = self.transform_vertices(mesh.get_vertices(), *surface.get_size())
            avg_z = mesh.calculate_average_z(transformed_vertices)
            for z in avg_z:
            #for z in sorted(avg_z, key=lambda x: x[1], reverse=True):
                pointlist = mesh.create_polygon(mesh.get_face(z[0]), transformed_vertices)
                polygons.append((pointlist, z[1]))
                #pygame.draw.polygon(surface, (128, 128, 192), pointlist)
                #pygame.draw.polygon(surface, (0, 0, 0), pointlist, 3)

        for poly in sorted(polygons, key=lambda x: x[1], reverse=True):
            pygame.draw.polygon(surface, (128, 128, 192), poly[0])
            pygame.draw.polygon(surface, (0, 0, 0), poly[0], 3)
        

vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1), (-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (2, 2, 2)]
faces = [(0,1,2,3), (1,5,6,2), (5,4,7,6), (4,0,3,7), (3,2,6,7), (1,0,4,5)]

forceVectorVertices =   [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1), (-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
forceVectorLines = [(0,8),(1,9),(2,10),(3,11),(4,12),(5,13),(6,14),(7,15)]

axes = [(1,0,0),(0,1,0),(0,0,1)]

#cube_origins = [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (-1, 1, 0), (-1, 0, 0)]
cube_origins = [(0,0,0)]
meshes = []
for origin in cube_origins:
    cube = Mesh(vertices, faces)
    cube.scale((0.5, 0.5, 0.5))
    cube.translate(origin)
    
    for i in range(len(forceVectorLines)):
        print(i)
        forceVectors = Mesh(forceVectorVertices, [forceVectorLines[i]], True)
        #forceVectors.scale((0.5, 0.5, 0.5))
        forceVectors.translate(origin)
        meshes.append(forceVectors)
    
    meshes.append(cube)
    

scene = Scene(meshes, 90, 5)

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
    sceneSave = copy.deepcopy(scene.meshes)
    for i in scene.meshes:
        if (i.modVector == True):
            # print(i)
            angles = generateAngle()
            for j in range(3):
                i.rotate(-angles[j] * 0, axes[j])
                print(f"angle:{-angles[j]} axis:{axes[j]}")
            # i.vertices[]
    scene.draw(window)
    scene.meshes = sceneSave
    
    scene.euler_angles[1] += 1
    t += 1.0/timeFrame
    if(manualStop != -1 and t > manualStop):
        break
    pygame.display.flip()

print("--POINTS--\n")
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

print("\n--POINTS VELO--\n")
#print(pointsVelocity)
pointsAcceleration = []
for i in range(len(pointsVelocity) - 1):
    pointsAcceleration.append([])
    for j in range(8):
        accelX = pointsVelocity[i + 1][j][0] - pointsVelocity[i][j][0]
        accelY = pointsVelocity[i + 1][j][1] - pointsVelocity[i][j][1] + 9.81
        accelZ = pointsVelocity[i + 1][j][2] - pointsVelocity[i][j][2]
        pointsAcceleration[i].append((accelX,accelY,accelZ))
        
print("\n--POINTS ACCEL--\n")
#print(pointsAcceleration)

netAccel = [0,0,0,0,0,0,0,0]
for j in range(8):
    for i in range(len(pointsAcceleration)):
        netAccel[j] += math.sqrt((pointsAcceleration[i][j][0] ** 2) + (pointsAcceleration[i][j][1] ** 2) + (pointsAcceleration[i][j][2] ** 2))
     
print("\n--NET ACCEL--\n")   
print(netAccel)
pygame.quit()
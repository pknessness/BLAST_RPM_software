import sys
import math
import pygame

from pygame.math import Vector3
from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    SILVER = (192,192,192)


class Cube():

    def __init__(self, vectors, screen_width, screen_height, initial_angle=25):
        self._vectors = vectors
        self._angle = initial_angle
        self._screen_width = screen_width
        self._screen_height = screen_height

        # Define the vectors that compose each of the 6 faces
        self._faces  = [(0,1,2,3),
                       (1,5,6,2),
                       (5,4,7,6),
                       (4,0,3,7),
                       (0,4,5,1),
                       (3,2,6,7)]

        self._setup_initial_positions(initial_angle)

    def _setup_initial_positions(self, angle):
        tmp = []
        for vector in self._vectors:
            rotated_vector = vector.rotate_x(angle).rotate_y(angle)#.rotateZ(self.angle)
            tmp.append(rotated_vector)

        self._vectors = tmp

    def transform_vectors(self, new_angle):
        # It will hold transformed vectors.
        transformed_vectors = []

        for vector in self._vectors:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            mod_vector = vector.rotate_y(new_angle)
            # Transform the point from 3D to 2D
            mod_vector = self._project(mod_vector, self._screen_width, self._screen_height, 256, 4)
            # Put the point in the list of transformed vectors
            transformed_vectors.append(mod_vector)

        return transformed_vectors

    def _project(self, vector, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + vector.z)
        x = vector.x * factor + win_width / 2
        y = -vector.y * factor + win_height / 2
        return Vector3(x, y, vector.z)

    def calculate_average_z(self, vectors):
        avg_z = []
        for i, face in enumerate(self._faces):
            # for each point of a face calculate the average z value
            z = (vectors[face[0]].z + 
                 vectors[face[1]].z + 
                 vectors[face[2]].z + 
                 vectors[face[3]].z) / 4.0
            avg_z.append([i, z])

        return avg_z

    def get_face(self, index):
        return self._faces[index]

    def create_polygon(self, face, transformed_vectors):
        return [(transformed_vectors[face[0]].x, transformed_vectors[face[0]].y), 
                (transformed_vectors[face[1]].x, transformed_vectors[face[1]].y),
                (transformed_vectors[face[2]].x, transformed_vectors[face[2]].y),
                (transformed_vectors[face[3]].x, transformed_vectors[face[3]].y),
                (transformed_vectors[face[0]].x, transformed_vectors[face[0]].y)]


class Simulation:
    def __init__(self, win_width=640, win_height=480):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))

        self.clock = pygame.time.Clock()

        cube = Cube([
            Vector3(0, 0.5, -0.5),
            Vector3(0.5, 0.5, -0.5),
            Vector3(0.5, 0, -0.5),
            Vector3(0, 0, -0.5),
            Vector3(0, 0.5, 0),
            Vector3(0.5, 0.5, 0),
            Vector3(0.5, 0, 0),
            Vector3(0, 0, 0)
        ], win_width, win_height)

        cube2 = Cube([
            Vector3(0.5, 0.5, -0.5),
            Vector3(1, 0.5, -0.5),
            Vector3(1, 0, -0.5),
            Vector3(0.5, 0, -0.5),
            Vector3(0.5, 0.5, 0),
            Vector3(1, 0.5, 0),
            Vector3(1, 0, 0),
            Vector3(0.5, 0, 0)
        ], win_width, win_height)

        self._angle = 30

        self._cubes = [cube, cube2]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(Color.BLACK.value)

            for cube in self._cubes:
                transformed_vectors = cube.transform_vectors(self._angle)
                avg_z = cube.calculate_average_z(transformed_vectors)

                # Draw the faces using the Painter's algorithm:
                # Distant faces are drawn before the closer ones.
                for avg_z in sorted(avg_z, key=lambda x: x[1], reverse=True):
                    face_index = avg_z[0]
                    face = cube._faces[face_index]
                    pointlist = cube.create_polygon(face, transformed_vectors)

                    pygame.draw.polygon(self.screen, Color.SILVER.value,pointlist)
                    pygame.draw.polygon(self.screen, Color.BLACK.value, pointlist, 3)
                    # break 

            self._angle += 1

            pygame.display.flip()

if __name__ == "__main__":
    Simulation().run()
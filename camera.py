import math
import sys
from hittable import Hittable
from ray import Ray
from vec3 import vec3, color, point3, write_color, random_vec
from interval import Interval
import numpy as np

class Camera():

    def __init__(self, aspect_ratio: float, image_width: int, samples_per_pixel: int):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel

    def render(self, world: Hittable):
        self.initialize()
        sys.stdout.write("P3\n" + str(self.image_width) + " " + str(self.image_height) + "\n255\n")
        for j in range(self.image_height):
            sys.stderr.write("\rScanlines remaining: " + str(self.image_height - j) + " ")
            sys.stderr.flush()
            for i in range(self.image_width):
                pixel_color = color() #0, 0, 0
                for _ in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, world)
                write_color(pixel_color / self.samples_per_pixel)

        sys.stderr.write("\rDone.                   \n")
        return

    def initialize(self):
        self.image_height = int(self.image_width // self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height
        self.camera_center = point3(0, 0, 0)

        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width/self.image_height)

    # pixel delta
        self.dels = np.array([viewport_width / self.image_width, -viewport_height / self.image_height, 1.0], dtype='double')

        viewport_upper_left = (self.camera_center 
            - vec3(0, 0, focal_length) 
            - (vec3(viewport_width, -viewport_height) / 2))

        self.pixel00_loc = viewport_upper_left + (self.dels[0] + self.dels[1]) * 0.5
        return

    def get_ray(self, i: int, j: int) -> Ray:
        #ray from origin to randomly sampled point around i, j
        offset = self.sample_square()
        pixel_offset = np.array([i, j, 0], dtype='double')

        pixel_sample = self.pixel00_loc + (offset + pixel_offset) * self.dels
        # gets random pixel loc around point i, j

        direction = pixel_sample - self.camera_center

        return Ray(self.camera_center, direction)
    
    def sample_square(self):
        # return random vector to a unit square, from (-.5, -.5) to (.5, .5)
        res = random_vec(-0.5, 0.5)
        res[2] = 0.0
        return res


    def ray_color(self, r: Ray, world: Hittable) -> np.ndarray:
        res = world.hit(r, Interval(0, math.inf))
        if res:
            return 0.5 * (res.normal + color(1, 1, 1))

        unit_direction: np.ndarray = r.direction / np.linalg.norm(r.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1-a) * color(1, 1, 1) + a * color(0.5, 0.7, 1)


def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180.0

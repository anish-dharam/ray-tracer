import math
import sys
from hittable import Hittable
from ray import Ray
from vec3 import Vec3, Color, Point3, unit_vector, write_color, random_float, random_unit_vector
from interval import Interval

class Camera():

    def __init__(self, aspect_ratio: float, image_width: int, samples_per_pixel: int, max_depth: int):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth #for a 3-sphere, 2-cube env: 50 sped up program by ~30%, 10 sped up program by ~70%
        # (max_depth also prevents stack overflows)

    def render(self, world: Hittable):
        self.initialize()
        sys.stdout.write("P3\n" + str(self.image_width) + " " + str(self.image_height) + "\n255\n")
        for j in range(self.image_height):
            sys.stderr.write("\rScanlines remaining: " + str(self.image_height - j) + " ")
            sys.stderr.flush()
            for i in range(self.image_width):
                pixel_color = Color() #0, 0, 0
                for _ in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, self.max_depth, world)
                write_color(pixel_color / self.samples_per_pixel)

        sys.stderr.write("\rDone.                   \n")
        return

    def initialize(self):
        self.image_height = int(self.image_width // self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height
        self.camera_center = Point3(0, 0, 0)

        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width/self.image_height)

    # viewport
        viewport_u = Vec3(viewport_width, 0, 0)
        viewport_v = Vec3(0, -viewport_height, 0)
    # pixel delta
        self.del_u = viewport_u / self.image_width
        self.del_v = viewport_v / self.image_height

        viewport_upper_left = (self.camera_center 
            - Vec3(0, 0, focal_length) 
            - viewport_u/2 
            - viewport_v/2)

        self.pixel00_loc = viewport_upper_left + (self.del_u + self.del_v) * 0.5
        return

    def get_ray(self, i: int, j: int):
        #ray from origin to randomly sampled point around i, j
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x()) * self.del_u) + ((j + offset.y()) * self.del_v)
        # gets random pixel around point i, j

        direction = pixel_sample - self.camera_center

        return Ray(self.camera_center, direction)
    
    def sample_square(self):
        # return random vector to a unit square, from (-.5, -.5) to (.5, .5)
        return Vec3(random_float() - 0.5, random_float() - 0.5, 0)


    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        if depth <= 0:
            return Color()
        res = world.hit(r, Interval(0.001, math.inf)) # prevents shadow acne, sped up 3-sphere 2-cube w/ max_depth 10 by ~50%
        if res:
            bounce_direction = random_unit_vector() + res.normal #lambertian reflection
            return 0.5 * self.ray_color(Ray(res.point, bounce_direction), depth - 1, world)

        unit_direction: Vec3 = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y() + 1.0)
        return (1-a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)


def degrees_to_radians(degrees: float):
    return degrees * math.pi / 180.0

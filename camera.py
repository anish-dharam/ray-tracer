import math
import sys
from hittable import Hittable
from ray import Ray
from vec3 import Vec3, Color, Point3, unit_vector, write_color
from interval import Interval

class Camera():

    def __init__(self, aspect_ratio: float, image_width: int):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width

    def render(self, world: Hittable):
        self.initialize()
        sys.stdout.write("P3\n" + str(self.image_width) + " " + str(self.image_height) + "\n255\n")
        for j in range(self.image_height):
            sys.stderr.write("\rScanlines remaining: " + str(self.image_height - j) + " ")
            sys.stderr.flush()
            for i in range(self.image_width):
                pixel_center: Point3 = self.pixel00_loc + (self.del_u * i) + (self.del_v * j)
                ray_direction: Vec3 = pixel_center - self.camera_center
                r = Ray(self.camera_center, ray_direction)

                pixel_color: Color = self.ray_color(r, world)
                write_color(pixel_color)

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
    
    def ray_color(self, r: Ray, world: Hittable) -> Color:
        res = world.hit(r, Interval(0, math.inf))
        if res:
            return 0.5 * (res.normal + Color(1, 1, 1))

        unit_direction: Vec3 = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y() + 1.0)
        return (1-a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)


def degrees_to_radians(degrees: float):
    return degrees * math.pi / 180.0

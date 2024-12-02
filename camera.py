import math
import sys
from hittable import Hittable
from ray import Ray
from vec3 import Vec3, Color, Point3, random_in_unit_disk, unit_vector, write_color, cross
from interval import Interval
import random

class Camera():

    def __init__(self, aspect_ratio: float, image_width: int, 
                 samples_per_pixel: int, max_depth: int, 
                 vfov: int, look_from: Point3, look_at: Point3, view_up: Vec3, 
                 defocus_angle: float, focus_dist: float):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth #for a 3-sphere, 2-cube env: 50 sped up program by ~30%, 10 sped up program by ~70%
        # (max_depth also prevents stack overflows)
        self.vertical_fov = vfov
        self.camera_center = look_from
        self.look_at = look_at
        self.view_up = view_up
        self.defocus_angle = defocus_angle
        self.focus_dist = focus_dist

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
                    res = self.ray_color(r, self.max_depth, world)
                    pixel_color += res
                write_color(pixel_color / self.samples_per_pixel)

        sys.stderr.write("\rDone.                   \n")
        return

    def initialize(self):
        self.image_height = int(self.image_width // self.aspect_ratio)
        self.image_height = 1 if self.image_height < 1 else self.image_height

    #viewport dimensions
        theta = degrees_to_radians(self.vertical_fov)
        top_viewable = math.tan(theta / 2)
        viewport_height = 2 * top_viewable * self.focus_dist
        viewport_width = viewport_height * (self.image_width/self.image_height)

    #calculate camera basis vectors
        w = unit_vector(self.camera_center - self.look_at)
        u = unit_vector(cross(self.view_up, w))
        v = cross(w, u)

    # viewport vectors
        viewport_u = viewport_width * u
        viewport_v = viewport_height * -v #vector down viewport vertical edge
    # pixel delta
        self.del_u = viewport_u / self.image_width
        self.del_v = viewport_v / self.image_height

        viewport_upper_left = (self.camera_center 
            - w * self.focus_dist 
            - viewport_u/2 
            - viewport_v/2)

    #calculator defocus disk basis vectors
        self.defocus_radius = self.focus_dist * math.tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = u * self.defocus_radius
        self.defocus_disk_v = v * self.defocus_radius
    #location of pixel 0, 0
        self.pixel00_loc = viewport_upper_left + (self.del_u + self.del_v) * 0.5
        return

    def get_ray(self, i: int, j: int):
        #ray from defocus disk to randomly sampled point around i, j
        offset = self.sample_square()
        pixel_sample = (self.pixel00_loc 
        + ((i + offset.x) * self.del_u) 
        + ((j + offset.y) * self.del_v))
        # gets random pixel around point i, j

        ray_origin = self.camera_center if self.defocus_angle <= 0 else self.defocus_disk_sample()

        direction = pixel_sample - ray_origin

        return Ray(ray_origin, direction)
    
    def sample_square(self):
        # return random vector to a unit square, from (-.5, -.5) to (.5, .5)
        return Vec3(random.uniform(0, 1) - 0.5, random.uniform(0, 1) - 0.5, 0)

    def defocus_disk_sample(self):
        #return a random point in the defocus disk
        p = random_in_unit_disk()
        return self.camera_center + p.x * self.defocus_disk_u + p.y * self.defocus_disk_v

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        if depth <= 0:
            return Color()
        res_rec = world.hit(r, Interval(0.001, math.inf)) # prevents shadow acne, sped up 3-sphere 2-cube w/ max_depth 10 by ~50%
        if res_rec:
            res_bounce = res_rec.mat.scatter(r, res_rec.point, res_rec.normal, res_rec.front_face)
            if res_bounce:
                return res_bounce.color * self.ray_color(res_bounce.ray, depth - 1, world)
            return Color()

        unit_direction: Vec3 = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1-a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)


def degrees_to_radians(degrees: float):
    return degrees * math.pi / 180.0

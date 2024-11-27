from vec3 import Vec3, Point3, Color, dot, unit_vector, write_color
from ray import Ray
import sys
import math
from hittable import Hittable, HitRecord
from hittable_list import HittableList
from sphere import Sphere
from cube import Cube
def ray_color(r: Ray, world: Hittable) -> Color:
    res = world.hit(r, 0, math.inf)
    if res:
        return 0.5 * (res.normal + Color(1, 1, 1))

    unit_direction: Vec3 = unit_vector(r.direction)
    a = 0.5 * (unit_direction.y() + 1.0)
    return (1-a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)

def main():
    #image
    aspect_ratio = 16.0 / 9.0
    WIDTH = 400 
    HEIGHT = int(WIDTH // aspect_ratio)
    if HEIGHT < 1:
        HEIGHT = 1

#world
    world: HittableList = HittableList([])
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0.5, 0.1, -1), 0.4))
    # world.add(Sphere(Point3(-0.1, -0.2, -0.3), 0.2))
    world.add(Sphere(Point3(0, -100.5, -1), 100))
    world.add(Cube(Point3(-1.0, 1.0, -1.5), 0.4))
#camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (WIDTH/HEIGHT)
    camera_center = Point3(0, 0, 0)

# viewport
    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)
# pixel delta
    del_u = viewport_u / WIDTH
    del_v = viewport_v / HEIGHT


    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2 
    pixel00_loc: Point3 = viewport_upper_left + (del_u + del_v) * 0.5
    
    #render

    sys.stdout.write("P3\n" + str(WIDTH) + " " + str(HEIGHT) + "\n255\n")
    for j in range(HEIGHT):
        sys.stderr.write("\rScanlines remaining: " + str(HEIGHT - j) + " ")
        sys.stderr.flush()
        for i in range(WIDTH):
            pixel_center: Point3 = pixel00_loc + (del_u * i) + (del_v * j)
            ray_direction: Vec3 = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            pixel_color: Color = ray_color(r, world)
            write_color(pixel_color)

    sys.stderr.write("\rDone.                   \n")
    return

if __name__ == "__main__":
    main()


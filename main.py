from vec3 import Vec3, Point3, Color
from hittable_list import HittableList
from sphere import Sphere
from cube import Cube
from camera import Camera
from material import Lambertian, Metal, Dielectric
import math


def main():

#world
    world: HittableList = HittableList([])

    #book metal example
    material_ground = Lambertian(Color(0.6, 0.8, 0.2))
    # material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.5, 0.1, 0.2))
    # material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left_glass   = Dielectric(1.5)
    material_bubble   = Dielectric(1/1.5)
    material_left_metal   = Metal(Color(0.8, 0.8, 0.8), 0.3)
    material_right  = Metal(Color(0.8, 0.6, 0.2), 1.0)
    # material_cube   = Lambertian(Color(0.7, 0.91, 0.95))

    #anish example
    # world.add(Sphere(Point3(0, 0, -1), 0.5, material_left))
    # world.add(Sphere(Point3(2, 0.1, -3), 0.4, material_right))
    # world.add(Sphere(Point3(0, -210.5, -3), 200, material_ground))
    # world.add(Cube(Point3(-1.0, 1.0, -1.5), 0.4, material_center))
    # world.add(Cube(Point3(4.0, -3.0, -5.5), 1.4, material_cube))
    
    #book metal example with cube
    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   .5, material_left_glass))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   .4, material_bubble))
    # world.add(Cube(Point3(-1.0,    -0.1, -1.2),   0.37, material_left_metal))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right))


#camera
    cam = Camera(aspect_ratio=16.0 / 9.0, image_width=400, samples_per_pixel=500, max_depth=50, 
                 vfov=20, look_from=Point3(-2, 2, 1), look_at=Point3(0, 0, -1), view_up=Vec3(0, 1, 0),
                 defocus_angle=10, focus_dist=3.4)
    cam.render(world)
    return

if __name__ == "__main__":
    main()


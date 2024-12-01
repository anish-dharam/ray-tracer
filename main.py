from vec3 import Point3, Color
from hittable_list import HittableList
from sphere import Sphere
from cube import Cube
from camera import Camera
from material import Lambertian, Metal


def main():

#world
    world: HittableList = HittableList([])
    #anish example
    # world.add(Sphere(Point3(0, 0, -1), 0.5))
    # world.add(Sphere(Point3(2, 0.1, -3), 0.4))
    # world.add(Sphere(Point3(0, -210.5, -3), 200))
    # world.add(Cube(Point3(-1.0, 1.0, -1.5), 0.4))
    # world.add(Cube(Point3(4.0, -3.0, -5.5), 1.4))
    
    # #book original example + cube
    # world.add(Sphere(Point3(0,0,-1), 0.5, Lambertian(Color(0.8, 1, 0.9))))
    # world.add(Cube(Point3(-1.0, 0.03, -1), 0.4, Lambertian(Color(0.2, 0.1, 0.3))))
    # world.add(Sphere(Point3(0,-100.5,-1), 100, Lambertian(Color(0.5, 0.4, 0.55))))

    #book metal example
    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left   = Metal(Color(0.8, 0.8, 0.8))
    material_right  = Metal(Color(0.8, 0.6, 0.2))

    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right))

#camera
    cam = Camera(aspect_ratio=16.0 / 9.0, image_width=400, samples_per_pixel=100, max_depth=50)
    cam.render(world)
    return

if __name__ == "__main__":
    main()


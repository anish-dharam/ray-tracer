from vec3 import Point3
from hittable_list import HittableList
from sphere import Sphere
from cube import Cube
from camera import Camera


def main():

#world
    world: HittableList = HittableList([])
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(2, 0.1, -3), 0.4))
    world.add(Sphere(Point3(0, -210.5, -3), 200))
    world.add(Cube(Point3(-1.0, 1.0, -1.5), 0.4))
    world.add(Cube(Point3(4.0, -3.0, -5.5), 1.4))

#camera
    cam = Camera(16.0 / 9.0, 400)
    cam.render(world)
    return

if __name__ == "__main__":
    main()


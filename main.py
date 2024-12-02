from vec3 import Vec3, Point3, Color, random_vec
from hittable_list import HittableList
from sphere import Sphere
from cube import Cube
from camera import Camera
from material import Lambertian, Metal, Dielectric
import random


def main():

#world
    world: HittableList = HittableList([])

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0,-1000,0), 1000, ground_material))

    for a in range(-6, 6):
        for b in range(-6, 6):
            choose_mat = random.uniform(0, 1)
            center = Point3(a + 0.9 * random.uniform(0, 1), 0.2, b + 0.9* random.uniform(0, 1))

            if ((center - Point3(4, 0.2, 0)).length() > 0.9):
                if (choose_mat < 0.8):
                    albedo = random_vec() * random_vec()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif (choose_mat < 0.95):
                    albedo = random_vec(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))
            
        
    

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))



#camera
    cam = Camera(aspect_ratio=16.0 / 9.0, image_width=1200, samples_per_pixel=300, max_depth=50, 
                 vfov=20, look_from=Point3(13, 2, 3), look_at=Point3(0, 0, 0), view_up=Vec3(0, 1, 0),
                 defocus_angle=0.6, focus_dist=10)
    cam.render(world)
    return

if __name__ == "__main__":
    main()


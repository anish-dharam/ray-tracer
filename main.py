from vec3 import vec3, point3, color, cross, dot, unit_vector, write_color
from ray import ray
import sys

def ray_color(r) -> color:
    unit_direction = unit_vector(r.direction)
    a =  0.5*(unit_direction.y() + 1)
    return (1-a) * color(1, 1, 1) + a * color(0.5, 0.7, 1)

def main():
    aspect_ratio = 16.0 / 9.0
    WIDTH = 400 
    HEIGHT = int(WIDTH // aspect_ratio)
    if HEIGHT < 1:
        HEIGHT = 1
#camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (WIDTH/HEIGHT)
    camera_center = point3(0, 0, 0)

# viewport
    viewport_u = vec3(viewport_width, 0, 0)
    viewport_v = vec3(0, -viewport_height, 0)
# pixel delta
    del_u = viewport_u / WIDTH
    del_v = viewport_v / HEIGHT


    viewport_upper_left = camera_center - vec3(0, 0, focal_length) + viewport_u/2 - viewport_v/2 
    pixel00_loc: point3 = viewport_upper_left + (del_u + del_v) * 0.5
    
    #render

    sys.stdout.write("P3\n" + str(WIDTH) + " " + str(HEIGHT) + "\n255\n")
    for j in range(HEIGHT):
        sys.stderr.write("\rScanlines remaining: " + str(HEIGHT - j) + " ")
        sys.stderr.flush()
        for i in range(WIDTH):
            pixel_center: point3 = pixel00_loc + (del_u * i) + (del_v * j)
            ray_direction: vec3 = pixel_center - camera_center
            r = ray(camera_center, ray_direction)

            pixel_color: color = ray_color(r)
            write_color(pixel_color)

    sys.stderr.write("\rDone.                   \n")
    return

if __name__ == "__main__":
    main()


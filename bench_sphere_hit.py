import timeit

setup="""
from sphere import Sphere
from ray import Ray
from vec3 import Point3, Vec3
from interval import Interval

c = Sphere(Point3(0, 0, 1), 0.5)
r = Ray(Point3(0, 0, 0), Vec3(0.1, 0.1, 1))
"""
print(timeit.timeit("c.hit(r, Interval(0, 10))", number=100_000, setup=setup))
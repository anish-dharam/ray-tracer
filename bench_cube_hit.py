import timeit

setup="""
from cube import Cube
from ray import Ray
import numpy as np
from vec3 import point3, vec3
from interval import Interval

c = Cube(point3(0, 0, 1), 0.5)
r = Ray(point3(0, 0, 0), vec3(0.1, 0.1, 1))
"""
print(timeit.timeit("c.hit(r, Interval(0, 10))", number=100_000, setup=setup))
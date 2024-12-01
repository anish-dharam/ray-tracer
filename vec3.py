import math
import sys
import random
from interval import Interval

class Vec3:

    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]
    
    def x(self):
        return self.e[0]
    
    def y(self):
        return self.e[1]
    
    def z(self):
        return self.e[2]

    def __add__(self, other):
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
    
    def __sub__(self, other):
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

    def __mul__(self, t):
        return Vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)
    
    def __rmul__(self, t):
        return self.__mul__(t)

    def __truediv__(self, scalar):
        return Vec3(self.e[0] / scalar, self.e[1] / scalar, self.e[2] / scalar)

    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def len_squared(self):
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2

    def length(self):
        return math.sqrt(self.len_squared())

def dot(u, v):
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

def cross(u, v):
    return Vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1], u.e[2] * v.e[0] - u.e[0] * v.e[2], u.e[0] * v.e[1] - u.e[1] * v.e[0])

def unit_vector(v):
    return v / v.length()

Color = Vec3
Point3 = Vec3

def linear_to_gamma(lin_comp: float):
    if lin_comp > 0:
        return math.sqrt(lin_comp)
    return 0

def write_color(pixel_color: Color):
    r = linear_to_gamma(pixel_color.x())
    g = linear_to_gamma(pixel_color.y())
    b = linear_to_gamma(pixel_color.z())

    intensity: Interval = Interval(0.000, 0.999)
    r = int(255.999 * intensity.clamp_float(r))
    g = int(255.999 * intensity.clamp_float(g))
    b = int(255.999 * intensity.clamp_float(b))

    sys.stdout.write(f"{r} {g} {b}\n")

def random_float(lo=0.0, hi=1.0):
    return random.uniform(lo, hi)

def random_vec(lo=0.0, hi=1.0):
    return Vec3(random_float(lo, hi), random_float(lo, hi), random_float(lo, hi))

def random_unit_vector():
    while True:
        p = random_vec(-1, 1)
        lensq = p.len_squared()
        if (1e-160 < lensq <= 1):
            return p / math.sqrt(lensq)

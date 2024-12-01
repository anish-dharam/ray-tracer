import math
import sys
import random
from interval import Interval

class Vec3:

    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.x = e0
        self.y = e1
        self.z = e2
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.x * t.x, self.y * t.y, self.z * t.z)
        return Vec3(self.x * t, self.y * t, self.z * t)
    
    def __rmul__(self, t):
        return self.__mul__(t)

    def __truediv__(self, scalar):
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def len_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    def length(self):
        return math.sqrt(self.len_squared())

def dot(u, v):
    return u.x * v.x + u.y * v.y + u.z * v.z

def cross(u, v):
    return Vec3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)

def unit_vector(v):
    return v / v.length()

Color = Vec3
Point3 = Vec3

def linear_to_gamma(lin_comp: float):
    if lin_comp > 0:
        return math.sqrt(lin_comp)
    return 0

def write_color(pixel_color: Color):
    r = linear_to_gamma(pixel_color.x)
    g = linear_to_gamma(pixel_color.y)
    b = linear_to_gamma(pixel_color.z)

    intensity: Interval = Interval(0.000, 0.999)
    r = int(255.999 * intensity.clamp_float(r))
    g = int(255.999 * intensity.clamp_float(g))
    b = int(255.999 * intensity.clamp_float(b))

    sys.stdout.write(f"{r} {g} {b}\n")

def random_float(lo=0.0, hi=1.0) -> float:
    return random.uniform(lo, hi)

def random_vec(lo=0.0, hi=1.0) -> Vec3:
    return Vec3(random_float(lo, hi), random_float(lo, hi), random_float(lo, hi))

def random_unit_vector() -> Vec3:
    while True:
        p = random_vec(-1, 1)
        lensq = p.len_squared()
        if (1e-160 < lensq <= 1):
            return p / math.sqrt(lensq)

def near_zero(v: Vec3) -> bool:
    threshold = 1e-8
    return abs(v.x) < threshold and abs(v.y) < threshold and abs(v.z) < threshold

def reflect(colliding_vec: Vec3, surface_unit_normal: Vec3) -> Vec3:
    # subtract by twice the projection
    return colliding_vec - 2 * dot(colliding_vec, surface_unit_normal) * surface_unit_normal
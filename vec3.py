import sys
import numpy as np

def vec3(x: float=0.0, y: float=0.0, z: float=0.0) -> np.ndarray:
    return np.array([x, y, z], dtype='double')

color = vec3
point3 = vec3

# class Vec3:

#     def __init__(self, e0=0.0, e1=0.0, e2=0.0):
#         self.e = [e0, e1, e2]
    
#     def x(self):
#         return self.e[0]
    
#     def y(self):
#         return self.e[1]
    
#     def z(self):
#         return self.e[2]

#     def __add__(self, other):
#         return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
    
#     def __sub__(self, other):
#         return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

#     def __mul__(self, t):
#         return Vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)
    
#     def __rmul__(self, t):
#         return self.__mul__(t)

#     def __truediv__(self, scalar):
#         return Vec3(self.e[0] / scalar, self.e[1] / scalar, self.e[2] / scalar)

#     def __neg__(self):
#         return Vec3(-self.e[0], -self.e[1], -self.e[2])

#     def len_squared(self):
#         return self.e[0]**2 + self.e[1]**2 + self.e[2]**2

#     def length(self):
#         return math.sqrt(self.len_squared())

# def dot(u, v):
#     return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

# def cross(u, v):
#     return Vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1], u.e[2] * v.e[0] - u.e[0] * v.e[2], u.e[0] * v.e[1] - u.e[1] * v.e[0])

# def unit_vector(v: np.ndarray):
#     return v / v.length()

# Color = Vec3
# Point3 = Vec3

def write_color(pixel_color: np.ndarray):
    pixel_color = 255.999 * np.clip(pixel_color, 0, 1)
    pixel_color = pixel_color.astype(int)
    
    sys.stdout.write(f"{pixel_color[0]} {pixel_color[1]} {pixel_color[2]}\n")

def random_vec(lo=0.0, hi=1.0) -> np.ndarray:
    if lo >= hi:
        raise ValueError(f"bad args to random_vec: {lo=}, {hi=}")
    return (hi-lo) * np.random.random_sample(3) + lo
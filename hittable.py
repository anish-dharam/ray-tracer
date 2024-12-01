from abc import ABC, abstractmethod
from dataclasses import dataclass
from ray import Ray
from vec3 import Vec3, dot, Color
from typing import Optional
from interval import Interval
from material import Material, Lambertian

@dataclass
class HitRecord:
    t: float = 0.0
    point: tuple = (0, 0, 0)
    mat: Material = Lambertian(Color())
    normal: Vec3 = Vec3(0, 0, 0)
    front_face: bool = None

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        #outward normal has unit length, mutates front_face, normal
        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        """Determine if a ray hits this object"""
        pass

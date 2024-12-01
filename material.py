from abc import ABC, abstractmethod
from dataclasses import dataclass
from vec3 import Color, unit_vector, random_unit_vector, near_zero, reflect, Point3, Vec3, dot
from ray import Ray
from typing import Optional

@dataclass
class ColoredRay():
    ray: Ray
    color: Color

class Material(ABC):
    @abstractmethod
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3) -> Optional[ColoredRay]:
        """Returns a reflected ray with a new color, unless r was completely absorbed by the material"""
        pass
    
@dataclass
class Lambertian(Material):
    albedo: Color
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3) -> ColoredRay | None:
        scatter_direction = surface_normal + random_unit_vector()
        scatter_direction = surface_normal if near_zero(scatter_direction) else scatter_direction
        return ColoredRay(
            Ray(collision_point, scatter_direction), 
            self.albedo
        )

@dataclass
class Metal(Material):
    albedo: Color=Color()
    fuzz: float=0 #shouldn't be > 1
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3) -> ColoredRay | None:
        reflect_direction = reflect(r.direction, surface_normal)
        reflect_direction = unit_vector(reflect_direction) + (self.fuzz * random_unit_vector())
        if dot(reflect_direction, surface_normal) > 0:
            return ColoredRay(
                Ray(collision_point, reflect_direction),
                self.albedo
            )
        return None

from abc import ABC, abstractmethod
from dataclasses import dataclass
from vec3 import Color, unit_vector, random_unit_vector, near_zero, reflect, Point3, Vec3, dot, refract
from ray import Ray
from typing import Optional
import random
import math

@dataclass
class ColoredRay():
    ray: Ray
    color: Color

class Material(ABC):
    @abstractmethod
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3, front_face: bool) -> Optional[ColoredRay]:
        """Returns a reflected ray with a new color, unless r was completely absorbed by the material"""
        pass
    
@dataclass
class Lambertian(Material):
    albedo: Color
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3, _) -> Optional[ColoredRay]:
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
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3, _) -> Optional[ColoredRay]:
        reflect_direction = reflect(r.direction, surface_normal)
        reflect_direction = unit_vector(reflect_direction) + (self.fuzz * random_unit_vector())
        if dot(reflect_direction, surface_normal) > 0:
            return ColoredRay(
                Ray(collision_point, reflect_direction),
                self.albedo
            )
        return None

@dataclass
class Dielectric(Material):
    refraction_index: float=1.5 #glass
    def scatter(self, r: Ray, collision_point: Point3, surface_normal: Vec3, front_face: bool) -> Optional[ColoredRay]:
        ri = 1 / self.refraction_index if front_face else self.refraction_index
        unit_direction = unit_vector(r.direction)
        cos_theta = min(dot(-unit_direction, surface_normal), 1.0)
        sin_theta = math.sqrt(1 - cos_theta * cos_theta)
        cannot_refract = ri * sin_theta > 1

        
        if cannot_refract or self.reflectance(cos_theta, ri) > random.uniform(0, 1):
            direction = reflect(unit_direction, surface_normal) 
        else:
            direction = refract(unit_direction, surface_normal, ri)

        return ColoredRay(
            Ray(collision_point, direction),
            Color(1, 1, 1)
        )
    def reflectance(self, cosine: float, corrected_refraction: float):
        #use schlick's approximation for reflectance
        r0 = (1 - corrected_refraction) / (1 + corrected_refraction)
        r0 = r0*r0
        return r0 + (1-r0)*((1-cosine) ** 5)

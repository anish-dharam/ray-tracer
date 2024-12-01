from vec3 import Point3, Vec3
from dataclasses import dataclass

@dataclass
class Ray():
    origin: Vec3=Point3()
    direction: Vec3=Vec3()

    def at(self, t: float) -> Point3:
        return self.origin + t * self.direction
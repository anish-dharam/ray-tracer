from abc import ABC, abstractmethod
from dataclasses import dataclass
from ray import Ray
from vec3 import vec3, point3
from typing import Optional
from interval import Interval
import numpy as np

@dataclass
class HitRecord:
    t: float
    point: np.ndarray
    normal: Optional[np.ndarray]=None
    front_face: Optional[bool]=None

    def set_face_normal(self, r: Ray, outward_normal: np.ndarray):
        #outward normal has unit length, mutates front_face, normal
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        """Determine if a ray hits this object"""
        pass

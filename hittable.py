from abc import ABC, abstractmethod
from ray import Ray
from vec3 import vec3, point3
from typing import Optional
from interval import Interval
import numpy as np
import numba.types as nbt
import numba
from numba.experimental import jitclass

spec = [
    ('t', nbt.float64),
    ('point', nbt.float64[:]),
    ('normal', numba.optional(nbt.float64[:])),
    ('front_face', numba.optional(nbt.bool)),
]

@jitclass(spec)
class HitRecord:
    t: float
    point: np.ndarray
    normal: Optional[np.ndarray]
    front_face: Optional[bool]

    def __init__(self, t, point):
        self.t = t
        self.point = point

    def set_face_normal(self, r: Ray, outward_normal: np.ndarray):
        #outward normal has unit length, mutates front_face, normal
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        """Determine if a ray hits this object"""
        pass

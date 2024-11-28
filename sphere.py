from hittable import HitRecord, Hittable
from ray import Ray
from typing import Optional
from interval import Interval
import numpy as np

class Sphere(Hittable):
    def __init__(self, center: np.ndarray, radius: float):
        self.center = center
        self.radius = max(0, radius)
    
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        #returns a boolean indicating a hit,
        #also populates rec with hit data
        oc = self.center - r.origin
        a: np.float64 = r.direction.dot(r.direction)
        h: np.float64 = r.direction.dot(oc)
        c: np.float64 = oc.dot(oc) - self.radius*self.radius
        
        discriminant = h*h - a*c
        if discriminant < 0: 
            return None

        sqrtd: np.float64 = np.sqrt(discriminant)
        root: np.float64 = (h-sqrtd)/a
        if (not ray_t.exclusive(root)):
            #first root bad
            root = (h+sqrtd) / a
            if (not ray_t.exclusive(root)):
                return None
        #root is the closer point of contact
        t = root
        p = r.at(t)
        outward_normal = (p - self.center) / self.radius
        rec = HitRecord(t, p, None, None)
        rec.set_face_normal(r, outward_normal)

        return rec
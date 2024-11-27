import math
from hittable import HitRecord, Hittable
from vec3 import Point3, dot
from ray import Ray
from typing import Optional
from interval import Interval

class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float):
        self.center = center
        self.radius = max(0, radius)
    
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        #returns a boolean indicating a hit,
        #also populates rec with hit data
        oc = self.center - r.origin
        a = r.direction.len_squared()
        h = dot(r.direction, oc)
        c = oc.len_squared() - self.radius*self.radius
        
        discriminant = h*h - a*c
        if discriminant < 0: 
            return None

        sqrtd = math.sqrt(discriminant)
        root = (h-sqrtd)/a
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
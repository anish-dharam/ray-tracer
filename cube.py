from hittable import HitRecord, Hittable
from vec3 import point3
from ray import Ray
from typing import Optional
from interval import Interval
import numpy as np

class Cube(Hittable):
    def __init__(self, center: np.ndarray, half_length: float):
        self.center = center
        self.half_length = half_length
    
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        #https://gamedev.stackexchange.com/questions/18436/most-efficient-aabb-vs-ray-collision-algorithms
        # reciprocal_x = 1 / r.direction.x()
        # reciprocal_y = 1 / r.direction.y()
        # reciprocal_z = 1 / r.direction.z()

        reciprocal_vec = 1 / r.direction

        #left bottom back (minimal coordinates)
        lbb = self.center - point3(self.half_length, self.half_length, self.half_length)
        #right top front (maximal coordinates)
        rtf = self.center + point3(self.half_length, self.half_length, self.half_length)

        #not sure what the division does
        scaled_lbb = (lbb - r.origin) * reciprocal_vec #t1, t3, t5
        scaled_rtf = (rtf - r.origin) * reciprocal_vec #t2, t4, t6

        tmin: np.float64 = np.max(np.minimum(scaled_lbb, scaled_rtf))
        tmax: np.float64 = np.min(np.maximum(scaled_lbb, scaled_rtf))

        if tmax < ray_t.lo: #too late (or square behind ray, etc.)
            return None
        elif tmin > tmax:
            return None
        elif tmin > ray_t.hi:
            return None

        t=tmin
        p = r.at(t)
        
        relative_pos = p - self.center #cube center to hit point
        
        # component with largest absolute value tells us which face was hit
        abs_vec = np.absolute(relative_pos)
        abs_x = abs_vec[0]
        abs_y = abs_vec[1]
        abs_z = abs_vec[2]
        
        #will be a unit vector pointing out from the hit face
        if abs_x > abs_y and abs_x > abs_z:
            outward_normal = point3(1 if relative_pos[0] > 0 else -1, 0, 0)
        elif abs_y > abs_z:
            outward_normal = point3(0, 1 if relative_pos[1] > 0 else -1, 0)
        else:
            outward_normal = point3(0, 0, 1 if relative_pos[2] > 0 else -1)
            
        rec = HitRecord(t, p)
        rec.set_face_normal(r, outward_normal)

        return rec
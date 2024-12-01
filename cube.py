from hittable import HitRecord, Hittable
from vec3 import Point3
from ray import Ray
from typing import Optional
import numpy # type: ignore
from interval import Interval
from material import Material

class Cube(Hittable):
    def __init__(self, center: Point3, half_length: float, mat: Material):
        self.center = center
        self.half_length = half_length
        self.mat = mat
    
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        #https://gamedev.stackexchange.com/questions/18436/most-efficient-aabb-vs-ray-collision-algorithms
        # reciprocal_x = 1 / r.direction.x()
        # reciprocal_y = 1 / r.direction.y()
        # reciprocal_z = 1 / r.direction.z()
        reciprocal_x: float = numpy.divide(1, r.direction.x()) #very expensive
        reciprocal_y: float = numpy.divide(1, r.direction.y())
        reciprocal_z: float = numpy.divide(1, r.direction.z())

        #left bottom back (minimal coordinates)
        lbb = self.center - Point3(self.half_length, self.half_length, self.half_length) #very expensive
        #right top front (maximal coordinates)
        rtf = self.center + Point3(self.half_length, self.half_length, self.half_length)

        #not sure what the division does
        t1 = (lbb.x() - r.origin.x()) * reciprocal_x
        t2 = (rtf.x() - r.origin.x()) * reciprocal_x
        t3 = (lbb.y() - r.origin.y()) * reciprocal_y
        t4 = (rtf.y() - r.origin.y()) * reciprocal_y
        t5 = (lbb.z() - r.origin.z()) * reciprocal_z
        t6 = (rtf.z() - r.origin.z()) * reciprocal_z

        tmin = max(min(t1, t2), min(t3, t4), min(t5, t6))
        tmax = min(max(t1, t2), max(t3, t4), max(t5, t6))

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
        abs_x = abs(relative_pos.x())
        abs_y = abs(relative_pos.y())
        abs_z = abs(relative_pos.z())
        
        #will be a unit vector pointing out from the hit face
        if abs_x > abs_y and abs_x > abs_z:
            outward_normal = Point3(1 if relative_pos.x() > 0 else -1, 0, 0)
        elif abs_y > abs_z:
            outward_normal = Point3(0, 1 if relative_pos.y() > 0 else -1, 0)
        else:
            outward_normal = Point3(0, 0, 1 if relative_pos.z() > 0 else -1)
            
        rec = HitRecord(t, p, self.mat, None, None)
        rec.set_face_normal(r, outward_normal)

        return rec
from hittable import Hittable, HitRecord
from ray import Ray
from typing import Optional

class hittable_list(Hittable):
    def __init__(self, objects: list[Hittable]=[]):
        self.objects = objects

    def clear(self):
        self.objects: list[Hittable] = []
    
    def add(self, obj):
        self.objects.append(obj)
    
    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float) -> Optional[HitRecord]:
        rec = None
        closest_so_far = ray_tmax
        for obj in self.objects:
            res = obj.hit(r, ray_tmin, closest_so_far)
            if res:
                closest_so_far = res.t
                rec = res
        
        return rec


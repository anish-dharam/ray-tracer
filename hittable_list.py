from hittable import Hittable, HitRecord
from ray import Ray
from typing import Optional
from interval import Interval

class HittableList(Hittable):
    def __init__(self, objects: list[Hittable]=[]):
        self.objects = objects

    def clear(self):
        self.objects: list[Hittable] = []
    
    def add(self, obj):
        self.objects.append(obj)
    
    def hit(self, r: Ray, ray_t: Interval) -> Optional[HitRecord]:
        rec = None
        closest_so_far = ray_t.hi
        for obj in self.objects:
            res = obj.hit(r, Interval(ray_t.lo, closest_so_far))
            if res:
                closest_so_far = res.t
                rec = res
        
        return rec

    
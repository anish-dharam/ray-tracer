import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Interval():
    lo: float=math.inf
    hi: float=-math.inf
    # default interval is invalid/maximally weird
    
    def size(self):
        return self.hi - self.lo
    
    def inclusive(self, x):
        return self.lo <= x <= self.hi

    def exclusive(self, x):
        return self.lo < x < self.hi

    def clamp_float(self, x: float):
        if (x < self.lo):
            return self.lo
        elif (x > self.hi):
            return self.hi
        return x

empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)
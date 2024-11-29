import math
import numba.types as nbt
from numba.experimental import jitclass

spec = [
    ('lo', nbt.float64),
    ('hi', nbt.float64),
]

# @dataclass(frozen=True)
@jitclass(spec)
class Interval():
    lo: float
    hi: float
    # default interval is invalid/maximally weird
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi
    
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
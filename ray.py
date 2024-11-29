import numpy as np
from numba.experimental import jitclass
import numba.types as nbt

spec = [
    ('origin', nbt.float64[:]),
    ('direction', nbt.float64[:]),
]
# @dataclass(frozen=True)
@jitclass
class Ray():
    origin: nbt.float64[:]
    direction: nbt.float64[:]

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction
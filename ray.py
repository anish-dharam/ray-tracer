from vec3 import point3, vec3
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Ray():
    origin: np.ndarray
    direction: np.ndarray

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction
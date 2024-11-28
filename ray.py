from vec3 import point3, vec3
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Ray():
    origin: np.ndarray=point3()
    direction: np.ndarray=vec3()

    def at(self, t: float) -> np.ndarray:
        return self.origin + t * self.direction
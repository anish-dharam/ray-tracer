import sys
import numpy as np

def vec3(x: float=0.0, y: float=0.0, z: float=0.0) -> np.ndarray:
    return np.array([x, y, z], dtype='double')

color = vec3
point3 = vec3

def write_color(pixel_color: np.ndarray):
    """writes pixel color data to stdout"""
    pixel_color = 255.999 * np.clip(pixel_color, 0, 1)
    pixel_color = pixel_color.astype(int)
    
    sys.stdout.write(f"{pixel_color[0]} {pixel_color[1]} {pixel_color[2]}\n")

def random_vec(lo=0.0, hi=1.0) -> np.ndarray:
    """returns random vector with components bounded by lo and hi"""
    if lo >= hi:
        raise ValueError(f"bad args to random_vec: {lo=}, {hi=}")
    return (hi-lo) * np.random.random_sample(3) + lo
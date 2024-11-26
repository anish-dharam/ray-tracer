from vec3 import point3, vec3

class ray():
    def __init__(self, origin=point3(), direction=vec3()):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + t * self.direction
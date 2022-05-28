import glm

# functions obeys right hand rule (thumb, finger)

def cross_scalar(a: float, b: float):
    return a.x * b.y - a.y * b.x

def cross_vec2(s: float, a: glm.vec2):
    return glm.vec2(-s * a.y, s * a.x)

# def cross_vec2_other(a: glm.vec2, s: float):
#     return glm.vec2(s * a.y, -s * a.x)

def clamp(a: float, low: float, high: float):
    return max(low, min(a, high))
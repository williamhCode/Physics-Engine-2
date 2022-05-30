import numpy as np
import ctypes
import glm

print(np.uint32 == ctypes.c_uint32)
print(glm.c_uint32 == ctypes.c_uint32)
print(glm.uint32)

from OpenGL.GL import *

a = glGenVertexArrays(1)
b = glGenBuffers(1)
print(a, b)
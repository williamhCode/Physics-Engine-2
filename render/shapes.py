import numpy as np
from OpenGL.GL import *
import glm
from .shader import Shader

class Circle:
    
    def __init__(self, shader: Shader, radius):
        self.shader = shader
        
        # self.vertex_count = int(1.5 * radius**0.5 + 8)
        self.vertex_count = 8
        vertices_x = np.cos(np.linspace(np.pi/2, 2.5*np.pi, self.vertex_count, endpoint=False)) * radius
        vertices_y = np.sin(np.linspace(np.pi/2, 2.5*np.pi, self.vertex_count, endpoint=False)) * radius
        vertices = [p for v in list(zip(vertices_x, vertices_y)) for p in v]
        vertices += vertices[:2] + [0, 0]
        self.vertex_count += 2
        vertices = glm.array(glm.float32, *vertices)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        
    def draw(self, position, rotation):
        self.shader.use()
        self.shader.set_vec2('translate', position)
        self.shader.set_mat2('rotate', glm.mat2x2(glm.rotate(rotation)))
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)

import time
class Polygon:
    
    def __init__(self, shader: Shader, vertices: glm.array):
        self.shader = shader
        
        self.vertex_count = len(vertices)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STREAM_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        # t2 = time.perf_counter()
        
    def draw(self, vertices: glm.array):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STREAM_DRAW)
        
        self.shader.use()
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)

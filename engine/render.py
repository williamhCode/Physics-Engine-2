from OpenGL.GL import *
import glm

from .utiliies import set_cwd
from pathlib import Path

from .shader import Shader


MAX_QUAD_COUNT = 100
MAX_VERTEX_COUNT = MAX_QUAD_COUNT * 4
MAX_INDEX_COUNT = MAX_QUAD_COUNT * 6
MAX_TEXTURES = 32

class RenderData:
    vao: GLuint
    vbo: GLuint
    ibo: GLuint

    white_texture: GLuint
    
    vertices: glm.array

    texture_slots = [0] * MAX_TEXTURES

    
_s_data = RenderData()
import numpy as np
def init():
    # generate vertices
    _s_data.vertices = glm.array.zeros(MAX_VERTEX_COUNT, glm.float32)
    
    # generate vertex array object
    _s_data.vertices = glGenVertexArrays(1)
    glBindVertexArray(_s_data.vao)
    
    # generate vertex buffer object and allocate memory
    _s_data.vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, _s_data.vbo)
    glBufferData(GL_ARRAY_BUFFER, _s_data.vertices.nbytes, None, GL_DYNAMIC_DRAW)

    print(_s_data.vao, _s_data.vbo)
    print(type(_s_data.vao), type(_s_data.vbo))

    # set vertex attribute pointers
    # 3 position, 4 color, 2 tex_coords, 3 tex_index
    # size = (3 + 4 + 2 + 3) * 4 = 48
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 48, ctypes.c_void_p((0) * 4))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 48, ctypes.c_void_p((0 + 3) * 4))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 48, ctypes.c_void_p((0 + 3 + 4) * 4))

    glEnableVertexAttribArray(3)
    glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 48, ctypes.c_void_p((0 + 3 + 4 + 2) * 4))

    # generate index buffer object and buffer data
    indices = glm.array.zeros(MAX_INDEX_COUNT, glm.uint32)
    offset = 0
    for i in range(0, MAX_INDEX_COUNT, 6):
        indices[i] = offset
        indices[i + 1] = offset + 1
        indices[i + 2] = offset + 2
        indices[i + 3] = offset + 2
        indices[i + 4] = offset + 3
        indices[i + 5] = offset
        offset += 4

    _s_data.ibo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _s_data.ibo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, GL_STATIC_DRAW)

    # create 1x1 white texture
    _s_data.white_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, _s_data.white_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    color = glm.array(glm.uint8, 255, 255, 255, 255)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, color.ptr)

    _s_data.texture_slots[0] = _s_data.white_texture

    
def clear_window():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

# def resize(width, height):
#     view_matrix = glm.ortho(0, width, 0, height, -1, 1)
    
#     for shader in self.shaders:
#         shader.use()
#         shader.set_mat4('view', view_matrix)

def draw_circle(self, color, center, radius, width=0):
    pass
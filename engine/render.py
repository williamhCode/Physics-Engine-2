import time
from pathlib import Path

from OpenGL.GL import *
import glm
import numpy as np
from PIL import Image

# from .utiliies import set_cwd
# from .shader import Shader


def load_texture(filepath: str) -> GLuint | np.uint32:
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    image = Image.open(filepath)
    img_data = image.convert("RGBA").tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    

MAX_QUAD_COUNT = 100
MAX_VERTEX_COUNT = MAX_QUAD_COUNT * 4
MAX_INDEX_COUNT = MAX_QUAD_COUNT * 6
MAX_TEXTURES = 32

VERTEX_STRIDE = 10

class RenderData:
    vao: GLuint | np.uint32
    vbo: GLuint | np.uint32
    ibo: GLuint | np.uint32

    white_texture: GLuint | np.uint32

    # glm.array[glm.float32]
    vertices: glm.array
    vertex_count = 0 

    # glm.array[glm.uint32]
    texture_slots: glm.array
    texture_slot_index = 0
    
_s_data = RenderData()

def init():
    t1 = time.perf_counter()
    
    # generate vertices
    _s_data.vertices = glm.array.zeros(MAX_VERTEX_COUNT * VERTEX_STRIDE, glm.float32)
    
    # generate vertex array object
    _s_data.vao = glGenVertexArrays(1)
    glBindVertexArray(_s_data.vao)
    
    # generate vertex buffer object and allocate memory
    _s_data.vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, _s_data.vbo)
    glBufferData(GL_ARRAY_BUFFER, _s_data.vertices.nbytes, None, GL_DYNAMIC_DRAW)

    # set vertex attribute pointers
    # 3 position, 4 color, 2 tex_coords, 1 tex_index
    # size = (3 + 4 + 2 + 1) * 4 = 40
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p((0) * 4))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p((0 + 3) * 4))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p((0 + 3 + 4) * 4))

    glEnableVertexAttribArray(3)
    glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p((0 + 3 + 4 + 2) * 4))

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

    _s_data.texture_slots = glm.array.zeros(MAX_TEXTURES, glm.uint32)
    _s_data.texture_slots[0] = _s_data.white_texture

    t2 = time.perf_counter()
    print(t2 - t1)

def begin_batch():
    pass    

def end_batch():
    pass

def flush():
    pass

def set_data_from_quad(curr_index, position, color, tex_coords, tex_index):
    _s_data.vertices[curr_index] = position[0]
    _s_data.vertices[curr_index + 1] = position[1]
    _s_data.vertices[curr_index + 2] = 0.0
    _s_data.vertices[curr_index + 3] = color[0]
    _s_data.vertices[curr_index + 4] = color[1]
    _s_data.vertices[curr_index + 5] = color[2]
    _s_data.vertices[curr_index + 6] = color[3]
    _s_data.vertices[curr_index + 7] = tex_coords[0]
    _s_data.vertices[curr_index + 8] = tex_coords[1]
    _s_data.vertices[curr_index + 9] = tex_index 

def draw_quad(position, size, color):
    if (_s_data.vertex_count >= MAX_VERTEX_COUNT):
        end_batch()
        flush()
        begin_batch()

    texture_index = 0.0
    
    curr_index = _s_data.vertex_count * VERTEX_STRIDE
    _s_data.vertices[curr_index] = position[0]
    _s_data.vertices[curr_index + 1] = position[1]
    _s_data.vertices[curr_index + 2] = 0.0
    _s_data.vertices[curr_index + 3] = color[0]
    _s_data.vertices[curr_index + 4] = color[1]
    _s_data.vertices[curr_index + 5] = color[2]
    _s_data.vertices[curr_index + 6] = color[3]
    _s_data.vertices[curr_index + 7] = 0.0
    _s_data.vertices[curr_index + 8] = 0.0
    _s_data.vertices[curr_index + 9] = texture_index
    # set_data_from_quad(curr_index, position, color, (0.0, 0.0), texture_index)
    _s_data.vertex_count += 1

    curr_index = _s_data.vertex_count * VERTEX_STRIDE
    _s_data.vertices[curr_index] = position[0] + size[0]
    _s_data.vertices[curr_index + 1] = position[1]
    _s_data.vertices[curr_index + 2] = 0.0
    _s_data.vertices[curr_index + 3] = color[0]
    _s_data.vertices[curr_index + 4] = color[1]
    _s_data.vertices[curr_index + 5] = color[2]
    _s_data.vertices[curr_index + 6] = color[3]
    _s_data.vertices[curr_index + 7] = 1.0
    _s_data.vertices[curr_index + 8] = 0.0
    _s_data.vertices[curr_index + 9] = texture_index
    _s_data.vertex_count += 1

    curr_index = _s_data.vertex_count * VERTEX_STRIDE
    _s_data.vertices[curr_index] = position[0] + size[0]
    _s_data.vertices[curr_index + 1] = position[1] + size[1]
    _s_data.vertices[curr_index + 2] = 0.0
    _s_data.vertices[curr_index + 3] = color[0]
    _s_data.vertices[curr_index + 4] = color[1]
    _s_data.vertices[curr_index + 5] = color[2]
    _s_data.vertices[curr_index + 6] = color[3]
    _s_data.vertices[curr_index + 7] = 1.0
    _s_data.vertices[curr_index + 8] = 1.0
    _s_data.vertices[curr_index + 9] = texture_index
    _s_data.vertex_count += 1

    curr_index = _s_data.vertex_count * VERTEX_STRIDE
    _s_data.vertices[curr_index] = position[0]
    _s_data.vertices[curr_index + 1] = position[1] + size[1]
    _s_data.vertices[curr_index + 2] = 0.0
    _s_data.vertices[curr_index + 3] = color[0]
    _s_data.vertices[curr_index + 4] = color[1]
    _s_data.vertices[curr_index + 5] = color[2]
    _s_data.vertices[curr_index + 6] = color[3]
    _s_data.vertices[curr_index + 7] = 0.0
    _s_data.vertices[curr_index + 8] = 1.0
    _s_data.vertices[curr_index + 9] = texture_index
    _s_data.vertex_count += 1

def draw_circle(color, center, radius, width=0):
    pass
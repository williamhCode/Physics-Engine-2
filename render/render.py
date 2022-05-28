from OpenGL.GL import *

from physics.body import Shape
from physics.body import Body
from physics.arbiter import Arbiter

from .shader import Shader
from .shapes import *
import os
import glm

import time
class Renderer:
    
    def __init__(self):
        self.shapes = []
        
        glClearColor(0.0, 0.0, 0.0, 1)

        glPointSize(5)
        glEnable(GL_LINE_SMOOTH)
        
        savedPath = os.getcwd()
        curr_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(curr_path)        
        
        self.circle_shader = Shader('shaders/circle.vert', 'shaders/circle.frag')
        self.point_shader = Shader('shaders/point.vert', 'shaders/point.frag')
        self.polygon_shader = Shader('shaders/polygon.vert', 'shaders/polygon.frag')
        
        os.chdir(savedPath)
        
        self.shaders = [self.circle_shader, self.point_shader, self.polygon_shader]

    def resize(self, width, height):
        view_matrix = glm.ortho(0, width, 0, height, -1, 1)
        
        for shader in self.shaders:
            shader.use()
            shader.set_mat4('view', view_matrix)
        
    def add_circle(self, radius):
        self.shapes.append(Circle(self.circle_shader, radius))
        
    def add_polygon(self, vertices):
        self.shapes.append(Polygon(self.polygon_shader, vertices))
    
    # world bodies list
    def draw_shapes(self, bodies_list: list[Body]):
        for shape, body in zip(self.shapes, bodies_list):

            if body.shape.get_type() == Shape.CIRCLE:
                shape.draw(body.position, body.rotation)
                
            elif body.shape.get_type() == Shape.POLYGON:
                shape.draw(body.shape.vertices)
            
    def draw_points(self, arbiters_list: list[Arbiter]):
        vertices = []
        for arb in arbiters_list:
            for contact in arb.contacts:
                vertices.extend([contact.position.x, contact.position.y])
        
        vertices = glm.array(glm.float32, *vertices)
        
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STREAM_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        self.point_shader.use()
        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, len(vertices)//2)
        
        glDeleteVertexArrays(1, (vao,))
        glDeleteBuffers(1, (vbo,))

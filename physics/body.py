import glm
from OpenGL.GL import *
from enum import IntEnum

class Shape(IntEnum):
    CIRCLE = 0
    POLYGON = 1


class Polygon:

    def __init__(self, vertices: list[tuple[float, float]]) -> None:
        self.org_vertices = glm.array([glm.vec2(v) for v in vertices])
        self.vertices = self.org_vertices
        
    def update_vertices(self, position, rotation):
        self.vertices = self.org_vertices.map(lambda v: glm.rotate(v, rotation) + position)
        
    def get_type(self):
        return Shape.POLYGON


class Box(Polygon):
    
    def __init__(self, dim) -> None:
        width_h = dim[0] / 2
        height_h = dim[1] / 2
        vertices = [(width_h, height_h), (-width_h, height_h), (-width_h, -height_h), (width_h, -height_h)]
        super().__init__(vertices)
        
    def compute_inertia(self, mass):
        return mass/12 * ((self.vertices[0][0] * 2)**2 + (self.vertices[0][1] * 2)**2)


import numpy as np
import time

class Circle:
    
    def __init__(self, radius) -> None:
        self.radius = radius
        # self.num_vertices = int(radius/20 + 8)
        self.num_vertices = 10
        
    def compute_inertia(self, mass):
        return mass * (self.radius ** 2) / 2
        
    def get_type(self):
        return Shape.CIRCLE
        
        
class Body:
    
    def __init__(self, shape, position=(0, 0), rotation=0, velocity=(0, 0), angular_velocity=0, friction=0, mass=1) -> None:  
        self.shape: Polygon | Circle = shape
              
        self.position = glm.vec2(position)
        self.rotation: float = rotation
        self.velocity = glm.vec2(velocity)
        self.angular_velocity: float = angular_velocity
        
        self.friction: float = friction
        
        self.mass: float = mass
        self.inv_mass = 1 / self.mass
        self.I: float = self.shape.compute_inertia(self.mass)
        self.inv_I: float = 1 / self.I
        
        self.force = glm.vec2(0, 0)
        self.torque = 0
        
        if shape.get_type() == Shape.POLYGON:
            self.shape.update_vertices(self.position, self.rotation)
    
    def add_force(self, force: list[float, float]) :
        self.force += glm.vec(force)
import math
import pyglet

from render.render import Renderer
pyglet.options['shadow_window'] = False

from pyglet.window import mouse
from pyglet.window import key
from timer import Timer
import random
import time
import math

import numpy as np
import glm

from physics.body import *
from physics.arbiter import Arbiter
from physics.world import World
import engine

class MainWindow(pyglet.window.Window):
    
    def __init__(self):
        config = pyglet.gl.Config(major_version=4, minor_version=5, forward_compatible=True, double_buffer=True)
        super().__init__(width=1280, height=720, vsync=False, resizable=True, config=config)

        engine.render.init()

        self.timer = Timer() 
        self.renderer = Renderer()

        self.init_objects()
        self.event_loop()

    def init_objects(self):
        self.world = World(glm.vec2(0, -500), 10)
        
        b = Body(Box((1280, 100)), position=(640, 50), mass=float('inf'))
        self.world.bodies.append(b)
        self.renderer.add_polygon(b.shape.vertices)
        
        b = Body(Box((100, 800)), position=(0, 400), mass=float('inf'))
        self.world.bodies.append(b)
        self.renderer.add_polygon(b.shape.vertices)
        
        b = Body(Box((100, 800)), position=(1280, 400), mass=float('inf'))
        self.world.bodies.append(b)
        self.renderer.add_polygon(b.shape.vertices)
        
        b = Body(Box((100, 100)), position=(500, 500), rotation=math.radians(45), mass=float('inf'))
        self.world.bodies.append(b)
        self.renderer.add_polygon(b.shape.vertices)
    
        # b = Body(Circle(100), position=(500, 500), velocity=(0, 0), mass=100)
        # self.world.bodies.append(b)
        # self.renderer.add_circle(b.shape.radius)
        # self.circle = b
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            velocity = 0, 0
            # b = Body(Circle(10), position=(x, y), velocity=velocity, mass=100)
            # self.world.bodies.append(b)
            # self.renderer.add_circle(b.shape.radius)
            for i in range(10):
                for j in range(10):
                    b = Body(Box((10, 10)), position=(x+i*30, y+j*30), velocity=velocity, mass=100)
                    self.world.bodies.append(b)
                    self.renderer.add_polygon(b.shape.vertices)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        # self.circle.position = glm.vec2(x, y)
        
    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == key.R:
            self.world.bodies = self.world.bodies[:4]
            self.renderer.shapes = self.renderer.shapes[:4]
        if symbol == key.S:
            for _ in range(10):
                velocity = 0, 0
                b = Body(Circle(10), position=(self.mouse_x + 100*(random.random()-0.5), self.mouse_y + 100*(random.random()-0.5)), velocity=velocity, mass=5)
                self.world.bodies.append(b)
                self.renderer.add_circle(b.shape.radius)
       
    def on_resize(self, width, height):
        pixel_width, pixel_height = self.get_framebuffer_size()
        glViewport(0, 0, pixel_width, pixel_height)
        
        self.renderer.resize(width, height)
        
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
        self.renderer.draw_shapes(self.world.bodies)
        self.renderer.draw_points(self.world.arbiters)

        self.flip()
                
    def event_loop(self):
        self.timer = Timer()
        
        while not self.has_exit:
            self.dispatch_events()
            
            dt = self.timer.tick()
            
            # self.world.update(dt/2)
            # self.world.update(dt/2)
            
            self.set_caption(f'{self.timer.get_fps():.5f} FPS')
            
            self.dispatch_event('on_draw')
        
if __name__ == '__main__':
    window = MainWindow()
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
from engine.shader import Shader


class MainWindow(pyglet.window.Window):
    
    def __init__(self):
        config = pyglet.gl.Config(major_version=4, minor_version=5, forward_compatible=True, double_buffer=True)
        super().__init__(width=1280, height=720, vsync=False, resizable=True, config=config)

        engine.render.init()

        self.shader = Shader('engine/shaders/quad.vert', 'engine/shaders/quad.frag')
        self.shader.use()
        test_tex_id = engine.render.load_texture('test.png')

        self.timer = Timer() 
        self.event_loop()
        
    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
       
    def on_resize(self, width, height):
        pixel_width, pixel_height = self.get_framebuffer_size()
        glViewport(0, 0, pixel_width, pixel_height)
        
        view_matrix = glm.ortho(0, width, 0, height, -1, 1)
        self.shader.use()
        self.shader.set_mat4('u_ViewProj', view_matrix)
        
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        engine.render.begin_batch()
        
        engine.render.draw_colored_quad((100, 100), (50, 50), (255, 0, 0, 255))

        engine.render.end_batch()
        engine.render.flush()

        self.flip()
                
    def event_loop(self):
        self.timer = Timer()
        
        while not self.has_exit:
            self.dispatch_events()
            
            dt = self.timer.tick()
            self.set_caption(f'{self.timer.get_fps():.5f} FPS')
            
            self.dispatch_event('on_draw')
        
if __name__ == '__main__':
    window = MainWindow()
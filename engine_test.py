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
        test_tex_id = engine.render.load_texture('test.png')

        self.timer = Timer() 
        self.event_loop()
        
    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
       
    def on_resize(self, width, height):
        pass
        
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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
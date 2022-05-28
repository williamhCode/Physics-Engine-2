import glm

from .arbiter import Arbiter
from .body import Body, Shape

class World:
    
    def __init__(self, gravity: glm.vec2, iterations: int):
        self.gravity = gravity
        self.iterations = iterations
        
        self.bodies: list[Body] = []
        self.arbiters: list[Arbiter] = []
        
    def add(self, shape: Body):
        self.bodies.append(shape)
        
    def broad_phase(self):
        self.arbiters.clear()
        
        for i in range(len(self.bodies)):
            b1 = self.bodies[i]
            
            for j in range(i + 1, len(self.bodies)):
                b2 = self.bodies[j]
                
                new_arbiter = Arbiter(b1, b2)
                if new_arbiter.num_contacts > 0:
                    self.arbiters.append(new_arbiter)
                    
        
    def update(self, dt):
        inv_dt = 1 / dt if dt > 0 else 0
        
        # determine overlapping bodies and contants
        self.broad_phase()
        
        # integrate forces
        for body in self.bodies:
            
            if body.inv_mass == 0:
                continue
            
            body.velocity += dt * (self.gravity + body.inv_mass * body.force)
            body.angular_velocity += dt * body.inv_I * body.torque
        
        # perform presteps
        for arb in self.arbiters:
            arb.prestep(inv_dt)
            
        for _ in range(self.iterations):
            
            for arb in self.arbiters:
                arb.apply_impulse()
                
        # integrate velocities
        for body in self.bodies:
            body.position += dt * body.velocity
            body.rotation += dt * body.angular_velocity
            
            body.force = glm.vec2(0, 0)
            body.torque = 0
            
            if body.shape.get_type() == Shape.POLYGON:
                body.shape.update_vertices(body.position, body.rotation)
    
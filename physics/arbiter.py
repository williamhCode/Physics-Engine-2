import glm

from . import collision
from . import math_utils

from .body import Body


class Contact:
    # accumulated impulse
    Pn: float = 0
    Pt: float = 0
    Pnb: float = 0
    
    # info at collision
    position: glm.vec2
    separation: float
    
    # info at prestep
    r1: glm.vec2
    r2: glm.vec2
    
    mass_normal: float
    mass_tangent: float
    
    bias: float

    
class Arbiter:
    allowed_penetration = 0.01
    bias_factor = 0.1
    
    def __init__(self, b1: Body, b2: Body):
        self.b1 = b1
        self.b2 = b2
        
        # info at collision
        self.num_contacts: float = 0
        self.contacts: list[Contact] = []
        
        self.normal: glm.vec2 # from b1 to b2
        self.tangent: glm.vec2
    
        # info at prestep
        self.restitution: float
        self.friction: float
        
        collision.collide(self, b1, b2)
        
    def prestep(self, inv_dt):
        self.restitution = 0.0
        self.friction = 0.3
        
        if self.b1.inv_mass + self.b2.inv_mass == 0:
            return
        
        for contact in self.contacts:
            # calculate r1 and r2
            contact.r1 = contact.position - self.b1.position
            contact.r2 = contact.position - self.b2.position
            
            # calculate mass normal
            kNormal = self.b1.inv_mass + self.b2.inv_mass
            kNormal += self.b1.inv_I * math_utils.cross_scalar(contact.r1, self.normal)**2 + self.b2.inv_I * math_utils.cross_scalar(contact.r2, self.normal)**2
            contact.mass_normal = 1 / kNormal
            
            # calculate mass tangent
            kTangent = self.b1.inv_mass + self.b2.inv_mass
            kTangent += self.b1.inv_I * math_utils.cross_scalar(contact.r1, self.tangent)**2 + self.b2.inv_I * math_utils.cross_scalar(contact.r2, self.tangent)**2
            contact.mass_tangent = 1 / kTangent
            
            # calculate bias
            contact.bias = -self.bias_factor * inv_dt * min(0, contact.separation + self.allowed_penetration)
        
    def apply_impulse(self):
        if self.b1.inv_mass + self.b2.inv_mass == 0:
            return
        
        for contact in self.contacts:
            # calculate relative velocity
            rv = self.b2.velocity + math_utils.cross_vec2(self.b2.angular_velocity, contact.r2) - self.b1.velocity - math_utils.cross_vec2(self.b1.angular_velocity, contact.r1)
            
            # calculate normal impulse
            vn = glm.dot(rv, self.normal)
            lam_n = contact.mass_normal * (-vn + contact.bias)
            
            # clamp accumulated impulse
            old_lam_n = contact.Pn
            contact.Pn = max(old_lam_n + lam_n, 0)
            lam_n = contact.Pn - old_lam_n
            
            # lam_n = max(lam_n, 0)
            
            # apply impulse
            imp_n = lam_n * self.normal
            
            self.b1.velocity -= self.b1.inv_mass * imp_n
            self.b1.angular_velocity -= self.b1.inv_I * math_utils.cross_scalar(contact.r1, imp_n)
            
            self.b2.velocity += self.b2.inv_mass * imp_n
            self.b2.angular_velocity += self.b2.inv_I * math_utils.cross_scalar(contact.r2, imp_n)
            
            # friction
            # calculate relative velocity
            rv = self.b2.velocity + math_utils.cross_vec2(self.b2.angular_velocity, contact.r2) - self.b1.velocity - math_utils.cross_vec2(self.b1.angular_velocity, contact.r1)
            
            # calculate tangent impulse
            vt = glm.dot(rv, self.tangent)
            lam_t = contact.mass_tangent * (-vt)
            
            # compute friction impulse
            max_lam_t = self.friction * contact.Pn
            
            # clamp friction
            old_lam_t = contact.Pt
            contact.Pt = math_utils.clamp(old_lam_t + lam_t, -max_lam_t, max_lam_t)
            lam_t = contact.Pt - old_lam_t
            
            # max_lam_t = self.friction * lam_n
            # lam_t = math_utils.clamp(lam_t, -max_lam_t, max_lam_t)
            
            # apply impulse
            imp_t = lam_t * self.tangent
            
            self.b1.velocity -= self.b1.inv_mass * imp_t
            self.b1.angular_velocity -= self.b1.inv_I * math_utils.cross_scalar(contact.r1, imp_t)
            
            self.b2.velocity += self.b2.inv_mass * imp_t
            self.b2.angular_velocity += self.b2.inv_I * math_utils.cross_scalar(contact.r2, imp_t)
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .arbiter import Arbiter

import glm

from .body import Body
from . import arbiter
from . import math_utils


# return min and max verts projected on axis
def proj_verts_on_axis(vertices: list[glm.vec2], axis: glm.vec2):
    min_proj = float('inf')
    max_proj = -float('inf')
    
    for vertex in vertices:
        proj = glm.dot(vertex, axis)
        min_proj = min(min_proj, proj)
        max_proj = max(max_proj, proj)
        
    return min_proj, max_proj
        
def circle_to_circle(arb: Arbiter, b1: Body, b2: Body):
    r1 = b1.shape.radius
    r2 = b2.shape.radius
    
    diff = b2.position - b1.position
    dist = glm.length(diff)
    
    if dist == 0:
        diff = r1 + r2 + glm.vec2(0, 10)
        dist = glm.length(diff)
    
    # separation
    s = dist - r1 - r2
    
    if s > 0:
        return
    
    normal = diff / dist
    
    contact = arbiter.Contact()
    contact.position = (normal * (r1 - r2) + b1.position + b2.position) / 2
    contact.separation = s
    
    arb.contacts.append(contact)
    arb.num_contacts += 1
    
    arb.normal = normal
    arb.tangent = math_utils.cross_vec2(1, normal)

def circle_to_polygon(arb: Arbiter, b1: Body, b2: Body):
    if polygon_to_circle(arb, b2, b1):
        arb.normal = -arb.normal
        arb.tangent = -arb.tangent

def polygon_to_circle(arb: Arbiter, b1: Body, b2: Body):
    # separation
    min_dist = float('inf')
    closest_vertex: glm.vec2
    for vertex in b1.shape.vertices:
        dist = glm.length(b2.position - vertex)
        
        if dist < min_dist:
            min_dist = dist
            closest_vertex = vertex
            
    normal = glm.normalize(b2.position - closest_vertex)
    poly_min, poly_max = proj_verts_on_axis(b1.shape.vertices, normal)
    circle_cen = glm.dot(normal, b2.position)
    circle_min, circle_max = circle_cen - b2.shape.radius, circle_cen + b2.shape.radius
    
    if circle_min > poly_max or poly_min > circle_max:
        return
    
    min_s = circle_min - poly_max
    min_axis = org_axis = normal
            
    for i in range(len(b1.shape.vertices)):
        v1 = b1.shape.vertices[i]
        v2 = b1.shape.vertices[(i + 1) % len(b1.shape.vertices)]
        
        normal = glm.normalize(glm.vec2(v2.y - v1.y, v1.x - v2.x))
        s = glm.dot(normal, b2.position - v1) - b2.shape.radius
        
        if s > 0:
            return
        
        if s > min_s:
            min_s = s
            min_axis = normal
    
    contact = arbiter.Contact()
    
    if min_axis == org_axis:
        contact.position = closest_vertex
    else:
        contact.position = (b2.position - min_axis * (b2.shape.radius + min_s))
    
    contact.separation = min_s

    arb.contacts.append(contact)
    arb.num_contacts += 1
    
    arb.normal = min_axis
    arb.tangent = math_utils.cross_vec2(1, min_axis)
    
    return True

def polygon_to_polygon(arb: Arbiter, b1: Body, b2: Body):
    pass

_funcs = [[circle_to_circle, circle_to_polygon], 
         [polygon_to_circle, polygon_to_polygon]]

def collide(arb: Arbiter, b1: Body, b2: Body):
    _funcs[b1.shape.get_type()][b2.shape.get_type()](arb, b1, b2)
###
#   testtank/testfood.py
#

import pygame
import time
from testentity import Entity

class TestFood(Entity):
    def __init__(self, grow_rate:float=0.10):
        super(TestFood, self).__init__()
        self.grow_rate:float = grow_rate
        self.growth:float = 0.0
        
    def update(self, timer):
        deltatime = timer - self.last_update
        if self.growth < 1.0: self.grow(deltatime)
        
        self.last_update = timer
        
    def grow(self, deltatime):
        self.growth += self.grow_rate * deltatime
        if self.growth > 1.0: self.grow = 1.0

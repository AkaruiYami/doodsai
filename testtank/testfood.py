###
#   testtank/testfood.py
#

import pygame
import time
from testentity import Entity

class TestFood(Entity):
    def __init__(self):
        super(TestFood, self).__init__()
        
    def update(self):
        self.grow()
        
    def grow(self):

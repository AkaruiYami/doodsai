import pygame
import time
from entity import Entity

class Food(Entity):
    def __init__(self, pos:tuple=(0, 0), growth_speed:float=0.01, scale:tuple[int, int]=(16, 16), speed_mult:float=1.0) -> None:
        super(Food, self).__init__()
        self.setImage(pygame.image.load("./assets/food_v1-01.png"), scale=scale)
        self.setScale(scale)        
        self.setPos((pos[0], pos[1]))
        
        self._speed_mult:float = speed_mult
        self._speed:float = growth_speed
        self._growth:float = 0.0
        self._energy:int = 1
        
        self._last_update:float = time.perf_counter()
        
    def update(self, u_time=0.0) -> None:
        deltatime:float = u_time - self._last_update
        self._last_update = u_time
        
        if self._growth < 1.0:
            self.grow(deltatime)

    def grow(self, deltatime) -> None:
        self._growth += self._speed * deltatime * self._speed_mult
        
        if self._growth > 1.0: self._growth = 1.0
        
        if self._growth == 1.0: 
            self._energy = 40
            self.setScale((16, 16))
        elif self._growth >= 0.75: 
            self._energy = 30
            self.setScale((12, 12))
        elif self._growth >= 0.50: 
            self._energy = 20
            self.setScale((8, 8))
        elif self._growth >= 0.25: 
            self._energy = 10
            self.setScale((4, 4))
        else:
            self._energy = 0
            self.setScale((0, 0))
    
    def getEnergy(self) -> int:
        return self._energy
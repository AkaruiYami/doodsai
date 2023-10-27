import pygame
import math
import time
from entity import Entity

class Dood(Entity):
    def __init__(self, pos:tuple=(100, 100), speed_mult:float=1.0, scale:tuple[int, int]=(32, 32)) -> None:
        super(Dood, self).__init__()
        self.setScale(scale)
        self.setImage(pygame.image.load("./assets/dood_v3-01.png").convert_alpha(), scale=scale)
        self.setPos((pos[0], pos[1]))
        
        self._speed_mult:float = speed_mult

        self.attrib_speed:float = 2.0
        self.attrib_size:float = 1.0
        self.attrib_sense:float = 1.0
        
        self._time_alive:float = 0.0
        
        self.last_update:float = time.perf_counter()
        
    def moveForward(self, deltatime:float) -> None:
        rotation_rad:float = math.radians(self.angle)
        x = self.getPos()[0] + math.cos(rotation_rad) * self.attrib_speed * deltatime * self._speed_mult
        y = self.getPos()[1] - math.sin(rotation_rad) * self.attrib_speed * deltatime * self._speed_mult
        self.setPos((x, y))

    def moveBackward(self, deltatime:float) -> None:
        rotation_rad:float = math.radians(self.angle)
        x = self.getPos()[0] + math.cos(rotation_rad) * -self.attrib_speed * deltatime * self._speed_mult
        y = self.getPos()[1] - math.sin(rotation_rad) * -self.attrib_speed * deltatime * self._speed_mult
        self.setPos((x, y))
   
    def turnLeft(self, deltatime:float) -> None:
        self.angle += (self.attrib_speed / 2) * deltatime * self._speed_mult
        if self.angle >= 360.01: self.angle -= 360
 
    def turnRight(self, deltatime:float) -> None:
        self.angle -= (self.attrib_speed / 2) * deltatime * self._speed_mult
        if self.angle <= 0.01: self.angle += 360

    def update(self, u_time:float=0.0) -> None:
        deltatime:float = u_time - self.last_update
        self.last_update:float = u_time
        
        # behaviors effect position, angle
        self.turnLeft(deltatime)
        self.moveForward(deltatime)
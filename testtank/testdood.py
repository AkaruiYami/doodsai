###
#   testtank/testdood.py
#
from testentity import Entity
import math

class TestDood(Entity):
    def __init__(self, pos:tuple[int, int]=(0, 0), scale:tuple[int, int]=(32, 32), speed_mult:float=1.0) -> None:
        super(TestDood, self).__init__()
        self.scale = scale
        self.image = "./assets/dood_v3-01.png"
        self.pos = pos

        self._attr_speed:float = 1.0
        self._attr_size:float = 1.0
        self._attr_sense:float = 1.0
        
        self._speed_mult = speed_mult        
        self._time_alive:float = 0.0
    
    def update(self, u_time:float) -> None:
        deltatime = u_time - self._last_update
        
        self.turnLeft(deltatime)
        self.moveForward(deltatime)
        
        self._last_update = u_time

    def moveForward(self, deltatime:float) -> None:
        rad = math.radians(self.angle)
        x = self.pos[0] + math.cos(rad) * self._attr_speed * deltatime * self._speed_mult
        y = self.pos[1] - math.sin(rad) * self._attr_speed * deltatime * self._speed_mult
        self.pos = (x, y)
        
    def moveBackward(self, deltatime:float) -> None:
        rad = math.radians(self.angle)
        x = self.pos[0] + math.cos(rad) * -(self._attr_speed/2) * deltatime * self._speed_mult
        y = self.pos[1] - math.sin(rad) * -(self._attr_speed/2) * deltatime * self._speed_mult
        self.pos = (x, y)
        
    def turnLeft(self, deltatime:float) -> None:
        self.angle -= self._attr_speed * deltatime * self._speed_mult

    def turnRight(self, deltatime:float) -> None:
        self.angle += self._attr_speed * deltatime * self._speed_mult
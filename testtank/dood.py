###
#   testtank/testdood.py
#
import detection_component as components
from testentity import Entity
from doodbrain import Brain
import math

class TestDood(Entity):
    def __init__(self, scale:tuple[int, int]=(32, 32), speed_mult:float=1.0) -> None:
        super(TestDood, self).__init__()
        self.scale = scale
        self.image = "./assets/dood_v3-01.png"
        self.origin = self.center

        self._attr_speed:float = 1.0
        self._attr_size:float = 1.0
        self._attr_sense:float = 1.0
        
        self._speed_mult = speed_mult        
        self._time_alive:float = 0.0
    
        self._moving_forward:bool = False
        self._moving_backward:bool = False
        self._moving_left:bool = False
        self._moving_right:bool = False
        
        # additional component
        self.area_detection = components.CircleAreaDetection(self, 35)

        # TODO Currently needing input callbacks and output callbacks
        #   these will probably be defines as self._state_<whatevers>
        #   ALSO probably need to start giving some states of awareness to process
        
        # Brain init
        inputs = []
        output = []
        self._brain = Brain(connections=10)
    
    @property
    def movingForward(self) -> bool:
        return self._moving_forward    
    @property
    def movingBackward(self) -> bool:
        return self._moving_backward
    @property
    def movingLeft(self) -> bool:
        return self._moving_left
    @property
    def movingRight(self) -> bool:
        return self._moving_right
    
    @movingForward.setter
    def movingForward(self, isit:bool) -> None:
        self._moving_forward = isit
    @movingBackward.setter
    def movingBackward(self, isit:bool) -> None:
        self_moving_backward = isit
    @movingLeft.setter
    def movingLeft(self, isit:bool) -> None:
        self._moving_left = isit
    @movingRight.setter
    def movingRight(self, isit:bool) -> None:
        self._moving_right = isit

    def update(self, u_time:float) -> None:
        deltatime = u_time - self._last_update
        
        if self._moving_forward: self.moveForward(deltatime)
        if self._moving_backward: self.moveBackward(deltatime)
        if self._moving_left: self.turnLeft(deltatime)
        if self._moving_right: self.turnRight(deltatime)
                
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

    def sayHello(self, other: Entity) -> None:
        '''Just placeholder method to see if can say hello to outside entity'''
        print(f"Dood say hello to {other}")
    
    def sayBye(self, other: Entity):
        print(f"Dood say bye bye to {other}")

###
#   testtank/testfood.py
#
from testentity import Entity

class TestFood(Entity):
    def __init__(self, grow_rate:float=0.10, max_energy:int=50, scale:tuple[int, int]=(16, 16)):
        super(TestFood, self).__init__()
        self.image = "./assets/food_v1-01.png"
        self.scale = scale
        self._grow_rate:float = grow_rate
        self._growth:float = 0.0
        self._energy:float = 0
        self._max_energy:float = max_energy
        
    def update(self, u_time):
        deltatime = u_time - self._last_update
        if self._growth < 1.0: self.grow(deltatime)
        
        self._last_update = u_time
        
    def grow(self, deltatime):
        self._growth += self._grow_rate * deltatime
        if self._growth > 1.0: self._growth = 1.0
        if self._growth == 1.0: # growth state 100%
            self._energy = self._max_energy
        elif self._growth >= 0.8: # growth state 80%
            self.scale = (0.8, 0.8)
            self._energy = self._max_energy * .8
        elif self._growth >= 0.6: # growth state 60%
            self.scale = (0.6, 0.6)
            self._energy = self._max_energy * .6
        elif self._growth >= 0.4: # grwoth state 40%
            self.scale = (0.4, 0.4)
            self._energy = self._max_energy * .4
        elif self._growth >= 0.2: # growth state 20%
            self.scale = (0.2, 0.2)
            self._energy = self._max_energy * 2
        elif self._growth >= 0.0: # growth state 0%
            self.scale = (0, 0)
            self._energy = 0
        else: # well thats an issue for future me.
            pass
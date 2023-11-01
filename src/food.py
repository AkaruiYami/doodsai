'''
    testtank/food.py
'''
from entity import Entity

class Food(Entity):
    '''
        Food sprite that grows at a set rate and contains energy based on
        growth. Just here for the Dood()s to eat.
    '''
    def __init__(self, grow_rate:float=0.01, max_energy:int=50,
                 scale:tuple[int, int]=(16, 16)):
        Entity.__init__(self, scale=scale)
        self.image = "./assets/food_v1-01.png"
        self._max_energy:float = max_energy
        self._grow_rate:float = grow_rate
        self._growth:float = 0.0
        self._energy:float = 0
        self.origin = self.center
        self.scale = (0, 0)
        
    @property
    def growth(self):
        '''Return current growth of Food().
        Returns float - value from 0.0 - 1.0'''
        return self._growth

    @property
    def energy(self):
        '''Return current energy of Food().
        Returns float - current energy value.'''
        return self._energy

    def update(self, u_time):
        '''update states of Food() given a time of call.
        @u_time:float - time of update() call.'''
        if not self.alive:
            self.kill()
        deltatime = u_time - self._last_update
        if self._growth < 1.0:
            self._grow(deltatime)
            self._last_update = u_time

    def _grow(self, deltatime):
        '''Grow the food the amount it should given the deltatime.
        @deltatime: float - value should be passed from update()'''
        self._growth += self._grow_rate * deltatime
        self._growth = min(self._growth, 1.0)
        
        growth_stages = [
            (1.0, (16, 16), self._max_energy),
            (0.8, (12, 12), self._max_energy * .8),
            (0.6, (9, 9), self._max_energy * .6),
            (0.4, (6, 6), self._max_energy * .4),
            (0.2, (3, 3), self._max_energy * .2),
            (0.0, (0, 0), 0)
        ]
        
        for growth, scale, energy in (growth_stages):
            if self._growth >= growth:
                self.scale = scale
                self._energy = energy
                break
'''
    src/tank.py
'''
import time

class Tank():
    '''
        Tank() contains the parameters of the tank. This would be better off
        called tank and might be changed in future commits.
    '''
    def __init__(self, size:tuple[int, int]=(200, 200), 
                 border_wall:bool=False,
                 food_spawn_rate:float=2.5,
                 food_limit:int=50,
                 dood_limit:int=50):
        self._size:tuple = size
        self._border_walled:bool = border_wall
        self._food_spawn_rate:float = food_spawn_rate
        self._food_spawn_timer:float = 0.0
        self._food_max:int = food_limit
        self._dood_max:int = dood_limit
        self._last_update:float = time.perf_counter()
        
    @property
    def size(self) -> tuple[int, int]:
        '''Returns the size of the tank. tuple[width, height]'''
        return self._size
    
    @size.setter
    def size(self, size:tuple[int, int]) -> None:
        '''Set the size of the tank.
        @size : tuple[width, height]'''
        self_size = size
    
    @property
    def width(self) -> int:
        '''Returns the width of the tank.'''
        return self._size[0]
    
    @property
    def height(self) -> int:
        '''Returns the height of the tank.'''
        return self._size[1]
    
    @property
    def borderWalled(self) -> bool:
        '''Returns True if border is walled, else False'''
        return self._border_walled
    
    @borderWalled.setter
    def borderWalled(self, isit:bool) -> None:
        '''Set if the border of the tank is walled.
        @isit: bool'''
        self._border_walled = isit
    
    @property
    def spawnRate(self) -> float:
        '''Returns the rate at which food should grow in seconds.'''
        return self._food_spawnrate
    
    @spawnRate.setter
    def spawnRate(self, seconds:float) -> None:
        '''Set the spawn rate in seconds of food within the tank.
        @seconds: float'''
        self._food_spawnrate = seconds

    @property
    def foodLimit(self) -> int:
        '''Get the max amount of food allowed in tank at one time.'''
        return self._food_max
    
    @foodLimit.setter
    def foodLimit(self, max:int) -> None:
        '''Set the max amount of food allowed in tank at one time.
        @max: int'''
        self._food_max = max
        
    @property
    def doodLimit(self) -> int:
        '''Get the max amount of doods allowed in tank at one time.'''
        return self._dood_max
    
    @doodLimit.setter
    def doodLimit(self, max:int) -> None:
        '''Set the max amount of doods allowed in tank at one time.
        @max: int'''
        self._dood_max = max
        
    def update(self, u_time):
        '''Call this during the main script update to update tank timers.'''
        deltatime = u_time - self._last_update
        self._food_spawn_timer += deltatime
        
        self._last_update = u_time
        
    def spawnFood(self) -> bool:
        '''Calling this will both tell the program to spawn a food, as well
        as update the spawner if returning True'''
        should_spawn = False
        if self._food_spawn_timer > self._food_spawn_rate:
            should_spawn = True
            self._food_spawn_timer = 0.0
        return should_spawn

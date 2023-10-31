'''
   testtank/testdood.py
'''
import detection_component as components
import math
import pygame.math
import utils
from brain import Brain
from entity import Entity
from food import Food

class Dood(Entity):
    '''TestDood class so I don't break the Dood class.
    Consists of attributes, behaviors, and functions of Dood().'''

    def __init__(self, scale:tuple[int, int]=(32, 32),
                 speed_mult:float=1.0, sense_range:int=35,
                 neurons:int=10) -> None:
        super().__init__()
        self.scale = scale
        self.image = "./assets/dood_v3-01.png"
        self.origin = self.center
        self._speed_mult = speed_mult

        # 'Physical' attributes
        self._attr_speed:float = 1.0
        self._attr_size:float = 1.0
        self._attr_sense:float = 1.0
        self.area_detection = components.CircleAreaDetection(self, sense_range * self._attr_sense)

        # Internal Attributes // senses
        self._energy:float = 100.0
        self._max_energy:float = 200.0
        self._dist_to_food:float = -1 # -1 if no food,
        self._dist_to_dood:float = -1 # -1 if no dood
        self._dir_to_food:float = -1 # if no food
        self._dir_to_dood:float = -1 # if no dood
        self._time_reset_chronometer_a:float = 60.0
        self._time_reset_osc_a:float = 3.0

        # Internal timers
        self._time_alive:float = 0.0
        self._time_since_last_ate:float = 0.0
        self._time_chronometer_a:float = 0.0
        self._time_osc_a:float = 0.0

        # Physical States
        self._moving_forward:bool = False
        self._moving_backward:bool = False
        self._moving_left:bool = False
        self._moving_right:bool = False

        # TODO Currently needing input callbacks and output callbacks
        # Brain init
        inputs = [
            self.getStateAngleToFood,
            self.getStateDistToFood,
            self.getStateTimeAlive,
            self.getStateTimeSinceAte,
            self.getStateTimeChronometerA,
            self.getStateTimeOscA
            ]
        outputs = [
            self.setMovingForward,
            self.setMovingBackward,
            self.setMovingLeft,
            self.setMovingRight
            ]
        self._brain = Brain(connections=neurons, 
                            inputs=inputs, outputs=outputs, new=True)

    @property
    def size(self):
        '''Return a float for Dood() attribute size.'''
        return self._attr_size

    @property
    def speed(self):
        '''Return a float for Dood() attribute speed.'''
        return self._attr_speed

    @property
    def sense(self):
        '''Return a float for Dood() atttribute sense.'''
        return self._attr_sense

    @property
    def movingForward(self) -> bool:
        '''Return bool for state of moving forward.'''
        return self._moving_forward

    @property
    def movingBackward(self) -> bool:
        '''Return bool for state of moving backward.'''
        return self._moving_backward

    @property
    def movingLeft(self) -> bool:
        '''Return bool for state of turning left (counter-clockwise).'''
        return self._moving_left

    @property
    def movingRight(self) -> bool:
        '''Return bool for state of turning right (clockwise).'''
        return self._moving_right

    def setMovingForward(self, isit:bool) -> None:
        '''Set state of moving Forward.
        @isit: bool'''
        self._moving_forward = isit

    def setMovingBackward(self, isit:bool) -> None:
        '''Set state of moving backward.
        @isit: bool'''
        self._moving_backward = isit

    def setMovingLeft(self, isit:bool) -> None:
        '''Set state of moving left (counter-clockwise).
        @isit: bool'''
        self._moving_left = isit

    def setMovingRight(self, isit:bool) -> None:
        '''Set state of turning right (clockwise).
        @isit: bool'''
        self._moving_right = isit

    def update(self, u_time:float) -> None:
        '''Update states on every call, require an update time.
        Calculates time from last update to current call.
        @u_time:float'''
        if self._energy <= 0:
            self.kill() # remove self from spritegroup a.k.a ded
            
        if self.alive:
            deltatime = u_time - self._last_update 

            if self.movingForward:
                self._moveForward(deltatime)
            if self.movingBackward:
                self._moveBackward(deltatime)
            if self.movingLeft:
                self._turnLeft(deltatime)
            if self.movingRight:
                self._turnRight(deltatime)

            self._time_alive += deltatime
            self._time_since_last_ate += deltatime        
            self._time_chronometer_a += deltatime
            self._time_osc_a += deltatime

            self._time_osc_a %= self._time_reset_osc_a
            self._time_chronometer_a %= self._time_reset_chronometer_a

            self._last_update = u_time
            self._spendEnergy(deltatime)
            
            self._brain.process()

    def collision(self, entity:Entity):
        if isinstance(entity, Food):
            self.eatFood(entity.energy)

    ### BEHAVIORS
    def eatFood(self, value:float):
        '''Called when a Dood() bumps into a Food() object. Retrieves
        value of energy stored within that Food().
        @value: float - obtained from Food().energy'''
        self._energy += value
        self._energy = min(self._energy, self._max_energy)
        self._time_since_last_ate = 0.0

    def _moveForward(self, deltatime:float) -> None:
        '''Update position of Dood() based on angle we are traveling forward.
        @deltatime: float - recieved during Dood.update() call'''
        rad = math.radians(self.angle)
        delta_dist = self._attr_speed * deltatime * self._speed_mult
        x = self.pos[0] + math.cos(rad) * delta_dist
        y = self.pos[1] - math.sin(rad) * delta_dist
        self.pos = (x, y)

    def _moveBackward(self, deltatime:float) -> None:
        '''Update position of Dood() based on angle we are traveling backward.
        @deltatime: float - recieved during Dood.update() call'''
        rad = math.radians(self.angle)
        delta_dist = (self._attr_speed/2) * deltatime * self._speed_mult
        x = self.pos[0] + math.cos(rad) * delta_dist
        y = self.pos[1] - math.sin(rad) * -delta_dist
        self.pos = (x, y)

    def _turnLeft(self, deltatime:float) -> None:
        '''Update angle of Dood() to the left (counter-clockwise).
        @deltatime: float - recieved during Dood.update() call.'''
        self.angle -= self._attr_speed * deltatime * self._speed_mult

    def _turnRight(self, deltatime:float) -> None:
        '''Update angle of Dood() to the right (clock-wise).
        @deltatime: float - recived during Dood.update() call.'''
        self.angle += self._attr_speed * deltatime * self._speed_mult

    def sayHello(self, other: Entity) -> None:
        '''Just placeholder method to see if can say hello to outside entity'''
        print(f"Dood say hello to {other}")

    def sayBye(self, other: Entity):
        print(f"Dood say bye bye to {other}")

    def _spendEnergy(self, deltatime:float) -> None:
        '''Spend energy to live, more if self is moving and burning that energy.'''
        if self.movingBackward or self.movingForward or self.movingLeft or self.movingRight:
            self._energy -= deltatime * 1.10 * self._attr_speed
        else:
            self._energy -= deltatime 
        
    ### STATES --
    # not properties so they can be called back by children instances
    # (ie the Brain())
    def getStateDistToFood(self) -> float:
        '''Get distance of self to nearest Food().
        Returns float.'''
        valid_ents = [ent for ent in self.area_detection.entities_inside if isinstance(ent, Food)]
        return -1 if not valid_ents else min([math.dist(e.pos, self.pos) for e in valid_ents])

    def getStateDistToDood(self) -> float:
        '''Get disntance of self to nearest Dood().
        Returns float.'''
        valid_ents = [ent for ent in self.area_detection.entities_inside if isinstance(ent, Dood)]
        return -1 if not valid_ents else min([math.dist(valid_ents.pos, self.pos) for e in valid_ents])

    def  getStateAngleToFood(self) -> float:
        '''Get angle to the nearest food. Not relative to self.angle'''
        valid_ents = [ent for ent in self.area_detection.entities_inside if isinstance(ent, Food)]
        valid_ents.sort(key=lambda e: math.dist(self.pos, e.pos))
        return pygame.math.Vector2(self.pos).angle_to(valid_ents[0].pos) if valid_ents else self.angle

    def getStateAngleToDood(self) -> float:
        '''Get angle to the nearest dood. Not relative to self.angle'''
        valid_ents = [ent for ent in self.area_detection.entities_inside if isinstance(ent, Dood)]
        valid_ents.sort(key=lambda e: math.dist(self.pos, e.pos))
        return pygame.math.Vector2(self.pos).angle_to(valid_ents[0].pos) if valid_ents else self.angle

    def getStateTimeAlive(self) -> float:
        '''Get time in milliseconds self has been alive since init().
        Returns float.'''
        return self._time_alive

    def getStateTimeSinceAte(self) -> float:
        '''Get time in milliseconds since last time self has bumped into food
        Returns float.'''
        return self._time_since_last_ate

    def getStateTimeChronometerA(self) -> float:
        '''Get self time of chronometer in milliseconds.
        Returns float.'''
        return utils.normalize(self._time_chronometer_a, 0, self._time_reset_chronometer_a)

    def getStateTimeOscA(self) -> float:
        '''Get self time of oscilator in milliseconds.
        Returns float.'''
        return utils.normalize(self._time_osc_a, 0, self._time_reset_osc_a)

    def getStateMovingForward(self) -> float:
        '''Get state of self moving forward.
        Returns bool.'''
        return self._moving_forward

    def getStateMovingBackward(self) -> float:
        '''Get state of self moving backward.
        Returns bool.'''
        return self._moving_backward

    def getStateMovingLeft(self) -> float:
        '''Get state of self turning left (counter-clockwise).
        Returns bool.'''
        return self._moving_left

    def getStateMovingRight(self) -> float:
        '''Get state of self turning right (clock-wise).
        Returns bool.'''
        return self._moving_right

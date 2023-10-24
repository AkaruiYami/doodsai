import pygame
import math
import time

class Dood(pygame.sprite.Sprite):
    def __init__(self, pos:tuple=(100, 100), speed_mult:float=1.0) -> None:
        super(Dood, self).__init__()
        self._speed_mult:float = speed_mult
        self.base_image:pygame.image = pygame.image.load("./assets/dood_v3-01.png").convert_alpha()
        self.base_image:pygame.image = pygame.transform.scale(self.base_image, (32, 32))
        self.rect:pygame.Rect = self.base_image.get_rect()
        
        self.body_mask = pygame.mask.from_surface(self.base_image)
        
        self.pos_x:float = pos[0]
        self.pos_y:float = pos[1]
        self.center_x:float = (self.base_image.get_width()/2) + self.pos_x
        self.center_y:float = (self.base_image.get_height()/2) + self.pos_y
        
        self.attrib_speed:float = 2.0
        self.attrib_sense:float = 1.0
        self.attrib_size:float = 1.0
        
        self.state_direction:float = 0.0
        
        self._time_alive:float = 0.0
        
        self.last_update:float = time.perf_counter()
            
    def render(self) -> (pygame.image, pygame.Surface):
        rotated_image:pygame.image = pygame.transform.rotate(self.base_image, self.state_direction)
        new_rect:pygame.Rect = rotated_image.get_rect(center=self.base_image.get_rect(center=((self.base_image.get_width()/2) + self.pos_x, (self.base_image.get_height()/2) + self.pos_y)).center)
        self.body_mask = pygame.mask.from_surface(rotated_image)
        
        return (rotated_image, new_rect)
    
    def update(self, u_time:float=0.0) -> None:
        deltatime:float = u_time - self.last_update
        self.last_update:float = u_time
        
        # behaviors effect position, angle
        self.turnLeft(deltatime)
        self.moveForward(deltatime)

    def moveForward(self, deltatime:float) -> None:
        rotation_rad:float = math.radians(self.state_direction)
        self.pos_x += math.cos(rotation_rad) * self.attrib_speed * deltatime * self._speed_mult
        self.pos_y -= math.sin(rotation_rad) * self.attrib_speed * deltatime * self._speed_mult

    def moveBackward(self, deltatime:float) -> None:
        rotation_rad:float = math.radians(self.state_direction)
        self.pos_x += math.cos(rotation_rad) * -self.attrib_speed * deltatime * self._speed_mult
        self.pos_y -= math.sin(rotation_rad) * -self.attrib_speed * deltatime * self._speed_mult
   
    def turnLeft(self, deltatime:float) -> None:
        self.state_direction += (self.attrib_speed / 2) * deltatime * self._speed_mult
        if self.state_direction >= 360.01: self.state_direction -= 360
 
    def turnRight(self, deltatime:float) -> None:
        self.state_direction -= (self.attrib_speed / 2) * deltatime * self._speed_mult
        if self.state_direction <= 0.01: self.state_direction += 360

    def getPos(self) -> tuple:
        return ((self.base_image.get_width()/2) + self.pos_x, (self.base_image.get_height()/2) + self.pos_y)
    
    def getRect(self) -> pygame.Rect:
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        return self.rect
        
    def drawMask(self) -> None:
        rotated_image:pygame.image = pygame.transform.rotate(self.base_image, self.state_direction)
        new_surf = pygame.surface.Surface(size=(rotated_image.get_width(), rotated_image.get_height()))
        for y in range(self.body_mask.get_size()[1]):
            for x in range(self.body_mask.get_size()[0]):
                if self.body_mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, (255, 0, 0, 250), (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
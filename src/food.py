import pygame
import time

class Food(pygame.sprite.Sprite):
    def __init__(self, pos:tuple=(0, 0), growth_speed:float=0.01, speed_mult:float=1.0) -> None:
        super(Food, self).__init__()
        
        self.base_image:pygame.image = pygame.image.load("./assets/food_v1-01.png")
        self.base_image = pygame.transform.scale(self.base_image, (32, 32))
        self.base_rect:pygame.Rect = self.base_image.get_rect()
        
        self.body_mask:pygame.mask = pygame.mask.from_surface(self.base_image)
        
        self.pos_x:float = pos[0]
        self.pos_y:float = pos[1]
        
        self._speed_mult:float = speed_mult
        self._speed:float = growth_speed
        self._growth:float = 0.0
        self._last_update:float = time.perf_counter()
        
    def render(self) -> None:
        image:pygame.image = self.base_image
        
        if self._growth == 1.0:
            image = pygame.transform.scale(self.base_image, (16, 16))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.75:
            image = pygame.transform.scale(self.base_image, (12, 12))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.50:
            image = pygame.transform.scale(self.base_image, (8, 8))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.25:
            image = pygame.transform.scale(self.base_image, (4, 4))
            self.body_mask = pygame.mask.from_surface(image)
        else:
            image = pygame.transform.scale(self.base_image, (0, 0))
            self.body_mask = pygame.mask.from_surface(image)
            
        return (image, image.get_rect(center=self.base_image.get_rect(center=((self.base_image.get_width()/2) + self.pos_x, (self.base_image.get_height()/2) + self.pos_y)).center))

    def update(self, u_time=0.0) -> None:
        deltatime:float = u_time - self._last_update
        self._last_update = u_time
        if self._growth < 1.0:
            self.grow(deltatime)

    def grow(self, deltatime) -> None:
        self._growth += self._speed * deltatime * self._speed_mult
        if self._growth > 1.0: self._growth = 1.0
    
    def drawMask(self) -> None:
        image:pygame.image = self.base_image
        if self._growth == 1.0:
            image = pygame.transform.scale(self.base_image, (16, 16))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.75:
            image = pygame.transform.scale(self.base_image, (12, 12))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.50:
            image = pygame.transform.scale(self.base_image, (8, 8))
            self.body_mask = pygame.mask.from_surface(image)
        elif self._growth >= 0.25:
            image = pygame.transform.scale(self.base_image, (4, 4))
            self.body_mask = pygame.mask.from_surface(image)
        else:
            image = pygame.transform.scale(self.base_image, (0, 0))
            self.body_mask = pygame.mask.from_surface(image)
        new_surf = pygame.surface.Surface(size=(image.get_width(), image.get_height()))
        for y in range(self.body_mask.get_size()[1]):
            for x in range(self.body_mask.get_size()[0]):
                if self.body_mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, (255, 0, 0), (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf

    def getRect(self) -> pygame.Rect:
        self.base_rect.x = self.pos_x
        self.base_rect.y = self.pos_y
        return self.base_rect
    
    def getPos(self) -> tuple:
        return ((self.base_image.get_width()/2) + self.pos_x, (self.base_image.get_height()/2) + self.pos_y)
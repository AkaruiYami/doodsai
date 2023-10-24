import pygame
import time

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.base_image:pygame.image = None
        self.base_rect:pygame.Rect = None
        self.base_mask:pygame.mask = None
        
        self.pos_x:float = 0
        self.pos_y:float = 0
        self.angle:float = 0
    
    def setPos(self, pos:tuple=(0, 0)) -> None:
        self.pos_x = pos[0] + (self.base_image.get_width()/2)
        self.pos_y = pos[1] + (self.base_image.get_height()/2)
    
    def setAngle(self, angle) -> None:
        self.angle = angle if angle <= 360 and angle <= 0 else 0
    
    def getPos(self) -> tuple:
        return (self.pos_x, self.pos_y)
    
    def getAngle(self) -> float:
        return self.angle
    
    def getRect(self) -> pygame.Rect:
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        return self.rect
        
    def drawMask(self) -> None:
        image:pygame.image = pygame.transform.rotate(self.base_image, self.angle)
        new_surf = pygame.surface.Surface(size=(image.get_width(), image.get_height()))
        for y in range(self.body_mask.get_size()[1]):
            for x in range(self.body_mask.get_size()[0]):
                if self.body_mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, (255, 0, 0), (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
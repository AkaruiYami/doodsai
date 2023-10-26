import pygame
import time

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.base_image:pygame.image = None
        self._rect:pygame.Rect = None
        self.base_mask:pygame.mask = None    
        self.pos_x:float = 0
        self.pos_y:float = 0
        self.angle:float = 0
        self.scale:tuple[int, int] = (0, 0)
        self.alive = True

    @property
    def mask(self):
        return self.getMask()

    @property
    def rect(self):
        return self.getRect()

    def setPos(self, pos:tuple[int, int]=(0, 0)) -> None:
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        
    def setAngle(self, angle) -> None:
        self.angle = angle if angle >= 360 and angle <= 0 else 0
    
    def setMask(self, mask:pygame.mask) -> None:
        self.base_mask = mask
    
    def setScale(self, scale:tuple[int, int]) -> None:
        self.scale = scale
    
    def setImage(self, image:pygame.surface.Surface, scale:tuple[float, float]) -> None:
        self.base_image = pygame.transform.scale(image, (scale[0], scale[1]))
        self._rect = self.base_image.get_rect()
    
    def getScale(self) -> tuple[float, float]:
        return self.scale
    
    def getPos(self) -> tuple[float, float]:
        return (self.pos_x, self.pos_y)
    
    def getAngle(self) -> float:
        return self.angle

    def getMask(self) -> pygame.mask:
        mask = pygame.mask.from_surface(self.getImage())
        return mask
    
    def getRect(self) -> pygame.Rect:
        image = self.getImage()
        return image.get_rect(center=self.base_image.get_rect(
            center=((self.base_image.get_width()/2) + self.pos_x, (self.base_image.get_height()/2) + self.pos_y)
            ).center)

    def getImage(self) -> pygame.surface.Surface:
        image = pygame.transform.scale(self.base_image, self.scale)
        image = pygame.transform.rotate(image, self.angle)
        return image
    
    def render(self) -> tuple[pygame.Surface, pygame.Rect]:
        return (self.getImage(), self.getRect())
    
    def drawMask(self) -> pygame.Surface:
        image = self.getImage()
        new_surf = pygame.surface.Surface(size=(image.get_width(), image.get_height()))
        mask = self.getMask()
        for y in range(mask.get_size()[1]):
            for x in range(mask.get_size()[0]):
                if mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, (255, 0, 0), (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
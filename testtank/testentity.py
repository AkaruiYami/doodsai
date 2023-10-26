import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        
        self.base_image:pygame.Surface = None
        self.base_rect:pygame.Rect = None
        self.base_mask:pygame.mask = None
        
        self.scale:tuple[float, float] = (1, 1)
        self.pos:tuple[float, float] = (0, 0)
        self.pos_center:tuple[float, float] = (0, 0)
        self.angle:float = 0.0
        
    def setPos(self, pos:tuple[int, int]=(0,0)) -> None:
        pass

    def getPos(self) -> tuple[int, int]:
        return self.pos()

    def setImage(self):
        pass
    
    def getImage(self):
        return self.base_image()
    
    def setRect(self):
        pass

    def getRect(self):
        return self.rect

    def setAngle(self, angle:float):
        if angle >= 0 and angle <= 360: 
            self.angle = angle
            if self.angle > 360: self.angle - 360
            if self.angle < 0: self.angle + 360
        else:
            raise Exception("setAngle must be float between 0 and 360")

    def getAngle(self):
        return self.angle
        
    def setMask(self):
        pass

    def getMask(self):
        return self.base_mask

    def drawMask(self):
        pass

    def render(self):
        pass
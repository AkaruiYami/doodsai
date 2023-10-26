import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, image_path:str="", pos:tuple[float, float]=(0.0, 0.0), scale:tuple[float, float]=(1.0, 1.0)):
        super(Entity, self).__init__()
        
        self._base_image:pygame.Surface = None
        self._base_rect:pygame.Rect = None
        self._base_mask:pygame.mask = None
        
        self._scale:tuple[float, float] = (1, 1)
        self._pos:tuple[float, float] = (0, 0)
        self._center:tuple[float, float] = (0, 0)
        self._angle:float = 0.0
        
        self._last_update:float = 0.0
         
    @property
    def pos(self) -> tuple[float, float]:
        return self.pos()
    
    @property.setter       
    def pos(self, pos:tuple[float, float]=(0,0)) -> None:
        self.pos = pos
    
    @property
    def image(self) -> pygame.Surface:
        image = pygame.transform.rotate(self.base_image, self.angle)
        return image
    
    @property.setter
    def image(self, image_path:str="", scale:tuple[float, float]=(1, 1)):
        self.base_image = pygame.image.load(image_path)
        rescale_x = pygame.transform.scale(self.base_image.get_width() * scale[0])
        rescale_y = pygame.transform.scale(self.base_image.get_height() * scale[1])
        self.base_image = pygame.transform.scale((rescale_x, rescale_y))
    
    @property
    def rect(self) -> pygame.Rect:
        return self.base_rect
    
    @property.setter
    def rect(self) -> None:
        self.base_rect = self.base_image.get_rect()

    @property
    def angle(self) -> float:
        return self.angle

    @property.setter
    def angle(self, angle:float) -> None:
        if not 0 <= angle <= 360: 
            raise Exception("setAngle(float) must be float between 0 and 360")
        self.angle = angle
        self.angle = 360

    @property
    def mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(pygame.transform.rotate(self.base_image, self.angle))

    def drawMask(self, color:tuple[int, int, int, int]=(255, 0, 0, 255)):
        image = pygame.transform.rotate(self.base_image, self.angle)
        new_surf = pygame.surface.Surface((image.get_width(), image.get_height()))
        mask = pygame.mask.from_surface(image)
        for y in range(mask.get_size()[1]):
            for x in range(mask.get_size()[0]):
                if mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, color, (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
        
    def render(self) -> tuple[pygame.Surface, pygame.Rect]:
        pass
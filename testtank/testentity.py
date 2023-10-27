import pygame
import time

class Entity(pygame.sprite.Sprite):
    def __init__(self, position:tuple[int, int]=(0, 0), scale:tuple[int, int]=(32, 32)):
        super(Entity, self).__init__()        
        self._filepath:str = None
        self._base_image:pygame.Surface = None
        self._scale:tuple[int, int] = scale
        self._pos:tuple[int, int] = position
        self._origin:tuple[float, float] = (0, 0)
        self._angle:float = 0.0
        self._last_update:float = time.perf_counter()
    
    @property
    def size(self) -> tuple[int, int]:
         return (self.image.get_width(), self.image.get_height())
        
    @property
    def pos(self) -> tuple[int, int]:
        return self._pos
    
    @pos.setter       
    def pos(self, pos:tuple[int, int]=(0,0)) -> None:
        self._pos = pos
    
    @property
    def center(self) -> tuple[int, int]:
        center_x = self._pos[0] - (self.image.get_width()/2)
        center_y = self._pos[1] - (self.image.get_height()/2)
        return (center_x, center_y)
    
    @property
    def origin(self):
        return self._origin
    
    @origin.setter
    def origin(self, origin_offset:tuple[float, float]=(0, 0)) -> None:
        self._origin = origin_offset
    
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, scale:tuple[int, int]=(32, 32)):
        self._scale = scale
    
    @property
    def image(self) -> pygame.Surface:
        image = pygame.transform.scale(self._base_image, self._scale)
        image = pygame.transform.rotate(image, self._angle)
        return image
    
    @image.setter
    def image(self, image_path:str="") -> None:
        self._filepath = image_path
        self._base_image = pygame.image.load(image_path).convert_alpha()
        self._base_image = pygame.transform.scale(self._base_image, self.scale)
        rescale_x = int(self._base_image.get_width() * self._scale[0])
        rescale_y = int(self._base_image.get_height() * self._scale[1])
        self._base_image = pygame.transform.scale(self._base_image, (rescale_x, rescale_y))
    
    @property
    def rect(self) -> pygame.rect.Rect:
        return self.image.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, angle:float) -> None:
        self._angle = angle
        self._angle = self._angle % 360

    @property
    def mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(pygame.transform.rotate(self._base_image, self._angle))

    def drawMask(self, color:tuple[int, int, int, int]=(255, 0, 0, 255)):
        image = pygame.transform.rotate(self._base_image, self._angle)
        new_surf = pygame.surface.Surface((image.get_width(), image.get_height()))
        mask = pygame.mask.from_surface(image)
        for y in range(mask.get_size()[1]):
            for x in range(mask.get_size()[0]):
                if mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, color, (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
        
    def render(self) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
        return (self.image(), self.rect())
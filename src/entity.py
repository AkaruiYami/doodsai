'''
    testtank/entity.py
'''
import time
import pygame

class Entity(pygame.sprite.Sprite):
    '''Base class for entities within the tank. Doods, Foods, etc..
    Inherits from pygame.sprite.Sprite()
'''
    def __init__(self, position:tuple[int, int]=(0, 0), scale:tuple[int, int]=(32, 32)):
        super().__init__()
        self._filepath:str = None
        self._base_image:pygame.Surface = pygame.surface.Surface((0, 0))
        self._curr_image:pygame.Surface = None
        self._scale:tuple[int, int] = scale
        self._pos:tuple[int, int] = position
        self._origin:tuple[float, float] = (0, 0)
        self._angle:float = 0.0
        self._last_update:float = time.perf_counter()
        self._rect = None
        self.alive = True

    @property
    def size(self) -> tuple[int, int]:
        '''Get the current size of the entity.
        Returns tuple(int, int) - width and height.'''
        return (self.image.get_width(), self.image.get_height())

    @property
    def width(self) -> int:
        '''Return the width of the current image.'''
        return self.image.get_width()
    
    @property
    def height(self) -> int:
        '''Return the height of the current image.'''
        return self.image.get_height()

    @property
    def pos(self) -> tuple[int, int]:
        '''Get the current position of the entity at top-left corner.
        Returns tuple(int, int) - x-coord, y-coord.'''
        return self._pos

    @pos.setter
    def pos(self, pos:tuple[int, int]=(0,0)) -> None:
        '''Set the current position of the entity.
        @pos:tuple(int, int) - width and height.'''
        self._pos = pos

    @property
    def center(self) -> tuple[int, int]:
        '''Get the current posiiton of the entity at the center.
        Returns tuple(int, int) - x-coord, y-coord.'''
        center_x = self._pos[0] - (self.image.get_width()/2)
        center_y = self._pos[1] - (self.image.get_height()/2)
        return (center_x, center_y)

    @property
    def origin(self) -> tuple[int, int]:
        '''Get current position offset of the entity.
        Returns a tuple(int, int) - x-coord, y-coord'''
        return self._origin

    @origin.setter
    def origin(self, origin_offset:tuple[int, int]=(0, 0)) -> None:
        '''Set the current position offset of the entity.
        @origin_offset: tuple(int, int) - x-coord, y-coord'''
        self._origin = origin_offset

    @property
    def scale(self):
        '''Get current scale of the entity.
        Returns tuple(int, int) - width, height'''
        return self._scale

    @scale.setter
    def scale(self, scale:tuple[int, int]=(32, 32)):
        '''Set current scale of the entity.
        @scale : tuple(int, int) - width, height'''
        self._scale = scale
        self._curr_image = pygame.transform.scale(self._base_image, scale)

    @property
    def image(self) -> pygame.Surface:
        '''Get image surface of entity at the set angle.
        Returns pygame.Surface - stored image after rotation of angle.'''
        image = pygame.transform.rotate(self._curr_image, self._angle)
        return image
    
    @image.setter
    def image(self, image_path:str="") -> None:
        '''Set the image of the entity to the given filepath of image.
        Alpha layer in image is converted to transparency, and image is scaled
        to the initial scale.
        Sets both _base_image, _filepath, and current pygame.Rect() of created
        image.
        @image_path: str - filepath and name to assets image.
        '''
        self._filepath = image_path
        image = pygame.image.load(image_path).convert_alpha()
        self._base_image = image
        self._curr_image = pygame.transform.scale(image, self.scale)
        # self._rect = image.get_rect()

    @property
    def rect(self) -> pygame.Rect:
        '''Get the current rect of most recent image at current angle and scale.
        Return pygame.Rect()'''
        image = self.image
        self._rect = image.get_rect()
        return image.get_rect(center=image.get_rect(
            center=self.center
        ).center)

    @property
    def angle(self) -> float:
        '''Get current rotation angle of entity image.
        Returns float - value between 0.0 and 359.9 inclusive.'''
        return self._angle

    @angle.setter
    def angle(self, angle:float) -> None:
        '''Set the angle of entity image.
        @angle: float - corrects to value between 0.0 and 359.9 inclusive.'''
        self._angle = angle
        self._angle = self._angle % 360

    @property
    def mask(self) -> pygame.mask.Mask:
        '''Get mask for current image at angle.
        Returns pygame.mask.Mask'''
        return pygame.mask.from_surface(pygame.transform.rotate(self.image, self._angle))

    def drawMask(self, color:tuple[int, int, int, int]=(255, 0, 0)) -> pygame.Surface:
        '''Draw pixel perfect collision mask of entity current image.'''
        image = self.image
        new_surf = pygame.Surface(size=(image.get_width(), image.get_height()))
        mask = pygame.mask.from_surface(image)
        for y in range(mask.get_size()[1]):
            for x in range(mask.get_size()[0]):
                if mask.get_at((x, y)):
                    pygame.draw.rect(new_surf, color, (x, y, 1, 1))
        new_surf.set_colorkey((0, 0, 0))
        return new_surf
    
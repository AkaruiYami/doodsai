from abc import ABC, abstractmethod

import pygame


class Widget(ABC):
    def __init__(self, rect, *args, **kwargs):
        self.rect = pygame.Rect(*rect)
        super().__init__()
        self.image = None

    @property
    def pos(self) -> pygame.Vector2:
        """Get the position of the widget"""
        return pygame.Vector2(self.rect.x, self.rect.y)

    @pos.setter
    def pos(self, pos: tuple[float, float]):
        """Set the position of the widget"""
        x, y = pos
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen: pygame.Surface):
        "Draw the widget on the given surface if image is initialized"
        if not self.image:
            screen.blit(self.image, self.pos)
        else:
            # NOTE: I might need to remove this.
            print(
                f"{self} image is None. You might forgot to initialize the widget image"
            )

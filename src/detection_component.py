from abc import ABC, abstractmethod

from entity import Entity


class BaseAreaDetection(ABC):
    def __init__(self, body: Entity):
        self.body: Entity = body
        self.entities_inside: set[Entity] = set()

    @abstractmethod
    def enterArea(self, body: Entity) -> bool:
        """Return True if an Entity enter the area"""
        ...

    @abstractmethod
    def leaveArea(self, body: Entity) -> bool:
        """Return True if an Entity leave the area"""
        ...

class CircleAreaDetection(BaseAreaDetection):
    def __init__(self, body: Entity, radius: float):
        super().__init__(body)
        self.radius: float = radius

    def enterArea(self, other: Entity) -> bool:
        if self.body == other:
            return False

        if self._isin_x(other) and self._isin_y(other) and other not in self.entities_inside:
            self.entities_inside.add(other)
            return True
        return False
    
    def leaveArea(self, other: Entity) -> bool:
        if self.body == other:
            return False

        if not (self._isin_x(other) and self._isin_y(other)) and other in self.entities_inside:
            self.entities_inside.remove(other)
            return True
        return False

    def _isin_x(self, other: Entity):
        pos = self.body.pos[0]
        x_range = (pos - self.radius, pos + self.radius)
        left = x_range[0] < other.rect.left < x_range[1]
        right = x_range[0] < other.rect.right < x_range[1]
        return left or right

    def _isin_y(self, other: Entity):
        pos = self.body.pos[1]
        y_range = (pos - self.radius, pos + self.radius)
        top = y_range[0] < other.rect.top < y_range[1]
        bottom = y_range[0] < other.rect.bottom < y_range[1]
        return top or bottom

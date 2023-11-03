from typing import Optional, Callable, Iterable, Any, Union

import pygame

from .widget import Widget
from ._common import _ButtonState, _ColorMap, _Color, _Rect

DEFAULT_BACKGROUND_COLOR = {
    "normal": (192, 192, 192),
    "active": (128, 128, 128),
    "hover": (160, 160, 160),
    "disable": (224, 224, 224),
}
DEFAULT_FOREGROUND_COLOR = {
    "normal": (32, 32, 32),
    "active": (224, 224, 224),
    "hover": (0, 0, 0),
    "disable": (192, 192, 192),
}

pygame.font.init()


class Button(Widget):
    def __init__(
        self,
        text: str,
        rect: _Rect,
        font_size: int = 12,
        font_type: Optional[pygame.font.Font] = None,
        state: _ButtonState = "normal",
        command: Optional[Callable] = None,
        background_color: Union[_Color, _ColorMap, None] = None,
        foreground_color: Union[_Color, _ColorMap, None] = None,
        **kwargs,
    ):
        super().__init__(rect, **kwargs)
        self.text = text
        if font_type is None:
            font_type = pygame.font.SysFont("arial", font_size)
        self.font = font_type
        self.state = state
        self.command = command
        self.background_color = self._parse_color_map(
            background_color, DEFAULT_BACKGROUND_COLOR
        )
        self.foreground_color = self._parse_color_map(
            foreground_color, DEFAULT_FOREGROUND_COLOR
        )

        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self._draw_button()

    def click(self, *args, **kwargs) -> Any:
        """If widget is hovered, then try to call the command"""
        if self.ishovered and self.state != "disable":
            if self.command is None:
                return
            return self.command(*args, **kwargs)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button, update the sprite base on button's state"""
        if self.state == "disable":
            self._draw_button()
            super().draw(screen)
            return

        if any(pygame.mouse.get_pressed()) and self.ishovered:
            self.state = "active"
        elif self.ishovered:
            self.state = "hover"
        else:
            self.state = "normal"
        self._draw_button()

        super().draw(screen)

    @property
    def ishovered(self) -> bool:
        "Check if the cursor is on the button rect"
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def _draw_button(self) -> None:
        """Draw the whole button"""
        self.image.fill(self.background_color[self.state])
        self._draw_text()

    def _draw_text(self) -> None:
        """Slap text onto the button"""
        txt = self.font.render(self.text, True, self.foreground_color[self.state])
        txt_rect = txt.get_rect(center=(self.rect.w / 2, self.rect.h / 2))
        self.image.blit(txt, txt_rect)

    def _parse_color_map(
        self,
        val: Optional[Union[Iterable, dict[str, _Color]]],
        default: dict[str, _Color],
    ) -> dict[str, _Color]:
        """Convert the given value into proper color map matching the button states.
        Any missing color will be set to default"""
        if val is None:
            return default

        if isinstance(val, Iterable) and not isinstance(val, dict):
            if isinstance(val[0], int):
                val = [val]
            val = dict(zip(default.keys(), val))

        if isinstance(val, dict):
            _missing = {k: v for k, v in default.items() if k not in val.keys()}
            val |= _missing

        return val

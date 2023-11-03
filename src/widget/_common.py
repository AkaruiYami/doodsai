from typing import Literal, Union, Iterable, Optional

_Rect = tuple[float, float, float, float]

_ButtonState = Literal["normal", "active", "hover", "disable"]
_Color = tuple[int, int, int]
_ColorMap = Union[dict[str, _Color], Iterable[_Color]]

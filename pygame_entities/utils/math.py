import math
from typing import Union, Tuple


class Vector2:
    """
    Class for 2-dimensional vector.

    Handles operators like + - * /
    """

    def __init__(self, x=0.0, y=0.0) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(xy: Tuple[Union[float, int], Union[float, int]]) -> "Vector2":
        """
        Creating new Vector() from tuple with 2 numbers
        """
        return Vector2(xy[0], xy[1])

    def get_tuple(self) -> Tuple[float, float]:
        """
        Gets tuple with x and y in it
        """
        return (self.x, self.y)

    def get_integer_tuple(self) -> Tuple[int, int]:
        """
        Gets tuple with x and y in it.

        x and y will be rounded to int
        """
        return (int(self.x), int(self.y))

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]) -> "Vector2":
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: Union[int, float]) -> "Vector2":
        return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other: Union[int, float]) -> "Vector2":
        return Vector2(self.x // other, self.y // other)

    def magnitude(self) -> float:
        """
        Length of vector
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self) -> "Vector2":
        """
        Returns normilized vector.

        Length of normilized vector == 1, but it is still points into same direction
        """
        magnitude = self.magnitude()

        if magnitude == 0:
            return Vector2(0, 0)

        return Vector2(self.x / magnitude, self.y / magnitude)

    @staticmethod
    def lerp(a: "Vector2", b: "Vector2", t: float) -> "Vector2":
        """
        Smoothly changing value from a to b.

        Smooth coef is t.

        0 < t <= 1
        """
        return Vector2(lerp(a.x, b.x, t), lerp(a.y, b.y, t))

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"


def lerp(a: float, b: float, t: float) -> float:
    """
    Smoothly changing value from a to b.

    Smooth coef is t.

    0 < t <= 1
    """
    return (1 - t) * a + t * b


def clamp(x: Union[float, int], minimum: Union[float, int], maximum: Union[float, int]) -> Union[float, int]:
    """
    Clamping x between minimum and maximum.

    Using python functions max() and min()
    """
    return min(max(x, minimum), maximum)

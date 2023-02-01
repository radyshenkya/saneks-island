from pygame import Rect

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


def check_side_x(a: Rect, b: Rect) -> int:
    """
    Checks where is the a depending on b position on horizontal.

    Returns LEFT / RIGHT
    """
    if a.center[0] > b.center[0]:
        return RIGHT
    return LEFT


def check_side_y(a: Rect, b: Rect) -> int:
    """
    Checks where is the a depending on b position on vertical.

    Returns UP / DOWN
    """
    if a.center[1] > b.center[1]:
        return DOWN
    return UP


def check_side(a: Rect, b: Rect) -> int:
    """
    Checks where is the a depending on b position on vertical and horizontal.

    Returns UP / DOWN / LEFT/ RIGHT
    """
    width_ratio = (a.height + b.height) / (a.width + b.width)

    a.center = (a.center[0] * width_ratio, a.center[1])
    b.center = (b.center[0] * width_ratio, b.center[1])

    if abs(a.center[0] - b.center[0]) > abs(a.center[1] - b.center[1]):
        return check_side_x(a, b)
    return check_side_y(a, b)

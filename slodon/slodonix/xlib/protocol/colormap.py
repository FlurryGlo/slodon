# Based on: https://tronche.com/gui/x/xlib/color/XCreateColormap.html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from slodon.slodonix.display.display import Display


class _ColorMap:
    def __init__(self, display: Display, w, visual, alloc: int) -> None:
        """
        ColorMap initialization
        ### Arguments
        - display (str): Specifies the connection to the X server.
        - w (Window): 	Specifies the window on whose screen you want to create a colormap.
        - visual (Visual): If the visual type is not one supported by the screen, a BadMatch error results.
        - alloc (int): 	Specifies the colormap entries to be allocated. You can pass AllocNone or AllocAll.
        ### Returns
        - None
        """

        self.display = display
        self.w = w
        self.visual = visual
        self.alloc = alloc


def create_color_map(*args, **kwargs) -> _ColorMap:
    """

    :param args:
    :param kwargs:
    :return:
    """
    return _ColorMap(*args, **kwargs)

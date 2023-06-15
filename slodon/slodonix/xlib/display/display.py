"""Basic display"""

import os
from slodon.slodonix.protocol.display import BaseDisplay


class Display(BaseDisplay):
    """
    Represents a basic display

    A set of screens for a single user with one keyboards and one pointer(usually a mouse) is called a display.
    """

    def __init__(self, display) -> None:
        super().__init__(display=display)


def open_display(name=os.environ["DISPLAY"]) -> Display:
    """
    Open a display

    name: The name of the display

    Returns a display object
    """
    return Display(display=name)

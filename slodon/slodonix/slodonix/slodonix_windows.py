# https://www.win7dll.info/user32_dll.html
# Taken inspiration from: https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py
# (pyautogui: see notice.md)
import time
from ctypes import windll as w
import ctypes
from typing import Union, Callable, Any

# This project
from slodon.slodonix.systems.windows.keyboard_map import full_map as key_map
from slodon.slodonix.systems.windows.utils import *
from slodon.slodonix.systems.windows.structures import POSITION, SIZE
from slodon.slodonix.systems.windows.constants import *
from slodon.slodonix.slodonix.tween import linear, getPointOnLine


__all__ = ["Display", "get_os", "DisplayContext"]

ev = MOUSEEVENTF_LEFTDOWN
ev_up = MOUSEEVENTF_LEFTUP
ev_click = MOUSEEVENTF_LEFTCLICK

X_TYPE = Union[int, float, None, tuple]
Y_TYPE = Union[int, float, None]
DURATION_TYPE = Union[float, None]
TWEEN_TYPE = Union[Callable, None]  # Callable -> tween function


class Screen:
    """
    Represent a screen in a display on windows, it contains information about the screen.
    """

    pass


class _Interact:
    """ """

    def __init__(self, info) -> None:
        self.info = info

    # noinspection PyMethodMayBeStatic
    def key_up(self, key: str) -> None:
        """
        - https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-keyup#parameters
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L295-L332

        ### Arguments
            - key (str): The key(FROM UTILS.KEY_NAMES) to release
        ### Returns
            - None
        """

        if key_map[key] is None:
            return

        needs_shift = is_shift_character(key)

        mods, vk_code = divmod(key_map[key], 0x100)

        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needs_shift, 0x10),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, 0, 0)  #

        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

        for apply_mod, vk_mod in [
            (mods & 1 or needs_shift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)  #

    # Todo: redefine this by using the latest SendInput function
    # noinspection PyMethodMayBeStatic
    def key_down(self, key: str, with_release=False) -> None:
        """
        - https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L250-L292
        Key press without release | with release
        ### Arguments
          - key (str): The key(FROM UTILS.KEY_NAMES) to press down
          - with_release (bool): Whether to release the key after press down
        ### Returns
          - None
        """

        if key_map[key] is None:  # the key is not valid
            return

        needs_shift = is_shift_character(key)

        # https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        mods, vk_code = divmod(key_map[key], 0x100)

        for apply_mod, vk_mod in [
            (mods & 4, 0x12),
            (mods & 2, 0x11),
            (mods & 1 or needs_shift, 0x10),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYDOWN, 0)  #

        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYDOWN, 0)
        for apply_mod, vk_mod in [
            (mods & 1 or needs_shift, 0x10),
            (mods & 2, 0x11),
            (mods & 4, 0x12),
        ]:  # HANKAKU not supported! mods & 8
            if apply_mod:
                ctypes.windll.user32.keybd_event(vk_mod, 0, KEYEVENTF_KEYUP, 0)  #

        if with_release:
            self.key_up(key)

    # noinspection PyMethodMayBeStatic
    def moveto(self, x: int, y: int, x_offset, y_offset, duration, tween=linear) -> None:
        """

        Move the mouse to the specified position
        ### Arguments
         - x (int): x position of the mouse
         - y (int): y position of the mouse
         - tween (Callable): The tween function to use
         - duration (float): The amount of time it takes to move the mouse
         - x_offset (int): The x offset of the mouse(how  far left and right move the mouse)
         - y_Offset (int): The y offset of the mouse (how far up and down move the mouse)
         (https://pyautogui.readthedocs.io/en/latest/mouse.html#tween-easing-functions

        ### Returns
         - None
        """
        x_offset = int(x_offset) if x_offset is not None else 0
        y_offset = int(y_offset) if y_offset is not None else 0

        if x is None and y is None and x_offset == 0 and y_offset == 0:
            return  # Special case for no mouse movement at all.

        _position = self.info.position()
        start_x, start_y = _position.x, _position.y

        x = int(x) if x is not None else start_x
        y = int(y) if y is not None else start_y

        _size = self.info.size()
        width, height = _size.cx, _size.cy

        steps = [(x, y)]

        sleep_amount = MINIMUM_SLEEP

        if duration > MINIMUM_DURATION:
            num_steps = max(width, height)
            sleep_amount = duration / num_steps
            if sleep_amount < MINIMUM_SLEEP:
                num_steps = int(duration / MINIMUM_SLEEP)
                sleep_amount = duration / num_steps

            steps = [getPointOnLine(start_x, start_y, x, y, tween(n / num_steps)) for n in range(num_steps)]
            steps.append((x, y))

        for tween_x, tween_y in steps:
            if len(steps) > 1:
                time.sleep(sleep_amount)

            tween_x = int(round(tween_x))
            tween_y = int(round(tween_y))

            if (tween_x, tween_y) not in FAILSAFE_POINTS:
                fail_safe_check(instance=self.info)

            w.user32.SetCursorPos(tween_x, tween_y)

        w.user32.SetCursorPos(x, y)

    # noinspection PyMethodMayBeStatic
    def mouse_down(self, x, y, button, with_release=False) -> None:
        """
        - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L375-L401

        ### Arguments
          - x (int): The x position of the mouse
          - y (int): The y position of the mouse
          - button (str): The button to press down
        ### Returns
          - None
        """
        global ev
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            ev = MOUSEEVENTF_LEFTDOWN  # value in hex: 0x0002
        elif button == MIDDLE:
            ev = MOUSEEVENTF_MIDDLEDOWN  # value in hex: 0x0020
        elif button == RIGHT:
            ev = MOUSEEVENTF_RIGHTDOWN  # value in hex: 0x0008

        try:
            send_mouse_event(ev, x, y, instance=_Info())  # instance for the size
        except (PermissionError, OSError):
            # TODO: We need to figure out how to prevent these errors,
            #  see https://github.com/asweigart/pyautogui/issues/60
            pass
        if with_release:
            self.mouse_up(x, y, button)

    # noinspection PyMethodMayBeStatic
    def mouse_up(self, x, y, button) -> None:
        """
        - https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L404-L429
        Args:
            x (int): The x position of the mouse event.
            y (int): The y position of the mouse event.
            button (str): The mouse button, either 'left', 'middle', or 'right'
        Returns:
          None
        """
        global ev_up
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if button == LEFT:
            ev_up = MOUSEEVENTF_LEFTUP  # value in hex: 0x0004
        elif button == MIDDLE:
            ev_up = MOUSEEVENTF_MIDDLEUP  # value in hex: 0x0040
        elif button == RIGHT:
            ev_up = MOUSEEVENTF_RIGHTUP  # value in hex: 0x0010

        try:
            send_mouse_event(ev_up, x, y, instance=_Info())
        except (
            PermissionError,
            OSError,
        ):  # TODO: We need to figure out how to prevent these errors,
            # see https://github.com/asweigart/pyautogui/issues/60
            pass

    # noinspection PyMethodMayBeStatic
    def click(self, x, y, button) -> None:
        """
        - https://learn.microsoft.com/en-us/windows/win32/learnwin32/mouse-clicks
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L432-L458
        ### Arguments
            - x (int): The x position of the mouse event.
            - y (int): The y position of the mouse event.
            - button (str): The mouse button, either 'left', 'middle', or 'right'
        ### Returns
            - None
        """

        global ev_click
        if button not in (LEFT, MIDDLE, RIGHT):
            raise ValueError(
                'button arg to _click() must be one of "left", "middle", or "right", not %s'
                % button
            )

        if x is None:
            x = self.info.position().x
        if y is None:
            y = self.info.position().y

        if button == LEFT:
            ev_click = MOUSEEVENTF_LEFTCLICK

        if button == MIDDLE:
            ev_click = MOUSEEVENTF_MIDDLECLICK

        if button == RIGHT:
            ev_click = MOUSEEVENTF_RIGHTCLICK

        try:
            send_mouse_event(ev_click, x, y, instance=_Info())

        except (PermissionError, OSError):
            pass

    # noinspection PyMethodMayBeStatic
    def mouse_is_swapped(self):
        """
        - https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics (SM_SWAPBUTTON)
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L461

        Nonzero if the meanings of the left and right mouse buttons are swapped; otherwise, 0.
        # TODO - measure the performance of checking this setting for each click.
        """
        return w.user32.GetSystemMetrics(23) != 0

    def scrool(self):
        """ """
        pass

    def hscrool(self):
        """ """
        pass

    def vscrool(self):
        """ """
        pass


class _Info:
    """
    Returns back information about the display
    """

    def get_top_window(self):
        pass

    # noinspection PyMethodMayBeStatic
    def position(self, _type=float, _tuple=False) -> Position | tuple[Any, Any]:
        """
        x-y position of the mouse
        ##Arguments
            - _type (type): The type of the x and y coordinates
            - _tuple (bool): If True, returns a tuple of the x and y coordinates

        ### Returns
          - Position object with the x and y coordinates

        """

        pos = POSITION()

        w.user32.GetCursorPos(
            ctypes.byref(pos)
        )  # fill up the pointer with the information

        if _tuple:
            return _type(pos.x), _type(pos.y)

        return Position(pos.x, pos.y)  # access it from the pointer

    # noinspection PyMethodMayBeStatic
    def size(self) -> SIZE:
        """
        - https://learn.microsoft.com/en-us/windows/win32/api/windef/ns-windef-size(?)
        - https://github.com/asweigart/pyautogui/blob/master/pyautogui/_pyautogui_win.py#L348-L354
        """
        return SIZE(
            ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1),
        )


class Display:
    """
    Represents a basic display, which is the starting point.
    Acts as a context manager.
    """

    def __init__(self):
        self.info = _Info()
        self._interact = _Interact(info=self.info)  # SHOULD BE NOT USED DIRECTLY OUTSIDE THE CLASS

    def key_up(self, key, _pause=True) -> None:
        """
        Performs a keyboard key release  (without the press down beforehand).

        ### Arguments:
            - key (str): The key to be pressed. See the [keys](keys.md) page for valid key strings.

        ### Returns:
            - None
        """

        if len(key) > 1:
            key = key.lower()

        self._interact.key_up(key)

    def key_down(self, key, _pause=True, with_release=True) -> None:
        """
        Performs a keyboard key press down (without the release afterwards).

        ### Arguments:
            - key (str): The key to be pressed. See the [keys](keys.md) page for valid key strings.
            - with_release (bool): If True, the key will be released after the press down.
        ### Returns:
            - None
        """

        if len(key) > 1:
            key = key.lower()

        self._interact.key_down(key, with_release=with_release)

    def move_to(
        self,
        x: X_TYPE = None,
        y: Y_TYPE = None,
        duration: DURATION_TYPE = 0.0,
        tween: TWEEN_TYPE = linear,
        _pause=True,
    ):
        """
        Moves the mouse cursor to a point on the screen.

        The x and y parameters detail where the mouse event happens. If None, the
        current mouse position is used. If a float value, it is rounded down. If
        outside the boundaries of the screen, the event happens at edge of the
        screen.

        ### Arguments:
            - x (int): The x position on the screen where the
                click happens. None by default. If tuple, this is used for x and y.

            - y (int): : The y position on the screen where the
                        click happens. None by default.

            - duration (float): The number of seconds to perform the mouse move to the x,y coordinates.
                0, then the mouse cursor is moved
                instantaneously. 0.0 by default.

            - tween (func, optional): The tweening function used if the duration is not
            0. A linear tween is used by default.

        ### Returns:
            None
        """
        self._interact.moveto(x, y, duration=duration, x_offset=0, y_offset=0, tween=tween)

    def mouse_down(self, x=None, y=None, button=PRIMARY, duration=0.0, tween=linear, _pause=True, with_release=True):
        """
        Performs pressing a mouse button down(but not up).

        The x and y parameters detail where the mouse event happens. If None, the
        current mouse position is used. If a float value, it is rounded down. If
        outside the boundaries of the screen, the event happens at edge of the
        screen.

        ### Arguments:
            x (int, float, None, tuple, optional): The x position on the screen where the
                mouse down happens. None by default. If tuple, this is used for x and y.
                If x is a str, it's considered a filename of an image to find on
                the screen with locateOnScreen() and click the center of.
            y (int, float, None, optional): The y position on the screen where the
                mouse down happens. None by default.

            button (str, int, optional): The mouse button pressed down.

        ### Returns:
            - None

        Raises:
            SlodonixException: If button is not one of 'left', 'middle', 'right', 1, 2, or 3
        """

        # move the mouse to the x, y coordinates
        self._interact.moveto(x, y, x_offset=0, y_offset=0, duration=0, tween=tween)
        self._interact.mouse_down(x, y, button, with_release=with_release)  # press the button

    def mouse_up(self):

        pass


class DisplayContext(Display):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class DisplayAsParent(Display):
    """
    Use the display class as a parent for other classes.

    TBD
    """


def get_os() -> str:
    """
    Return back the currently used operating system.
    """
    return "Windows"

import ctypes
from ctypes import wintypes
# Basic structures


class MOUSEINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
    """
    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
    """
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
    """
    _fields_ = [
        ("uMsg", ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.DWORD),
    ]


class INPUT(ctypes.Structure):
    """
    https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
    """
    class _I(ctypes.Union):
        _fields_ = [
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT),
            ("hi", HARDWAREINPUT),
        ]

    _anonymous_ = ("i",)
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("i", _I),
    ]

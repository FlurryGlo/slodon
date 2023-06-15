# This code is based on python3-xlib
# https://github.com/simonzack/python3-xlib

# local
from . import *

"""Keyboard and Pointer Events"""

# -----------------------------------------------------------------------
# Event names:
#
# 0 and 1 are reserved for errors and replies in the protocol

_KeyPress = 2
_KeyRelease = 3
_ButtonPress = 4
_ButtonRelease = 5
_MotionNotify = 6
_EnterNotify = 7
_LeaveNotify = 8
_FocusIn = 9
_FocusOut = 10
_KeymapNotify = 11
_Expose = 12
_GraphicsExpose = 13
_NoExpose = 14
_VisibilityNotify = 15
_CreateNotify = 16
_DestroyNotify = 17
_UnmapNotify = 18
_MapNotify = 19
_MapRequest = 20
_ReparentNotify = 21
_ConfigureNotify = 22
_ConfigureRequest = 23
_GravityNotify = 24
_ResizeRequest = 25
_CirculateNotify = 26
_CirculateRequest = 27
_PropertyNotify = 28
_SelectionClear = 29
_SelectionRequest = 30
_SelectionNotify = 31
_ColormapNotify = 32
_ClientMessage = 33
_MappingNotify = 34
LASTEvent = 35


class AnyEvent(Event):
    _code = None
    _fields = Struct(
        Card8("type"),
        Card8("detail"),
        Card16("sequence_number"),
        FixedString("data", 28),
    )


class KeyButtonPointer(Event):
    _code = None
    _fields = Struct(
        Card8("type"),
        Card8("detail"),
        Card16("sequence_number"),
        Card32("time"),
        Window("root"),
        Window("window"),
        Window("child", (NONE,)),
        Int16("root_x"),
        Int16("root_y"),
        Int16("event_x"),
        Int16("event_y"),
        Card16("state"),
        Card8("same_screen"),
        Pad(1),
    )


class KeyPress(KeyButtonPointer):
    _code = _KeyPress


class KeyRelease(KeyButtonPointer):
    _code = _KeyRelease


class ButtonPress(KeyButtonPointer):
    _code = _ButtonPress


class ButtonRelease(KeyButtonPointer):
    _code = _ButtonRelease


class MotionNotify(KeyButtonPointer):
    _code = _MotionNotify


class EnterLeave(Event):
    _code = None
    _fields = Struct(
        Card8("type"),
        Card8("detail"),
        Card16("sequence_number"),
        Card32("time"),
        Window("root"),
        Window("window"),
        Window("child", (NONE,)),
        Int16("root_x"),
        Int16("root_y"),
        Int16("event_x"),
        Int16("event_y"),
        Card16("state"),
        Card8("mode"),
        Card8("flags"),
    )


class EnterNotify(EnterLeave):
    _code = _EnterNotify


class LeaveNotify(EnterLeave):
    _code = _LeaveNotify


class Focus(Event):
    _code = None
    _fields = Struct(
        Card8("type"),
        Card8("detail"),
        Card16("sequence_number"),
        Window("window"),
        Card8("mode"),
        Pad(23),
    )


class FocusIn(Focus):
    _code = _FocusIn


class FocusOut(Focus):
    _code = _FocusOut


class Expose(Event):
    _code = _Expose
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("window"),
        Card16("x"),
        Card16("y"),
        Card16("width"),
        Card16("height"),
        Card16("count"),
        Pad(14),
    )


class GraphicsExpose(Event):
    _code = _GraphicsExpose
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("x"),
        Card16("y"),
        Card16("width"),
        Card16("height"),
        Card16("minor_event"),
        Card16("count"),
        Card8("major_event"),
        Pad(11),
    )


class NoExpose(Event):
    _code = _NoExpose
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Drawable("window"),
        Card16("minor_event"),
        Card8("major_event"),
        Pad(21),
    )


class VisibilityNotify(Event):
    _code = _VisibilityNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("window"),
        Card8("state"),
        Pad(23),
    )


class CreateNotify(Event):
    _code = _CreateNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("parent"),
        Window("window"),
        Int16("x"),
        Int16("y"),
        Card16("width"),
        Card16("height"),
        Card8("border_width"),
        Card8("override"),
        Pad(9),
    )


class DestroyNotify(Event):
    _code = _DestroyNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Pad(20),
    )


class UnmapNotify(Event):
    _code = _UnmapNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Card8("from_configure"),
        Pad(19),
    )


class MapNotify:
    _code = _MapNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Card8("override"),
        Pad(19),
    )


class MapRequest(Event):
    _code = _MapRequest
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("parent"),
        Window("window"),
        Pad(20),
    )


class ReparentNotify(Event):
    _code = _ReparentNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Window("parent"),
        Int16("x"),
        Int16("y"),
        Card8("override"),
        Pad(11),
    )


class ConfigureNotify(Event):
    _code = _ConfigureNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Window("above_sibling", (NONE,)),
        Int16("x"),
        Int16("y"),
        Card16("width"),
        Card16("height"),
        Card16("border_width"),
        Card8("override"),
        Pad(5),
    )


class ConfigureRequest(Event):
    _code = _ConfigureRequest
    _fields = Struct(
        Card8("type"),
        Card8("stack_mode"),
        Card16("sequence_number"),
        Window("parent"),
        Window("window"),
        Window("sibling", (NONE,)),
        Int16("x"),
        Int16("y"),
        Card16("width"),
        Card16("height"),
        Card16("border_width"),
        Card16("value_mask"),
        Pad(5),
    )


class GravityNotify(Event):
    _code = _GravityNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Int16("x"),
        Int16("y"),
        Pad(16),
    )


class ResizeRequest(Event):
    _code = _ResizeRequest
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("window"),
        Card16("width"),
        Card16("height"),
        Pad(20),
    )


class Circulate(Event):
    _code = None
    _fields = Struct(
        Card8("type"),
        Card16("sequence_number"),
        Window("event"),
        Window("window"),
        Pad(4),
        Card8("place"),
        Pad(15),
    )


class CirculateNotify(Circulate):
    _code = _CirculateNotify


class CirculateRequest(Circulate):
    _code = _CirculateRequest


class PropertyNotify(Event):
    _code = _PropertyNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("window"),
        Card32("atom"),
        Card32("time"),
        Card8("state"),
        Pad(15),
    )


class SelectionClear(Event):
    _code = _SelectionClear
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Card32("time"),
        Window("window "),
        Card32("atom"),
        Pad(16),
    )


class SelectionRequest(Event):
    _code = _SelectionRequest
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Card32("time"),
        Window("owner"),
        Window("requestor"),
        Card32("selection"),
        Card32("target"),
        Card32("property"),
        Pad(4),
    )


class SelectionNotify(Event):
    _code = _SelectionNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Card32("time"),
        Window("requestor"),
        Card32("selection"),
        Card32("target"),
        Card32("property"),
        Pad(8),
    )


class ColormapNotify(Event):
    _code = _ColormapNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Window("window"),
        Colormap("colormap", (NONE,)),
        Card8("new"),
        Card8("state"),
        Pad(18),
    )


class MappingNotify(Event):
    _code = _MappingNotify
    _fields = Struct(
        Card8("type"),
        Pad(1),
        Card16("sequence_number"),
        Card8("request"),
        Card8("first_keycode"),
        Card8("count"),
        Pad(25),
    )


class ClientMessage(Event):
    _code = _ClientMessage
    _fields = Struct(
        Card8("type"),
        Format("data", 1),
        Card16("sequence_number"),
        Window("window"),
        Card32("client_type"),
        FixedPropertyData("data", 20),
    )


class KeymapNotify:
    _code = _KeymapNotify
    _fields = Struct(Card8("type"), FixedList("data", 31, Card8Obj, pad=0))

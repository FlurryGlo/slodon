__all__ = ["DisplayNameError", "DisplayConnectionError"]


class DisplayError(Exception):
    pass


class DisplayNameError(Exception):
    pass


class DisplayConnectionError(Exception):
    pass


class ConnectionClosedError(Exception):
    pass


class XError(Exception):
    pass

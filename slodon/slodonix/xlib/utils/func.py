import socket


def is_socket_connected(sock) -> bool:
    """
    :param sock: the socket to check
    :return: bool
    """
    try:
        # Get the socket error status
        error_code = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if error_code == 0:
            return True  # Socket is connected
        else:
            return False  # Socket is closed or errored
    except socket.error:
        return False  # Socket is closed or errored

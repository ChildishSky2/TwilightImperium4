import types

import Server


class _FakeRFile:
    def __iter__(self):
        raise OSError("An existing connection was forcibly closed by the remote host", winerror=10054)


class _FakeWFile:
    def write(self, _data):
        raise OSError("An existing connection was forcibly closed by the remote host", winerror=10054)

    def flush(self):
        pass


class _FakeServer:
    incoming_messages = None
    game = types.SimpleNamespace()


def test_handle_ignores_winerror_10054_on_socket_read():
    handler = Server._ClientHandler.__new__(Server._ClientHandler)
    handler.client_address = ("127.0.0.1", 12345)
    handler.server = _FakeServer()
    handler.rfile = _FakeRFile()
    handler.wfile = _FakeWFile()

    handler.handle()


def test_send_message_ignores_winerror_10054_on_write():
    handler = Server._ClientHandler.__new__(Server._ClientHandler)
    handler.wfile = _FakeWFile()

    handler._send_message({"type": "ping"})

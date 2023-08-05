from logging import getLogger
from typing import Any, cast
from reactivex.subject import BehaviorSubject
import dataclasses
import reactivex

import orjson
import websocket

from .request import CryptodotcomRequestMessage

logger = getLogger(__name__)


class EnhancedWebsocket:
    socket: websocket.WebSocketApp
    _id = 0

    def __str__(self):
        return f'EnhancedWebsocket <{self.socket.url}>'
    

    def __init__(self, socket: websocket.WebSocketApp):
        self.socket = socket

    def send_message(self, message: CryptodotcomRequestMessage) -> int:
        return self.send_json(dataclasses.asdict(message))

    def prepare_request(self, message: dict | CryptodotcomRequestMessage) -> tuple[int, bytes]:
        as_dict: dict
        if type(message) == CryptodotcomRequestMessage:
            as_dict = dataclasses.asdict(message)
        else:
            as_dict = cast(dict, message)

        self._id += 1
        if "params" in as_dict and not as_dict["params"]:
            del as_dict["params"]
        if not as_dict["id"]:
            as_dict["id"] = self._id
        as_bytes = orjson.dumps(as_dict)
        return as_dict["id"], as_bytes

    def request_to_observable(self, message: dict | CryptodotcomRequestMessage) -> tuple[int, reactivex.Observable[Any]]:
        message_id, as_bytes = self.prepare_request(message)
        def send_():
            logger.debug("[SOCKET][BYTES] Sending json to socket: %s", as_bytes)
            self.socket.send(as_bytes)
        return message_id, reactivex.from_callable(send_)

    def send_json(self, message: dict):
        message_id, as_bytes = self.prepare_request(message)
        logger.debug("[SOCKET] Sending json to socket: %s", as_bytes)
        self.socket.send(as_bytes)
        return message_id

EnhancedWebsocketBehaviorSubject = BehaviorSubject[EnhancedWebsocket]

__all__ = [
    "EnhancedWebsocket",
    "EnhancedWebsocketBehaviorSubject",
]

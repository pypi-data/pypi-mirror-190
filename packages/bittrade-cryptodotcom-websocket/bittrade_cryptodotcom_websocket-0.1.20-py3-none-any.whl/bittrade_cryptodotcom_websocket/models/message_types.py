from typing import Literal


WEBSOCKET_STATUS = "WEBSOCKET_STATUS"
WEBSOCKET_HEARTBEAT = "WEBSOCKET_HEARTBEAT"
WEBSOCKET_MESSAGE = "WEBSOCKET_MESSAGE"
MessageTypes = Literal["WEBSOCKET_STATUS", "WEBSOCKET_HEARTBEAT", "WEBSOCKET_MESSAGE"]

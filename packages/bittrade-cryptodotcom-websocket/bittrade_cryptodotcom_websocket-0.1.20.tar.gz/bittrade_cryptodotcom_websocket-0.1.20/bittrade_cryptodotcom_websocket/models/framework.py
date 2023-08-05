from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import cryptocom
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler

from .response_message import CryptodotcomResponseMessage
from .enhanced_websocket import EnhancedWebsocket, EnhancedWebsocketBehaviorSubject
from .bundle import WebsocketBundle
from .user_balance import (
    UserBalance,
)

from .order import OrderDict


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class CryptodotcomContext:
    all_subscriptions: CompositeDisposable
    books: dict[str, Observable[Orderbook]]
    cancel_all: Callable[[str, Literal["trigger", "limit", "all"]], Observable[bool]]
    cancel_all_http: Callable[
        [str, Literal["trigger", "limit", "all"]], Observable[bool]
    ]
    cancel_order: Callable[[str, str | None, bool | None, bool | None], Observable[bool]]
    close_position: Callable[
        [str, Literal["market", "limit"], Optional[str]], Observable[int]
    ]
    close_position_http: Callable[
        [str, Literal["market", "limit"], Optional[str]], Observable[int]
    ]
    create_order: Callable[
        [str, str, str, float, Optional[float], Optional[Any]],
        Observable[dict[str, Any]],
    ]
    exchange: cryptocom
    feed_messages: Observable[CryptodotcomResponseMessage]
    get_user_balance: Callable[[], Observable[list[UserBalance]]]
    get_user_open_orders: Callable[[Optional[str]], Observable[list[OrderDict]]]
    guaranteed_websocket: Observable[EnhancedWebsocket]
    public_socket_connection: ConnectableObservable[WebsocketBundle]
    private_socket_connection: ConnectableObservable[WebsocketBundle]
    private_messages: Observable[CryptodotcomResponseMessage]
    public_messages: Observable[CryptodotcomResponseMessage]
    response_messages: Observable[CryptodotcomResponseMessage]
    scheduler: ThreadPoolScheduler
    websocket_bs: EnhancedWebsocketBehaviorSubject
    open_orders: Observable[Any]
    open_orders_reloaded: Observable[Any]

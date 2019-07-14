# coding=utf-8

# from ssdb.connection import (BlockingConnectionPool, ConnectionPool, Connection)
# from ssdb.utils import SortedDict
# from ssdb.exceptions import (AuthenticationError, ConnectionError,
#                              BusyLoadingError, DataError, InvalidResponse,
#                              PubSubError, SSDBError, ResponseError, WatchError)
from ssdb.kv import KV
from ssdb.hash import HashMap
from ssdb.queue import Queue
from ssdb.z_hash import ZHash

global LIMIT_MAX


class Client(HashMap, KV, ZHash, Queue):
    pass


__version__ = '0.0.10'
VERSION = tuple(map(int, __version__.split('.')))

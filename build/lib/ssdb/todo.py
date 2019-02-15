# coding=utf-8
import pickle, warnings
from pyssdb import Client as PY_SSDB_Client, command_post_processing
from typing import Union


class Base(PY_SSDB_Client):
    @command_post_processing
    def execute_command(self, cmd, *args):
        connection = self.connection_pool.get_connection()
        try:
            connection.send(cmd, *args)
            data = connection.recv()
            # print(f'cmd={cmd:<10} recv={type(data).__name__}:{str(data):<10} args={args}')
        except Exception as e:
            self.connection_pool.release(connection, error=True)
            raise e
        else:
            self.connection_pool.release(connection)
            return data


def pickle_dumps(obj):
    return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)


def pickle_loads(obj):
    return obj if obj is None else pickle.loads(obj)


def check_limit(limit):
    return limit if limit else 999999999


def deal_start_end(start, end, mode=''):
    start = c(start, check_empty=False)
    if not end:
        end = '' if mode == 'z' else f'{start}\xFF'
    return start, end


def c(a: Union[int, str, list], check_empty: bool = True) -> str:
    if check_empty:
        assert a or a == 0, f'key or name is EMPTY? ({a})'
    if isinstance(a, list):
        a = '_'.join([str(i) for i in a])
    else:
        a = str(a) if a or a == 0 else ''
    return a


def dict_to_list(kv_dict):
    kv_list = []
    for k, v in kv_dict.items():
        kv_list.extend([k, pickle_dumps(v)])
    return kv_list


def list_to_dict(items, mode=''):
    x = dict()
    for i in range(0, len(items), 2):
        x[items[i].decode('utf-8')] = int(items[i + 1]) if mode == 'z' else pickle_loads(items[i + 1])
    return x


def bytes_to_str(x):
    if isinstance(x, list):
        return [_.decode('utf-8') for _ in x]
    elif isinstance(x, bytes):
        return x.decode('utf-8')
    assert 0, f'bytes_to_str not support  [{type(x)}]'

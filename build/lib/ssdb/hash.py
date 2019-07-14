# coding=utf-8
from ssdb.todo import *


class HashMap(Base):
    """出错则返回 false, 其它值表示正常."""

    def hset(self, name, key, value) -> int:
        """
        :return: int (1:new 0:update)
        """
        return self.execute_command('hset', c(name), c(key), pickle_dumps(value))

    def hget(self, name, key):
        return pickle_loads(self.execute_command('hget', c(name), c(key))) if key else None

    def hdel(self, name, key):
        """如果出错则返回 false, 其它值表示正常. 你无法通过返回值来判断被删除的 key 是否存在."""
        return self.execute_command('hdel', c(name), c(key))

    def hincr(self, name, key, num: int = 1):
        """返回新的值."""
        return self.execute_command('hincr', c(name), c(key), int(num))

    def hexists(self, name, key) -> int:
        """
        :return: exist: 1 / not:0
        """
        return int(self.execute_command('hexists', c(name), c(key)))

    def hsize(self, name) -> int:
        """
        :return: exist: 1 / not:0
        """
        return self.execute_command('hsize', c(name))

    def hlist(self, name_start=None, name_end=None, limit=None) -> list:
        """
        列出名字处于区间 (name_start, name_end] 的 hash map. ("", ""] 表示整个区间. (return name_list)
        """
        name_start, name_end = deal_start_end(name_start, name_end)
        name_end = name_end if name_end else '{}\xFF'.format(name_start)
        return bytes_to_str(self.execute_command('hlist', name_start, name_end, check_limit(limit)))

    def hrlist(self, name_start=None, name_end=None, limit=None) -> list:
        return self.hlist(name_start, name_end, limit)[::-1]

    def hkeys(self, name, key_start=None, key_end=None, limit=None):
        key_start, key_end = deal_start_end(key_start, key_end)
        return bytes_to_str(self.execute_command('hkeys', c(name), key_start, key_end, check_limit(limit)))

    def hgetall(self, name) -> dict:
        x = self.execute_command('hgetall', c(name))
        return list_to_dict(x)

    def hscan(self, name, key_start=None, key_end=None, limit=None, r='v'):
        """
        :param name:
        :param key_start:
        :param key_end:
        :param limit:
        :param r: v/d > value list/ kv dict
        :return:
        """
        key_start, key_end = deal_start_end(key_start, key_end)
        d = list_to_dict(self.execute_command('hscan', c(name), key_start, key_end, check_limit(limit)))
        return list(d.values()) if r == 'v' else d

    def hrscan(self, name, key_start=None, key_end=None, limit=None, r='v'):
        d = self.hscan(name, key_start, key_end, limit, r)
        return d[::-1] if d == 'v' else d

    def hclear(self, name) -> int:
        """
        :return: delete key number
        """
        return int(self.execute_command('hclear', c(name)))

    def multi_hset(self, name, kvs: dict):
        # assert kvs, 'kvs is empty?'
        return self.execute_command('multi_hset', c(name), *dict_to_list(kvs)) if kvs else 0

    def multi_hget(self, name, keys: list):
        return list_to_dict(self.execute_command('multi_hget', c(name), *keys)) if keys else {}

    def multi_hdel(self, name, keys: list) -> int:
        return self.execute_command('multi_hdel', c(name), *keys) if keys else 0

    hset_multi = multi_hset
    hget_multi = multi_hget
    hdel_multi = multi_hdel

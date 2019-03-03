# coding=utf-8
from ssdb.todo import *


class KV(Base):
    """
    ssdb python 3 client
    """

    # K/V
    # 出错则返回 false, 其它值(默认1)表示正常.
    def set(self, key, value) -> int:
        """
        :return: int (1)
        """
        return self.execute_command('set', c(key), pickle_dumps(value))

    def setx(self, key, value, ttl: int) -> int:
        """
        :return: int (1)
        """
        return self.execute_command('setx', c(key), pickle_dumps(value), ttl)

    def setnx(self, key, value, ttl: int) -> int:
        """
        当 key 不存在时, 设置指定 key 的值内容. 如果已存在, 则不设置.
        :return: 1: value 已经设置, 0: key 已经存在, 不更新.
        """
        warnings.warn("This method is invalid, Please do not use...", DeprecationWarning)
        return int(self.execute_command('setnx', c(key), pickle_dumps(value), ttl))

    def expire(self, key, ttl: int) -> int:
        """
        :return: 如果 key 存在并设置成功, 返回 1, 如果 key 不存在, 返回 0.
        """
        return int(self.execute_command('expire', c(key), ttl))

    def ttl(self, key) -> int:
        """
        :return: ttl | -1: not ttl
        """
        return int(self.execute_command('ttl', c(key)))

    def get(self, key):
        """
        :return: None or Obj
        """
        d = self.execute_command('get', c(key))
        return pickle_loads(d)

    def getset(self, key, value):
        """
        :return: None or **Old Obj**
        """
        warnings.warn("This method is invalid, Please do not use...", DeprecationWarning)
        d = self.execute_command('getset', c(key), pickle_dumps(value))
        return pickle_loads(d)

    def delete(self, key) -> int:
        """
        :return: ALL 1
        """
        return self.execute_command('del', c(key))

    def incr(self, key, num: int = 1) -> int:
        """
        :param key:
        :param num: int, default = 1
        :return: int (new value)
        """
        return self.execute_command('incr', c(key), int(num))

    def exists(self, key) -> int:
        """
        :return: exist: 1 / not: 0
        :rtype: int
        """
        return int(self.execute_command('exists', c(key)))

    # def getbit(self, key, offset):  # bit
    #     return int(self.execute_command('getbit', c(key), offset))
    #
    # def setbit(self, key, offset, val):  # bit
    #     return int(self.execute_command('setbit', c(key), offset, val))
    #
    # def bitcount(self, key, start, end):  # bit
    #     return int(self.execute_command('bitcount', c(key), start, end))
    #
    # def countbit(self, key, start, size):  # bit
    #     return int(self.execute_command('countbit', c(key), start, size))
    #
    # def substr(self, key, start, size):
    #     return self.execute_command('substr', c(key), start, size)

    def strlen(self, key) -> int:
        warnings.warn("This method is incorrect, Because [pickle.dumps], Please do not use...", DeprecationWarning)
        return int(self.execute_command('strlen', c(key)))

    def keys(self, key_start=None, key_end=None, limit=None) -> list:
        """
        keys('') >>>  ("", ""] 表示整个区间.
        warn: keys('0') >>> ['0_1', '0_2'] not include '0'
        """
        key_start = c(key_start, check_empty=False)
        key_end = key_end if key_end else '{}\xFF'.format(key_start)
        return bytes_to_str(self.execute_command('keys', key_start, key_end, check_limit(limit)))

    def rkeys(self, key_start=None, key_end=None, limit=None) -> list:
        return self.keys(key_start, key_end, limit)[::-1]

    def scan(self, key_start=None, key_end=None, limit=None, r='v'):
        """
        :param key_start:
        :param key_end:
        :param limit:
        :param r: v/d > value list/dict
        :return:
        """
        key_start = c(key_start, check_empty=False)
        key_end = key_end if key_end else '{}\xFF'.format(key_start)
        x = list_to_dict(self.execute_command('scan', key_start, key_end, check_limit(limit)))
        return list(x.values()) if r == 'v' else x

    def rscan(self, key_start=None, key_end=None, limit=None, r='v') -> list:
        x = self.scan(key_start, key_end, limit, r)
        return x[::-1] if r == 'v' else x

    def multi_set(self, kvs):  # 出错则返回 false, 其它值表示正常.
        return self.execute_command('multi_set', *dict_to_list(kvs)) if kvs else 0

    def multi_get(self, keys, r='v'):  # 返回包含 key-value 的关联数组, 如果某个 key 不存在, 则它不会出现在返回数组中.
        x = list_to_dict(self.execute_command('multi_get', *keys)) if keys else {}
        return list(x.values()) if r == 'v' else x

    def multi_del(self, keys) -> int:  # 出错则返回 false, 其它值表示正常.
        return self.execute_command('multi_del', *keys) if keys else 0

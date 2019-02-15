# coding=utf-8
from ssdb.todo import *


class ZHash(Base):
    def zset(self, name, key, score: int) -> int:
        """
        :return: int (1:new 0:update)
        """
        return self.execute_command('zset', c(name), c(key), score)

    def zget(self, name, key) -> int:
        return self.execute_command('zget', c(name), c(key))

    def zdel(self, name, key):
        return self.execute_command('zdel', c(name), c(key))

    def zincr(self, name, key, num: int = 1):
        """
        返回新的值.
        使 zset 中的 key 对应的值增加 num. 参数 num 可以为负数. 如果原来的值不是整数(字符串形式的整数), 它会被先转换成整数.
        """
        return self.execute_command('zincr', c(name), c(key), int(num))

    def zexists(self, name, key) -> int:
        """
        :return: exist: 1 / not:0
        """
        return int(self.execute_command('zexists', c(name), c(key)))

    def zsize(self, name) -> int:
        """
        :return: exist: 1 / not:0
        """
        return self.execute_command('zsize', c(name))

    def zlist(self, name_start=None, name_end=None, limit=None) -> list:
        """
         ("", ""] 表示整个区间. (return name_list)
        """
        name_start, name_end = deal_start_end(name_start, name_end)
        name_end = name_end if name_end else '{}\xFF'.format(name_start)
        return bytes_to_str(self.execute_command('zlist', name_start, name_end, check_limit(limit)))

    def zrlist(self, name_start=None, name_end=None, limit=None) -> list:
        return self.zlist(name_start, name_end, limit)[::-1]

    def zkeys(self, name, key_start=None, score_start=None, score_end=None, limit=None):
        key_start = c(key_start, False)
        score_start, score_end = deal_start_end(score_start, score_end, 'z')
        return bytes_to_str(
            self.execute_command('zkeys', c(name), key_start, score_start, score_end, check_limit(limit)))

    def zscan(self, name, key_start=None, score_start=None, score_end=None, limit=None):
        key_start = c(key_start, False)
        score_start, score_end = deal_start_end(score_start, score_end, 'z')
        return list_to_dict(
            self.execute_command('zscan', c(name), key_start, score_start, score_end, check_limit(limit)), 'z')

    def zrscan(self, name, key_start=None, score_start=None, score_end=None, limit=None):
        warnings.warn("This method is invalid, Please do not use...", DeprecationWarning)
        return []

    def zclear(self, name) -> int:
        """
        :return: delete key number
        """
        return self.execute_command('zclear', c(name))

    def multi_zset(self, n1, kvs: dict):
        assert kvs, 'kvs is empty?'
        return self.execute_command('multi_zset', c(n1), *dict_to_list(kvs))

    def multi_zget(self, n1, keys: list):
        return list_to_dict(self.execute_command('multi_zget', c(n1), *keys),'z')

    def multi_zdel(self, n1, keys: list) -> int:
        return self.execute_command('multi_zdel', c(n1), *keys)

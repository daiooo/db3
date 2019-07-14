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

    def zincr(self, name, key, num: int = 1, decimals: int = 0):
        """
        返回新的值.
        使 zset 中的 key 对应的值增加 num. 参数 num 可以为负数. 如果原来的值不是整数(字符串形式的整数), 它会被先转换成整数.
        decimals 为了 id 生成 多少位的数字， 不够就 加
        """
        v = self.execute_command('zincr', c(name), c(key), int(num))
        if decimals and v < 10 ** (decimals - 1):
            v = self.execute_command('zincr', c(name), c(key), 10 ** (decimals - 1))
        return v

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
        """

        列出 zset 中处于区间 (key_start+score_start, score_end] 的 key-score 列表. 如果 key_start 为空,
        那么对应权重值大于或者等于 score_start 的 key 将被返回. 如果 key_start 不为空, 那么对应权重值大于 score_start 的 key,
        或者大于 key_start 且对应权重值等于 score_start 的 key 将被返回.

        也就是说, 返回的 key 在 (key.score == score_start && key > key_start || key.score > score_start),
        并且 key.score <= score_end 区间. 先判断 score_start, score_end, 然后判断 key_start.

        ("", ""] 表示整个区间.


        :param name:
        :param key_start: score_start 对应的 key.
        :param score_start: 返回 key 的最小权重值(可能不包含, 依赖 key_start), 空字符串表示 -inf.
        :param score_end: 返回 key 的最大权重值(包含), 空字符串表示 +inf.
        :param limit:
        :return:
        """
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

    def multi_zset(self, name, kvs: dict):
        assert kvs, 'kvs is empty?'
        return self.execute_command('multi_zset', c(name), *dict_to_list(kvs)) if kvs else 0

    def multi_zget(self, name, keys: list):
        return list_to_dict(self.execute_command('multi_zget', c(name), *keys), 'z') if keys else {}

    def multi_zdel(self, name, keys: list) -> int:
        return self.execute_command('multi_zdel', c(name), *keys) if keys else 0

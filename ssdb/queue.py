# coding=utf-8
from ssdb.todo import *


class Queue(Base):
    def qsize(self, name) -> int:
        return self.execute_command('qsize', c(name))

    def qlist(self, name_start=None, name_end=None, limit=None) -> list:
        """
        列出名字处于区间 (name_start, name_end] 的 queue/list.
        ("", ""] 表示整个区间.
        :param name_start:  返回的起始名字(不包含), 空字符串表示 -inf.
        :param name_end: 返回的结束名字(包含), 空字符串表示 +inf.
        :param limit: 最多返回这么多个元素.
        :return: 出错则返回 false, 返回返回包含名字的数组.
        """
        name_start, name_end = deal_start_end(name_start, name_end)
        name_end = name_end if name_end else '{}\xFF'.format(name_start)
        return bytes_to_str(self.execute_command('qlist', name_start, name_end, check_limit(limit)))

    def qrlist(self, name_start=None, name_end=None, limit=None) -> list:
        return self.qlist(name_start, name_end, limit)[::-1]

    def qclear(self, name) -> int:
        """
        :return: 清空队列的长度
        """
        return int(self.execute_command('qclear', c(name)))

    def qpush(self, name, item) -> int:
        """
        :return: 添加元素之后, 队列的长度
        """
        return int(self.execute_command('qpush', c(name), pickle_dumps(item)))

    def qpop(self, name):
        return pickle_loads(self.execute_command('qpop', c(name)))

    def qget(self, name, index=0):
        return pickle_loads(self.execute_command('qget', c(name), index))

    def qrange(self, name, offset: int = 0, limit: int = 0) -> list:
        """
        返回下标处于区域 [offset, offset + limit] 的元素.
        :param name: queue 的名字.
        :param offset: 整数, 从此下标处开始返回. 从 0 开始. 可以是负数, 表示从末尾算起.
        :param limit:
        :return:
        """
        x = self.execute_command('qrange', c(name), offset, check_limit(limit))
        return [pickle_loads(_) for _ in x]

    def qslice(self, name, begin=0, end=-1) -> list:
        x = self.execute_command('qslice', c(name), begin, end)
        return [pickle_loads(_) for _ in x] if isinstance(x, list) else []

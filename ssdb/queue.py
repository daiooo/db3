# coding=utf-8
from ssdb.todo import *


class Queue(Base):
    def qpush(self, name, item) -> int:
        """
        :return: 添加元素之后, 队列的长度
        """
        return int(self.execute_command('qpush', c(name), pickle_dumps(item)))

    def qpop(self, name) -> int:
        return pickle_loads(self.execute_command('qpop', c(name)))

    def qsize(self, name) -> int:
        return self.execute_command('qsize', c(name))

    def qclear(self, name) -> int:
        """
        :return: 清空队列的长度
        """
        return int(self.execute_command('qclear', c(name)))

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

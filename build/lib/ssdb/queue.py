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

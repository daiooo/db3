from . import TestCase
from munch import munchify

n1 = '11'
n2 = '22'
i1 = 0
i2 = [0, 0]


class TestGetSet(TestCase):
    def test_qpush(self):
        self.db.qclear(n1)
        self.assertEqual(1, self.db.qpush(n1, i1))
        self.assertEqual(2, self.db.qpush(n1, i2))

    def test_qpop(self):
        self.test_qpush()
        self.assertEqual(i1, self.db.qpop(n1))
        self.assertEqual(i2, self.db.qpop(n1))
        self.assertEqual(None, self.db.qpop(n1))

    def test_qsize(self):
        self.test_qpush()
        self.assertEqual(2, self.db.qsize(n1))
        self.db.qclear(n1)
        self.assertEqual(0, self.db.qsize(n1))

from . import TestCase
from munch import munchify

n1 = '11'
n2 = '22'
k1 = 0
k2 = [0, 0]
s1 = 55
s2 = 99


class TestGetSet(TestCase):
    def test_zset(self):
        self.db.zdel(n1, k1)
        self.assertEqual(1, self.db.zset(n1, k1, s1))  # new > 1
        self.assertEqual(0, self.db.zset(n1, k1, s1))
        self.assertIn(self.db.zset(n1, k2, s2), [0, 1])

    def test_zget(self):
        self.test_zset()
        self.assertEqual(s1, self.db.zget(n1, k1))

    def test_zdel(self):
        self.test_zset()
        self.assertIsInstance(self.db.zdel(n1, k1), int)
        self.assertIsInstance(self.db.zdel(n1, k1), int)
        self.assertEqual(0, self.db.zexists(n1, k1))

    def test_zincr(self):
        self.db.zdel(n1, k1)
        self.assertEqual(1, self.db.zincr(n1, k1))
        self.assertEqual(1 + 5, self.db.zincr(n1, k1, 5))
        self.assertEqual(1 + 5 - 5, self.db.zincr(n1, k1, -5))
        # digit
        self.db.zdel(n1, k1)
        self.assertEqual(10 ** (5 - 1) + 1, self.db.zincr(n1, k1, digit=5))  # 10001
        self.assertEqual(10 ** (5 - 1) + 2, self.db.zincr(n1, k1, digit=5))
        self.assertEqual(10 ** (5 - 1) + 3, self.db.zincr(n1, k1, digit=5))

    def test_zexists(self):
        self.db.zdel(n1, k1)
        self.assertEqual(0, self.db.zexists(n1, k1))
        self.db.zset(n1, k1, s1)
        self.assertEqual(1, self.db.zexists(n1, k1))

    def test_zsize(self):
        self.db.zclear(n1)
        self.assertEqual(0, self.db.zsize(n1))
        self.db.zset(n1, k1, s1)
        self.db.zset(n1, k2, s2)
        self.assertEqual(2, self.db.zsize(n1))

    def test_zlist(self):
        self.db.zset(n1, k1, s1)
        self.assertIn(n1, self.db.zlist(1))
        self.db.zset(n2, k2, s2)
        self.assertIn(n2, self.db.zlist(2))

        self.assertIn(n1, self.db.zlist())  # all
        self.assertIn(n2, self.db.zlist())  # all

    def test_zrlist(self):
        self.db.zset(n1, k1, s1)
        self.assertIn(n1, self.db.zrlist(1))
        self.db.zset(n2, k2, s2)
        self.assertIn(n2, self.db.zrlist(2))

        self.assertIn(n1, self.db.zrlist())  # all
        self.assertIn(n2, self.db.zrlist())  # all

    def test_zkeys(self):
        self.test_zset()
        self.assertIn(str(k1), self.db.zkeys(n1))
        self.assertIn(self.list_to_str(k2), self.db.zkeys(n1, 0))

    def test_zscan(self):
        self.test_zset()
        self.assertIn(str(k1), self.db.zscan(n1))

    ###
    def test_zclear(self):
        self.db.zclear(n1)
        self.assertEqual(0, self.db.zsize(n1))
        self.db.zset(n1, k1, s1)
        self.db.zset(n1, k2, s2)
        self.assertEqual(2, self.db.zsize(n1))
        self.db.zclear(n1)
        self.assertEqual(0, self.db.zsize(n1))

    def test_multi_zset(self):
        self.db.zclear(n1)
        self.db.multi_zset(n1, kvs={11: s1, 22: s2})
        self.assertEqual(2, self.db.zsize(n1))
        self.db.zclear(n1)

    def test_multi_zget(self):
        self.db.zset(n1, k1, s1)
        self.db.zset(n1, k2, s2)
        self.assertIn(str(k1), self.db.multi_zget(n1, [k1, '0_0']))
        self.assertIn('0_0', self.db.multi_zget(n1, [k1, '0_0']))

    def test_multi_zdel(self):
        self.db.zclear(n1)
        self.db.zset(n1, k1, s1)
        self.db.zset(n1, k2, s2)
        self.assertEqual(2, self.db.multi_zdel(n1, [k1, '0_0']))
        self.assertEqual(0, self.db.zsize(n1))

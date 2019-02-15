from . import TestCase
from munch import munchify

n1 = '11'
n2 = '22'
k1 = 0
k2 = [0, 0]
v1 = 123
v2 = {'111': 111, '222': munchify({'123': 123, '222': [11, 'aa']})}


class TestGetSet(TestCase):
    def test_hset(self):
        self.db.hdel(n1, k1)
        self.assertEqual(1, self.db.hset(n1, k1, v1))  # new > 1
        self.assertEqual(0, self.db.hset(n1, k1, v1))
        self.assertIn(self.db.hset(n1, k2, v2), [0, 1])

    def test_hget(self):
        self.db.hset(n1, k1, v1)
        self.db.hset(n1, k2, v2)
        self.assertEqual(v1, self.db.hget(n1, k1))
        self.assertEqual(v2, self.db.hget(n1, k2))

    def test_hdel(self):
        self.db.hset(n1, k1, v1)
        self.assertIsInstance(self.db.hdel(n1, k1), int)
        self.assertIsInstance(self.db.hdel(n1, k1), int)
        self.assertEqual(0, self.db.hexists(n1, k1))

    def test_hincr(self):
        self.db.hdel(n1, k1)
        self.assertEqual(1, self.db.hincr(n1, k1))
        self.assertEqual(1 + 5, self.db.hincr(n1, k1, 5))

    def test_hexists(self):
        self.db.hdel(n1, k1)
        self.assertEqual(0, self.db.hexists(n1, k1))
        self.db.hset(n1, k1, v1)
        self.assertEqual(1, self.db.hexists(n1, k1))

    def test_hsize(self):
        self.db.hclear(n1)
        self.assertEqual(0, self.db.hsize(n1))
        self.db.hset(n1, k1, v1)
        self.db.hset(n1, k2, v2)
        self.assertEqual(2, self.db.hsize(n1))

    def test_hlist(self):
        self.db.hset(n1, k1, v1)
        self.assertIn(n1, self.db.hlist(1))
        self.db.hset(n2, k2, v2)
        self.assertIn(n2, self.db.hlist(2))

        self.assertIn(n1, self.db.hlist())  # all
        self.assertIn(n2, self.db.hlist())  # all

    def test_hkeys(self):
        self.test_hset()
        self.assertIn(str(k1), self.db.hkeys(n1))
        self.assertIn(self.list_to_str(k2), self.db.hkeys(n1, 0))

    def test_hgetall(self):
        self.test_hset()
        self.assertIn(str(k1), self.db.hgetall(n1))

    def test_hscan(self):
        self.test_hset()
        self.assertIn(v1, self.db.hscan(n1))
        self.assertEqual(self.db.hgetall(n1), self.db.hscan(n1, r='d'))

    ###
    def test_hclear(self):
        self.db.hclear(n1)
        self.assertEqual(0, self.db.hsize(n1))
        self.db.hset(n1, k1, v1)
        self.db.hset(n1, k2, v2)
        self.assertEqual(2, self.db.hsize(n1))
        self.db.hclear(n1)
        self.assertEqual(0, self.db.hsize(n1))

    def test_multi_hset(self):
        self.db.hclear(n1)
        self.db.multi_hset(n1, kvs=v2)
        self.assertEqual(2, self.db.hsize(n1))
        self.db.hclear(n1)

    def test_multi_hget(self):
        self.db.hset(n1, k1, v1)
        self.db.hset(n1, k2, v2)
        self.assertIn(str(k1), self.db.multi_hget(n1, [k1, '0_0']))
        self.assertIn('0_0', self.db.multi_hget(n1, [k1, '0_0']))

    def test_multi_hdel(self):
        self.db.hclear(n1)
        self.db.hset(n1, k1, v1)
        self.db.hset(n1, k2, v2)
        self.assertEqual(2, self.db.multi_hdel(n1, [k1, '0_0']))
        self.assertEqual(0, self.db.hsize(n1))

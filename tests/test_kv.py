from . import TestCase, pf
import time

k1 = 0
k2 = [0, 0]
k_not = 'k_not'
v1 = 0
v2 = {'a': 1, 'b': [2, 3]}
ttl = 1


class TestGetSet(TestCase):
    # def clear(self):
    #     self.db.multi_del(self.db.keys())

    def test_set(self):
        self.assertEqual(1, self.db.set(k1, v1))
        self.assertEqual(1, self.db.set(k2, v2))
        # error
        self.assertRaises(AssertionError, self.db.set, '', v1)
        self.assertRaises(AssertionError, self.db.set, None, v1)

    def test_setx(self):
        self.db.delete(k1)
        self.assertEqual(1, self.db.setx(k1, v1, ttl))
        self.assertEqual(1, self.db.setx(k1, v1, ttl))
        time.sleep(0.5)
        self.assertEqual(1, self.db.exists(k1))
        time.sleep(0.6)
        self.assertEqual(0, self.db.exists(k1))

        # self.assertEqual(1, self.db.setnx('ttt', v, ttl))

    def test_setnx(self):  # 当 key 不存在时, 设置指定 key 的值内容.(1) / 如果已存在, 则不设置.(0)
        # 不会自动删除，setnx有问题
        pass

    def test_expire(self):
        self.db.set(k1, v1)
        self.assertEqual(1, self.db.expire(k1, 5))  # 如果 key 存在并设置成功, 返回 1
        self.assertEqual(5, self.db.ttl(k1))

        self.db.delete(k1)
        self.assertEqual(0, self.db.expire(k1, ttl))  # 如果 key 不存在, 返回 0.

    def test_ttl(self):
        self.db.setx(k1, v1, ttl)
        self.assertEqual(ttl, self.db.ttl(k1))
        time.sleep(ttl + 0.1)
        self.assertEqual(-1, self.db.ttl(k1))

    def test_get(self):
        self.db.set(k1, v1)
        self.db.set(k2, v2)
        # get
        self.assertEqual(v1, self.db.get(k1))
        self.assertEqual(v2, self.db.get(k2))
        self.assertEqual(None, self.db.get(k_not))

    def test_getset(self):
        pass

    def test_delete(self):
        self.db.set(k1, v1)
        self.assertEqual(1, self.db.delete(k1))
        self.assertEqual(1, self.db.delete(k_not))

    def test_incr(self):
        self.db.delete(k1)
        self.assertEqual(1, self.db.incr(k1, 1))
        self.assertEqual(1 + 5, self.db.incr(k1, '5'))
        self.assertRaises(ValueError, self.db.incr, k1, 'abc')

    def test_exists(self):
        self.db.set(k1, v1)
        self.assertEqual(1, self.db.exists(k1))
        self.db.delete(k1)
        self.assertEqual(0, self.db.exists(k1))

    def test_keys(self):
        self.db.set(k1, v1)
        self.db.set(k2, v2)
        self.assertIn('0_0', self.db.keys())  # k2 0_0
        self.assertIn('0_0', self.db.keys(0))  # k2 0_0

    def test_rkeys(self):
        self.db.set('0_1', v1)
        self.db.set('0_2', v2)
        self.assertIn('0_0', self.db.rkeys(0))  # k2 0_0
        self.assertIn('0_0', self.db.rkeys())  # k2 0_0

    def test_scan(self):
        self.db.set(k2, v1)
        self.assertIn(v1, self.db.scan())  # k2 0_0
        self.assertIn(v1, self.db.scan(0))  # k2 0_0
        self.assertIn('0_0', self.db.scan(0, r='d'))  # k2 0_0

    def test_rscan(self):
        self.db.set(k2, v1)
        self.assertIn(v1, self.db.rscan())  # k2 0_0
        self.assertIn(v1, self.db.rscan(0))  # k2 0_0
        self.assertIn('0_0', self.db.rscan(0, r='d'))  # k2 0_0

    def test_multi_set_get_del(self):
        # set
        kvs = {'mm1a': 'x1', 'mm1b': {'x2': 'x2', 'x3': [1, .2]}}
        self.assertIsInstance(self.db.multi_set(kvs), int)
        # get
        self.assertEqual(list(kvs.values()), self.db.multi_get(kvs))
        self.assertEqual(kvs, self.db.multi_get(kvs, r='d'))
        # del
        self.assertIsInstance(self.db.multi_del(kvs.keys()), int)
        self.assertEqual([], self.db.multi_get(kvs))

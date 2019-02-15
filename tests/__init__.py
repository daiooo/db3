import unittest
import ssdb


class TestCase(unittest.TestCase):

    def setUp(self):
        self.db = ssdb.Client(port=10000)

    def tearDown(self):
        self.db.disconnect()

    def list_to_str(self, a):
        if isinstance(a, list):
            a = '_'.join([str(i) for i in a])
        else:
            a = str(a) if a or a == 0 else ''
        return a


def pf(v):
    print(f'{str(type(v)):<30} {str(v):<}')

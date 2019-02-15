import ssdb
from munch import munchify

db = ssdb.Client(port=10000)


def pf(v):
    print(f'{str(type(v)):<30} {str(v):<}')


# pf(db.set('0', munchify({'123': 123, '222': [11, 'aa']})))
# pf(db.get('0'))
# pf(db.hset('0', [0, 0], munchify({'123': 123, '222': [11, 'aa']})))
# pf(db.hset('0', [0, 0]))

# pf(db.hset('0', 2, 123))
# pf(db.multi_hset('0', {'111': 1111, '222': munchify({'123': 123, '222': [11, 'aa']})}))
# pf(db.hget(0, 111))
# pf(db.hget(0, 222))
print(type(1).__name__)
pf(db.set(10, {'123': 111, 'a': [1, .2]}))
pf(db.set(11, '123456'))
pf(db.set(22, '123456'))
pf(db.set(33, '123456'))
pf(db.setnx(1))
pf(db.multi_set())
pf(db.multi_get(['1a', '1b']))
pf(db.multi_del(['1ax', '1b']))

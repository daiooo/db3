import ssdb  # db3

db = ssdb.Client(host='d', port=10000)
print(db.hset(1, 1, 1))

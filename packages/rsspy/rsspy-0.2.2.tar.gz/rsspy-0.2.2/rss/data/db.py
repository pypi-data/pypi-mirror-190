#!/usr/bin/env python
# from codefast.io.osdb import osdb
# db = osdb('/tmp/rsscache')

# if __name__ == '__main__':
#     for _ in range(1000):
#         db.set('foo', 'bar')
#     print(db.get('foo'))

import redis 
db = redis.Redis(host='localhost', port=6379)

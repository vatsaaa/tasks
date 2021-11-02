## Keep the order of imports
from waitress import serve
from config.config import app

import redis

def db_connect():
    r = redis.Redis(host='redis-16582.c264.ap-south-1-1.ec2.cloud.redislabs.com', port=16582, password='vatsaaa@R3D!5')
    r.set('hello', 'world')
    print(r.get('hello'))

if __name__ == '__main__':
    serve(app=app, host='127.0.0.1', port=5454)


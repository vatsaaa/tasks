import os
from config.config import app, ALLOWED_EXTENSIONS
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime as dt
import redis


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## Just some code to check connectivity to Redis Cloud Instance
def db_connect():
    r = redis.Redis(host='redis-16582.c264.ap-south-1-1.ec2.cloud.redislabs.com', port=16582, password='50m3p@55w0rd')
    r.set('hello', 'world')
    print(r.get('hello'))

def ping(suffix=None):
    resp_str = "User ping, tasks pong / " + dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    resp = resp_str if suffix is None else resp_str + " / " + suffix

    db_connect()
    
    return resp

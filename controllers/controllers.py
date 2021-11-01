import os
from config.config import app, ALLOWED_EXTENSIONS
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime as dt


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ping(suffix=None):
    resp_str = "User ping, tasks pong / " + dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    resp = resp_str if suffix is None else resp_str + " / " + suffix
    
    return resp

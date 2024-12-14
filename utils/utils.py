import functools

from config.config import ALLOWED_EXTENSIONS

def singleton(cls):
    """Decorator to make a class Singleton"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton

def allowed_file(filename, allow_all: bool = False):
    if allow_all:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


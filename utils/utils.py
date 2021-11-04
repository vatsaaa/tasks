from config.config import ALLOWED_EXTENSIONS


def allowed_file(filename, allow_all: bool = False):
    if allow_all:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


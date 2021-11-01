## Keep the order of imports
from waitress import serve
from config.config import app

if __name__ == '__main__':
    serve(app=app, host='127.0.0.1', port=5454)


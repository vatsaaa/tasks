from celery import Celery
from config import app

app.app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.app.name, broker=app.app.config['CELERY_BROKER_URL'])
celery.conf.update(app.app.config)
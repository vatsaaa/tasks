from celery import Celery
from config.config import app

# Celery-app configuration
redis_host = '127.0.0.1'
redis_port = '6379' ## Default port for redis
redis_db = 0

http_scheme = 'http://'

broker_url = 'redis://%s:%s/%s' % (redis_host, redis_port, redis_db)
result_backend =  'redis://%s:%s/0' % (redis_host, redis_port)

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Kolkata'
enable_utc = True

task_routes = {
    'tasks.taskqueue.enqueue_tasks': {
        'queue': 'DISPQ', 
        'routing_key': 'DISPQ'
    }
}

celery_app = Celery(app.app)

celery_app.conf.update(
    {
        'broker_url': broker_url,
        'imports': [],
        'task_routes': task_routes,
        'task_serializer': task_serializer,
        'result_serializer': result_serializer,
        'accept_content': accept_content,
        'timezone': timezone,
        'enable_utc': enable_utc,
        'task_acks_late': True,
        'result_backend': result_backend,
        'task_track_started': True
    }
)

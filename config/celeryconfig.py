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

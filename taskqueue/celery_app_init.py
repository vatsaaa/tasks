from celery import Celery
from config.config import app
from config.celeryconfig import broker_url, backend_url, task_routes, task_serializer, result_serializer
from config.celeryconfig import timezone, accept_content, enable_utc, result_backend

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


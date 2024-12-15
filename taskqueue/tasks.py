import sys
from config.celeryconfig import celery_app
from executor.PrintTask import PrintTask
from executor.DisplayTask import DisplayTask
from executor.IgnoreTask import IgnoreTask
from celery.result import AsyncResult
from appexception import AppException

# These are task functions that get executed async from the controller module
@celery_app.task(acks_late=True, default_retry_delay=1 * 60)
def enqueue_task(data: dict):
    if data['tasktype'] == 'TASKQ':
        task = PrintTask(data)
    elif data['tasktype'] == 'DISPQ':
        task = DisplayTask(data)
    else:
        task = IgnoreTask(data)

    task.run()

    task.persist(todb=True)

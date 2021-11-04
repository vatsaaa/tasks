from executor.PrintTask import PrintTask
from config.celeryconfig import celery_app
from celery.result import AsyncResult


# These are task functions that get executed async from the controller module
@celery_app.task(acks_late=True)
def enqueue_task(data: dict):
    task = PrintTask(data)

    task.run()
    task.persist(todb=True)



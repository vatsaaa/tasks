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

def get_celery_queue_len(queue_name: str = 'celery'):
    with celery_app.pool.acquire(block=True) as connection:
        return connection.default_channel.client.llen(queue_name)

def get_celery_queue_items(queue_name: str = 'celery'):
    import base64
    import json

    with celery_app.pool.acquire(block=True) as connection:
        tasks = connection.default_channel.client.lrange(queue_name, 0, -1)

    decoded_tasks = []

    if tasks:
        for task in tasks:
            j = json.loads(task)
            body = json.loads(base64.b64decode(j['body']))
            decoded_tasks.append(body)

    return decoded_tasks

def get_task_state(taskid: str):
    taskstatus = {'taskid': taskid}

    try:
        res = AsyncResult(taskid, app=celery_app)

        print('Caught celery task:', res, res.info)

        if res.failed():
            taskstatus['task-status'] = 'FAILED'
        elif res.ready() and res.result != 0:
            taskstatus['task-status'] = 'FAILED'
        elif res.successful():
            taskstatus['task-status'] = 'SUCCESS'
        else:
            taskstatus['task-status'] = res.state
    except KeyError:
        print("Error parsing Celery data")
        taskstatus['task-status'] = 'FAILED'
    except AttributeError:
        taskstatus['task-status'] = 'DISABLED'
    except AppException as e:
        print(e)
        print("error=" + str(sys.exc_info()[0]))
    
    return taskstatus
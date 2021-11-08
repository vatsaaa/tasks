import re
import sys
import requests

from executor.PrintTask import PrintTask
from executor.DisplayTask import DisplayTask
from executor.IgnoreTask import IgnoreTask

from config.celeryconfig import celery_app
from celery.result import AsyncResult

from appexception import AppException


# These are task functions that get executed async from the controller module
@celery_app.task(acks_late=True)
def enqueue_task(data: dict):
    if data['tasktype'] == 'TASKQ':
        task = PrintTask(data)
    elif data['tasktype'] == 'DISPQ':
        task = DisplayTask(data)
    else:
        task = IgnoreTask(data)

    task.run()
    task.persist(todb=True)

def filter_tasks_by_arg(tasktype: str, tasks, arg_filters: list):
    filtered_tasks = {}

    if tasks is None:
        return filtered_tasks

    for (argname, argvalue, optional) in arg_filters:
        if optional and (argvalue is None or len(str(argvalue)) == 1):
            print("Skipping filtering for {argname}".format(argname=argname))
            continue

        print("Filtering for {argname} = {argvalue}".format(argname=argname, argvalue=argvalue))
        for taskid, taskdetails in prev_filter.items():
            args = taskdetails['args']

            found_args_tasktype = args[15:20]
            if found_args_tasktype == tasktype and argname == 'taskid' and argvalue == taskid:
                    return {taskid: taskdetails}
                
            found_args = re.compile('\'' + argname + '\':  \'[a-zA-Z0-9-]{6,}\'').findall(str(args))
            if found_args is not None and len(found_args) > 0:
                print("Found in task {foundtask}".format(foundtask=found_args[0]))
                filtered_tasks[taskid] = taskdetails

            print("Filtered {numtasks} tasks".format(numtasks=len(filtered_tasks)))
            prev_filter = filtered_tasks.copy()
            filtered_tasks = {}

    return prev_filter


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
            j = json.loads(taks)
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


def get_flower_tasks(tasktype: str, batchid: str, username: str = None, taskid: str = None, taskstatus: str = None):
    if taskstatus is not None:
        params = {'state': taskstatus.upper()}
    else:
        params = {}

    url = http_scheme + flower_host + flower_port + '/api/tasks/'

    print("Sending request to url {url} with params {params}".format(url=url, params=params))

    response = requests.get(url, params=params)
    tasks = response.json()
    if response.status_code != 200:
        print("Retrieved invalid response from flower: ", response.text)

    arg_filters = [
        ('user', username, True),
        ('batchid', batchid, True),
        ('taskid', taskid, True)
    ]

    return filter_tasks_by_arg(tasktype, tasks, arg_filters)

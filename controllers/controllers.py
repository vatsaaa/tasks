import base64, json, os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime as dt

from config.config import ALLOW_ALL_FILE_TYPES, app as capp
from utils.utils import allowed_file
from appexception import AppException
from taskqueue import tasks
from config.celeryconfig import celery_app

def ping(suffix=None):
    resp_str = "User ping, tasks pong / " + dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    resp = resp_str if suffix is None else resp_str + " / " + suffix

    pong = jsonify(resp)
    pong.status_code = 200

    return resp

def create_task(username: str, tasktype: str, batchid: str, taskdelay: int = 2) -> dict:
    # Check if the post request has a file to work with
    if 'filename' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['filename']

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename, ALLOW_ALL_FILE_TYPES):
        filename = secure_filename(file.filename)

        # Only if the file was successfully saved, the async function needs to run
        # TODO: File successfully saves to disk, this should be saved to an external location e.g. S3 bucket
        try:
            file.save(os.path.join(capp.app.config['UPLOAD_FOLDER'], filename))
        except FileNotFoundError as fnf:
            raise AppException(fnf)
        except Exception as e:
            raise AppException(e)
        else:
            print("Task requested for {tasktype} for filename {filename}".format(tasktype=tasktype, filename=filename))
            args = [{
                    'tasktype': tasktype,
                    'batchid': batchid,
                    'username': username,
                    'filepath': capp.app.config['UPLOAD_FOLDER'],
                    'filename': filename,
                    'upload date/time': dt.now().strftime("%B %d, %Y %H:%M:%S")
            }]
            submitted = tasks.enqueue_task.apply_async(
                args, countdown = taskdelay, queue = tasktype, 
                track_started = True, task_ignore_result = False
                )
        if submitted:
            resp = jsonify({
                'message': 'Task successfully submitted to queue {tasktype} for creation'.format(tasktype=tasktype),
                'filepath': capp.app.config['UPLOAD_FOLDER'],
                'filename': filename,
                'username': username,
                'batchid': batchid,
                'task_id': submitted.task_id
            })
            resp.status_code = 201
        else:
            resp = jsonify({'message': 'Failed to create task in {tasktype}'.format(tasktype=tasktype)})
        
        return resp
    else:
        resp = jsonify({'message': 'Allowed filetypes are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

def list_tasks(username: str, tasktype: str, batchid: str=None, taskid: str=None):
    if not username:
        raise AppException("A user can only fetch tasks created by them. Please specify a valid username")

    if not tasktype:
        raise AppException("Please specify the task queue to fetch tasks from!")
    
    tasks = []
    with celery_app.pool.acquire(block=True) as conn:
        tasks = conn.default_channel.client.lrange(tasktype, 0, -1)
    
    decoded_tasks = []
    for task in tasks:
        j = json.loads(task.decode('utf-8'))
        body = json.loads(base64.b64decode(j['body']))
        header_taskid = j['headers']['id']
        body[0][0]['taskid'] = header_taskid
        
        if body[0][0]['batchid'] == batchid or batchid is None:
            if body[0][0]['taskid'] == taskid or taskid is None:
                decoded_tasks.append(body)
    
    return jsonify(decoded_tasks)

def update_tasks(username: str, tasktype: str, batchid: str, taskid: str=None) -> dict:
    resp = {}
    print("Updating task for {username} in task queue {tasktype}".format(username=username, tasktype=tasktype))
    fetched_tasks = list_tasks(tasktype, batchid, username, taskid)

    if len(fetched_tasks) == 0:
        resp = jsonify({'message': 'No tasks found for {username} in task queue {tasktype}'.format(username=username, tasktype=tasktype)})
        resp.status_code = 404
    elif len(fetched_tasks) > 1:
        resp = jsonify({'message': 'Multiple tasks found for {username} in task queue {tasktype}'.format(username=username, tasktype=tasktype)})
        resp.status_code = 404
    else:
        resp = jsonify({
            'task': fetched_tasks[0],
            'tasktype': tasktype,
            'batchid': batchid,
            'username': username,
            'taskid': taskid
            })
        resp.status_code = 200

    return resp
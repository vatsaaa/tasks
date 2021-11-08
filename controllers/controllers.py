import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime as dt
import redis

from config.config import ALLOW_ALL_FILE_TYPES, app
from utils.utils import allowed_file
from appexception import AppException
from taskqueue import tasks


## Just some code to check connectivity to Redis Cloud Instance
def db_connect():
    r = redis.Redis(host='redis-16582.c264.ap-south-1-1.ec2.cloud.redislabs.com', port=16582, password='vatsaaa@R3d!5')
    r.set('hello', 'world')
    print(r.get('hello'))

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
            file.save(os.path.join(app.app.config['UPLOAD_FOLDER'], filename))
        except FileNotFoundError as fnf:
            raise AppException(fnf)
        except Exception as e:
            raise AppException(e)
        else:
            print("Task requested for {tasktype} for filename {filename}".format(tasktype=tasktype, filename=filename))
            submitted = tasks.enqueue_task.apply_async(
                args = [{
                    'tasktype': tasktype,
                    'batchid': batchid,
                    'user': username,
                    'filepath': app.app.config['UPLOAD_FOLDER'],
                    'filename': filename,
                    'upload date/time': dt.now().strftime("%B %d, %Y %H:%M:%S")
                    }],
                countdown = taskdelay,
                queue = tasktype,
                track_started = True,
                task_ignore_result = False
            )

        if submitted:
            resp = jsonify({
                'message': 'Task successfully submitted to {tasktype} for creation'.format(tasktype=tasktype),
                'filepath': app.app.config['UPLOAD_FOLDER'],
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

def list_tasks(tasktype: str, batchid: str = None, username: str = None, taskid: str = None, taskstatus: str = None):
    resp = tasks.get_flower_tasks(tasktype, batchid, username, taskid, taskstatus)
    return resp

def update_task():
    # TODO: Implement soon
    pass

def get_task():
    # TODO: Implement soon
    pass


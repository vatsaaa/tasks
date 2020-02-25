import os
from config import app
from flask import request, jsonify
from werkzeug.utils import secure_filename
import tasks

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload():
    # check if the post request has the file part
    if 'filename' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['filename']

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Only if file was successfully saved, asycn function needs to be run
        try:
            file.save(os.path.join(app.app.config['UPLOAD_FOLDER'], filename))
        except FileNotFoundError as fnf:
            raise Exception(fnf)
        except:
            raise Exception("Unknown exception occurred!")
        else:
            tasks.async_print.apply_async(
                args=[{
                    'message': 'File successfully uploaded',
                    'filename': filename
                }],
                countdown=60)

        resp = jsonify({
            'message': 'File successfully uploaded',
            'filename': filename
        })
        resp.status_code = 201

        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

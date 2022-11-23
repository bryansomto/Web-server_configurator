from flask import Flask, Blueprint, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pathlib import Path

methods = Blueprint('methods', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pem', 'ppk', 'pub'}
UPLOAD_FOLDER = str(Path.home())
STORAGE_FOLDER = str(Path.cwd()) + '/fileStorage'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileUploadHandler():
    server_name = request.form.get('server_name')
    ip_addr = request.form.get('ip_addr')

    if 'id_file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)

    file = request.files['id_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        if not os.path.exists(app.config['STORAGE_FOLDER']):
            os.makedirs(app.config['STORAGE_FOLDER'])

        file.save(os.path.join(app.config['STORAGE_FOLDER'], filename))

        return redirect(url_for('views.nginx_config'))

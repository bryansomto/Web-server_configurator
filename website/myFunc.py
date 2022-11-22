import os
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

myFunc = Blueprint('myFunc', __name__)

UPLOAD_FOLDER = '../../USER_KEYS'
ALLOWED_EXTENSIONS = {'txt', 'pem', 'ppk'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

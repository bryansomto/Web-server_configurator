from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from .myFunc import allowed_file


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('views.nginx_config'))
    return render_template("home.html", user=current_user)

@views.route('/nginx-config', methods=['GET', 'POST'])
@login_required
def nginx_config():
    if request.method == 'POST':

        UPLOAD_FOLDER = str(Path.home())
        STORAGE_FOLDER = str(Path.cwd()) + '/fileStorage'
        ALLOWED_EXTENSIONS = {'txt', 'pem', 'ppk', 'pub'}

        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['STORAGE_FOLDER'] = STORAGE_FOLDER

        server_name = request.form.get('server_name')
        ip_addr = request.form.get('ip_addr')

        print(request.files, server_name, ip_addr)
        
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
            
            print ('Saved')
            
            return redirect(url_for('views.nginx_config'))
    
    return render_template("nginx-config.html", user=current_user)

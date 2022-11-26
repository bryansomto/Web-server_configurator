from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from .methods import paramikoHandler, fileUploadHandler


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
        server_name = request.form.get('server_name')
        ip_addr = request.form.get('ip_addr')
        private_key = request.files['private_key'].filename
        passphrase = request.form.get('passphrase')

        fileUploadHandler()
        paramikoHandler(server_name, ip_addr, private_key, passphrase)

    return render_template("nginx-config.html", user=current_user)

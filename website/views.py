from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from .methods import fileUploadHandler


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
        fileUploadHandler()

    return render_template("nginx-config.html", user=current_user)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('views.nginx_config'))
    return render_template("home.html", user=current_user)

@views.route('/nginx-config')
@login_required
def nginx_config():
    return render_template("nginx-config.html", user=current_user)

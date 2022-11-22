from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

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
        id_file = request.form['id_file']
        
        f = open(id_file, "r", encoding="UTF-8")
        print (f.read())
    return render_template("nginx-config.html", user=current_user)

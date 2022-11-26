from flask import Flask, Blueprint, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from os import path, getcwd, makedirs
from paramiko import SSHClient, AutoAddPolicy, ssh_exception

methods = Blueprint('methods', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pem', 'ppk', 'pub'}
STORAGE_FOLDER = getcwd() + '/fileStorage'

app = Flask(__name__)
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileUploadHandler():
    if 'private_key' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)

    file = request.files['private_key']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # type: ignore

        if not path.exists(app.config['STORAGE_FOLDER']):
            makedirs(app.config['STORAGE_FOLDER'])

        file.save(path.join(app.config['STORAGE_FOLDER'], filename))

    else:
        flash('file format not supported', category='error')
        return redirect(url_for('views.nginx_config'))


# SSH login handler
def paramikoHandler(server_name, ip_addr, private_key, passphrase=None):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    try:
        if (passphrase is not None):
            ssh.connect(ip_addr, username=server_name, password=passphrase,
                        key_filename=path.join(path.expanduser('~'), ".ssh", private_key))
        else:
            ssh.connect(ip_addr, username=server_name,
                        key_filename=path.join(path.expanduser('~'), ".ssh", private_key))
    except (ssh_exception.NoValidConnectionsError, ssh_exception.BadAuthenticationType, ssh_exception.PasswordRequiredException, ValueError) as error:
        print(error)
        flash(str(error), category='error')  # type: ignore
        return redirect(url_for('views.nginx_config'))

    stdin, stdout, stderr = ssh.exec_command(
        "ls; cd .")
    output = stdout.readlines()
    error = stderr.readlines()

    if output:
        print([line.strip() for line in output])
        flash('Success', category='success')
    if error:
        print([line.strip() for line in output])
        flash('Failed', category='error')

    # Cleanup
    ssh.close()

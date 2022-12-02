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


class File():
    def __init__(self, file):
        self.file = file

    def read_file(self):
        filename = secure_filename(self.file.filename)  # type: ignore

        if not path.exists(app.config['STORAGE_FOLDER']):
            makedirs(app.config['STORAGE_FOLDER'])

        self.file.save(path.join(app.config['STORAGE_FOLDER'], filename))

        with open(f"{app.config['STORAGE_FOLDER']/filename}") as f:
            file_content = f.read().splitlines

        return file_content

    def fileUploadHandler(self):
        if 'private_key' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        self.file = request.files['private_key']
        if self.file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        if self.file and allowed_file(self.file.filename):
            # self.read_file(self.file)  # type: ignore
            filename = secure_filename(self.file.filename)  # type: ignore

            if not path.exists(app.config['STORAGE_FOLDER']):
                makedirs(app.config['STORAGE_FOLDER'])

            self.file.save(path.join(app.config['STORAGE_FOLDER'], filename))

            file_path = STORAGE_FOLDER + filename
            print(file_path)
            with open(file_path, 'r') as f:
                file_content = f.read().splitlines

            return file_content

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
        "sudo apt-get -y install nginx; sudo systemctl restart nginx")
    output = stdout.readlines()
    error = stderr.readlines()

    if output:
        print([line.strip() for line in output])
        flash(output[3], category='success')
    if error:
        print([line.strip() for line in output])
        flash('Failed', category='error')

    # Cleanup
    ssh.close()

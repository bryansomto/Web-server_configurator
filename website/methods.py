""" Provides application core methods and function """
from flask import Flask, Blueprint, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from os import path, getcwd, makedirs, chmod
from paramiko import SSHClient, AutoAddPolicy, ssh_exception

methods = Blueprint('methods', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pem', 'ppk', 'pub'}
STORAGE_FOLDER = getcwd() + '/fileStorage'

app = Flask(__name__)
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER


def allowed_file(filename):
    """ Allowed file type handler """
    filename = filename
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class File():
    """ Handles file input is processing """

    def __init__(self, file):
        """ Initialize a new file method """
        self.file = file

    def fileUploadHandler(self):
        """ Handles file upload """
        if 'private_key' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        self.file = request.files['private_key']
        if self.file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        if self.file and allowed_file(self.file.filename):

            filename = secure_filename(self.file.filename)  # type: ignore

            if not path.exists(app.config['STORAGE_FOLDER']):
                makedirs(app.config['STORAGE_FOLDER'])

            self.file.save(path.join(app.config['STORAGE_FOLDER'], filename))

            file_path = path.join(app.config['STORAGE_FOLDER'], filename)

            return file_path

        else:
            flash('file format not supported', category='error')
            return redirect(url_for('views.nginx_config'))


def paramikoHandler(server_name, ip_addr, key, passphrase=None):
    """ SSH session handler """
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    # Connect to SSH client
    try:
        if (passphrase is not None):
            ssh.connect(ip_addr, username=server_name,
                        password=passphrase, key_filename=key)
        else:
            ssh.connect(ip_addr, username=server_name, key_filename=key)

    # Handle SSH client errors
    except (ssh_exception.NoValidConnectionsError, ssh_exception.BadAuthenticationType, ssh_exception.PasswordRequiredException, ValueError) as error:
        print(error)
        flash(str(error), category='error')  # type: ignore
        return redirect(url_for('views.nginx_config'))

    # Commands to execute
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

    # Close SSH session
    ssh.close()

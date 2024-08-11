import os.path
import logging

from flask import (Blueprint, request, render_template, flash, redirect, send_from_directory, current_app)
import urllib.parse
from werkzeug.utils import secure_filename

from .file_manager import get_file_manager
from .tfa import generate_otpauth_url, generate_secret_key
from .utils import file_is_allowed, filename_exists, file_save



_logger = logging.getLogger(__name__)


vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@vaulture_bp.route('/new_account', methods=['GET', 'POST'])
def vaulture_new_account():
    if request.method == 'POST':
        new_account_file = request.files['vault_file']
        new_account_name = secure_filename(new_account_file.filename).split('.')[0]
        new_account_otp_key = generate_secret_key()

        try:
            # get the file manager related to env
            filemanager = get_file_manager()

            # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault
            filemanager.file_create(
                new_account_file.filename, f'tmp_vaults/{current_app.config["UPLOAD_FOLDER"]}/{new_account_name}', 
                create_dirs=True
            )

            # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault.key
            filemanager.file_create(
                f'{new_account_otp_key}.key', f'tmp_vaults/{current_app.config["UPLOAD_FOLDER"]}/{new_account_name}'
            )            
        except FileExistsError as fer:
            return "Username already exists", 409
        
        return render_template('vaulture_new_account.html', otpurl=urllib.parse.quote(generate_otpauth_url(secret_key=new_account_otp_key, username=new_account_name)))

    return render_template('vaulture_new_account.html')

@vaulture_bp.route('/file', methods=['GET', 'POST'])
def vaulture_fileget():
    if request.method == 'POST':
        filename = request.form['filename']

        if not filename:
            flash('Please enter the name of the .vault file to retrieve', category='error')
            return

    return render_template('vaulture_fileget.html')

@vaulture_bp.route('/file/upload', methods=['GET', 'POST'])
def vaulture_fileupload():
    if request.method == 'POST':
        if 'vault_file' not in request.files:
            flash('No vault file provided', category='error')
            return redirect(request.url)

        file = request.files['vault_file']

        if not file_is_allowed(file) or filename_exists(file):
            flash('Selected file is invalid, please check the file and its extension', category='error')
            return redirect(request.url)

        try:
            filename = file_save(file)
        except FileExistsError:
            flash('An error occured while uploading the file, try again later', category='error')
            return redirect(request.url)

        flash(f'File {filename} successfully uploaded !', category='success')

        return render_template('vaulture_fileupload.html')

    return render_template('vaulture_fileupload.html')

@vaulture_bp.route('/file/create', methods=['GET', 'POST'])
def vaulture_filecreate():
    root_dir = os.path.dirname(os.getcwd())
    upload_dir = os.path.join(root_dir, current_app.config['UPLOAD_FOLDER'])

    _logger.error(upload_dir)

    try:
        response = send_from_directory(upload_dir, 'test.vault', as_attachment=True)
    except Exception as ex:
        _logger.error(ex)
        return render_template('vaulture_filecreate.html')

    _logger.error(response)

    return response
    #return render_template('vaulture_filecreate.html')

@vaulture_bp.route('/file/list', methods=['GET'])
def vaulture_filelist():
    return render_template('vaulture_filelist.html')
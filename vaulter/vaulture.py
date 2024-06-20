import os

from flask import (Blueprint, request, render_template, flash, redirect, current_app)
from .utils import file_is_allowed, filename_exists, file_save
from werkzeug.utils import secure_filename

vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@vaulture_bp.route('/file', methods=['GET', 'POST'])
def vaulture_fileget():
    if request.method == 'POST':
        filename = request.form['filename']

        if not filename:
            flash('Please enter the name of the .vault file to retrieve', category='error')
            return

        return render_template('')

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
    return render_template('vaulture_filecreate.html')

@vaulture_bp.route('/file/list', methods=['GET'])
def vaulture_filelist():
    return render_template('vaulture_filelist.html')
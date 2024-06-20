from flask import (Blueprint, request, render_template, flash)

vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@vaulture_bp.route('/file', methods=['GET', 'POST'])
def vaulture_fileget():
    if request.method == 'POST':
        filename = request.form['filename']

        if not filename:
            flash('Please enter the name of the .vault file to retrieve')
            return

        return render_template('')

    return render_template('vaulture_fileget.html')

@vaulture_bp.route('/file/upload', methods=['GET', 'POST'])
def vaulture_fileupload():
    if request.method == 'POST':
        pass

    return render_template('vaulture_fileupload.html')

@vaulture_bp.route('/file/create', methods=['GET', 'POST'])
def vaulture_filecreate():
    return render_template('vaulture_filecreate.html')

@vaulture_bp.route('/file/list', methods=['GET'])
def vaulture_filelist():
    return render_template('vaulture_filelist.html')
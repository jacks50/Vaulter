from flask import (Blueprint, request, render_template, flash)

vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@vaulture_bp.route('/file', methods=['GET', 'POST'])
def vaulturefile_get():
    if request.method == 'POST':
        filename = request.form['filename']

        if not filename:
            flash('Please enter the name of the .vault file to retrieve')
            return

        return render_template('')

    return render_template('vaulture_fileget.html')

@vaulture_bp.route('/file/upload', methods=['GET', 'POST'])
def vaulturefile_upload():
    if request.method == 'POST':
        pass

    return render_template('vaulture_fileupload.html')

@vaulture_bp.route('/file/create', methods=['GET', 'POST'])
def vaulturefile_create():
    pass

@vaulture_bp.route('/admin', methods=['GET'])
def vaulturefile_admin():
    pass
import logging
import traceback
import urllib.parse

from flask import (Blueprint, request, render_template, flash, redirect, send_from_directory, current_app)
from pathlib import Path
from werkzeug.utils import secure_filename

from .file_manager import get_file_manager
from .tfa import generate_otpauth_url, generate_secret_key, tfa_valid

_logger = logging.getLogger(__name__)

vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')

@vaulture_bp.route('/new_account', methods=['GET', 'POST'])
def vaulture_new_account():
    # get the file manager related to env
    filemanager = get_file_manager()
    TMP_FOLDER = Path('tmp_vaults')
    UPLOAD_FOLDER = Path(current_app.config["UPLOAD_FOLDER"])

    if request.method == 'POST':
        try:
            new_account_file = request.files.get('vault_file', False)
            new_account_otp_code = request.form.get('otp_code', False)

            # TODO : refactor this -> use Flask forms, correct fields, and also login decorators - not secured at all !!!
            if new_account_otp_code:
                # this is crap, used only for testing but an user could bypass this easily
                new_account_name = request.form['new_account_name']

                key_files = sorted((TMP_FOLDER / UPLOAD_FOLDER / Path(new_account_name)).glob('*.key'))

                if not any(key_files):
                    raise Exception("NoKey")
                
                otp_key = key_files[0].stem

                if not tfa_valid(otp_key, new_account_otp_code):
                    raise FileNotFoundError("NotValid")
                
                tmp_account_folder = TMP_FOLDER / UPLOAD_FOLDER / Path(new_account_name)

                tmp_account_folder.rename(UPLOAD_FOLDER / Path(new_account_name))

                return render_template('vaulture_new_account.html', success=True)
            else:
                new_account_filename = secure_filename(new_account_file.filename)
                new_account_name = new_account_filename.rsplit('.', 1)[0]
                new_account_otp_key = generate_secret_key()

                # get final path that will host required files
                folder_path = TMP_FOLDER / UPLOAD_FOLDER / Path(new_account_name)

                # create /tmp_vaults/UPLOAD_FOLDER/vault_filename
                filemanager.create_dir(folder_path)

                # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault
                filemanager.create(folder_path / Path(new_account_file.filename))

                # write content of file
                filemanager.write(folder_path / Path(new_account_file.filename), new_account_file.read())

                # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault.key
                filemanager.create(folder_path / Path(f'{new_account_otp_key}.key'))

                # generate OTP url to be scannable and display it on page
                otp_url = generate_otpauth_url(secret_key=new_account_otp_key, username=new_account_name)

                return render_template('vaulture_new_account.html', 
                                       otpurl=urllib.parse.quote(otp_url),
                                       new_account_name=new_account_name)
        except FileExistsError as fer:
            _logger.error(traceback.format_exc())
            return "Username already exists", 409
        except Exception as exc:
            _logger.error(traceback.format_exc())
            return "An error occurred", 400

    return render_template('vaulture_new_account.html')

@vaulture_bp.route('/file', methods=['GET', 'POST'])
def vaulture_fileget():
    # get the file manager related to env
    filemanager = get_file_manager()
    TMP_FOLDER = Path('tmp_vaults')
    UPLOAD_FOLDER = Path(current_app.config["UPLOAD_FOLDER"])

    if request.method == 'POST':
        try:
            account_name = request.form['filename']
            account_tfa = request.form['tfa_code']

            if not filemanager.exists(UPLOAD_FOLDER / Path(account_name).stem):
                raise FileNotFoundError("NotFound")
            
            key_files = sorted((UPLOAD_FOLDER / Path(account_name).stem).glob('*.key'))

            if not any(key_files):
                raise FileNotFoundError("NoKey")
            
            otp_key = key_files[0].stem

            if not tfa_valid(otp_key, account_tfa):
                raise FileNotFoundError("NotValid")

            return render_template('vaulture_fileget.html', 
                                   content=filemanager.read(UPLOAD_FOLDER / Path(account_name).stem / Path(account_name)).decode("utf-8"))
        except FileNotFoundError as fnfe:
            _logger.error(traceback.format_exc())
            return "Username does not exist", 400
        except Exception as exc:
            _logger.error(traceback.format_exc())
            return "An error occurred", 400

    return render_template('vaulture_fileget.html')

@vaulture_bp.route('/file/upload', methods=['GET', 'POST'])
def vaulture_fileupload():
    """
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
    """
    return NotImplementedError

@vaulture_bp.route('/file/create', methods=['GET', 'POST'])
def vaulture_filecreate():
    """
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
    """
    return NotImplementedError

@vaulture_bp.route('/file/list', methods=['GET'])
def vaulture_filelist():
    # get the file manager related to env
    filemanager = get_file_manager()
    TMP_FOLDER = Path('tmp_vaults')
    UPLOAD_FOLDER = Path(current_app.config["UPLOAD_FOLDER"])

    return render_template('vaulture_filelist.html',
                            content=filemanager.list(UPLOAD_FOLDER))
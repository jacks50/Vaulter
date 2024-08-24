import logging
import traceback
import urllib.parse

from flask import (Blueprint, request, jsonify)
from pathlib import Path

from .file_manager import get_file_manager
from .utils import valid_filename, generate_otpauth_url, generate_secret_key, tfa_valid

_logger = logging.getLogger(__name__)

vaulture_bp = Blueprint('vaulture', __name__, url_prefix='/vaulture')


@vaulture_bp.route('/new_account', methods=['POST'])
def vaulture_new_account():
    filemanager = get_file_manager()

    if request.method == 'POST':
        try:
            vault_file = request.files.get('vault_file', False)
            otp_code = request.form.get('otp_code', False)

            if vault_file:
                # First step : If a new file is received, we need to create paths accordingly
                #  and setup OTP keys

                # check validity of filename and retrieve account name from it
                vault_file_filename = valid_filename(vault_file)
                vault_account_name = vault_file_filename.rsplit('.', 1)[0]

                # generate OTP key
                vault_account_otp_key = generate_secret_key()

                # get final path that will host required files
                tmp_folder_path = filemanager.TMP_PATH / Path(vault_account_name)

                # if an account with this name already exists, raise
                if filemanager.exists(tmp_folder_path) or filemanager.exists(filemanager.UPLOAD_PATH / Path(vault_account_name)):
                    raise FileExistsError()

                # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault
                filemanager.create(tmp_folder_path / Path(vault_file_filename))

                # write content of file
                filemanager.write(tmp_folder_path / Path(vault_file_filename), vault_file.read())

                # create /tmp_vaults/UPLOAD_FOLDER/vault_filename/vault_filename.vault.key
                filemanager.create(tmp_folder_path / Path(f'{vault_account_otp_key}.key'))

                # generate OTP url to be scannable and display it on page
                otp_url = generate_otpauth_url(secret_key=vault_account_otp_key, username=vault_account_name)

                return jsonify({
                    'otp_url': urllib.parse.quote(otp_url),
                    'vault_account_name': vault_account_name,
                })                
            elif otp_code:
                # Second step : A code is received, so a path must be already created and we
                #  need to check now that the code is valid from the key generated
                vault_account_name = request.form['vault_account_name']
                account_name_path = Path(vault_account_name)

                # check that a .key file is present in directory of the account to be created
                key_files = sorted((filemanager.TMP_PATH / filemanager.UPLOAD_PATH / account_name_path).glob('*.key'))

                if not any(key_files):
                    _logger.error(f'No key found in folder for account {vault_account_name}')
                    raise Exception('KeyError')
                
                # get the stem of the file key found
                otp_key = key_files[0].stem

                if not tfa_valid(otp_key, otp_code):
                    _logger.error('Invalid OTP code provided')
                    raise Exception('KeyError')
                
                # get full path of account to be created and move it into folder of created accounts
                tmp_account_folder = filemanager.TMP_PATH / account_name_path

                filemanager.move(tmp_account_folder, filemanager.UPLOAD_PATH / account_name_path)
                
                return f'Your account "{vault_account_name}" has been succesfully created', 200
            else:
            # In this case, body is missing values -> Error
                raise Exception()
        except FileExistsError:
            _logger.error(traceback.format_exc())
            return 'Username already exists', 400
        except Exception:
            _logger.error(traceback.format_exc())
            return 'An error occurred', 400

    return 'Bad option', 400

@vaulture_bp.route('/login', methods=['POST'])
def vaulture_login():
    filemanager = get_file_manager()
    
    if request.method == 'POST':
        try:
            vault_account_name = request.form['vault_account_name']
            otp_code = request.form['otp_code']

            vault_account_path = Path(vault_account_name)

            if not filemanager.exists(filemanager.UPLOAD_PATH / vault_account_path):
                _logger.error(f'Trying to access non-existing account folder : {vault_account_name}')
                raise FileNotFoundError()
            
            key_files = sorted((filemanager.UPLOAD_PATH / vault_account_path).glob('*.key'))

            if not any(key_files):
                _logger.error(f'Account does not contain an OTP key : {vault_account_name}')
                raise FileNotFoundError()
            
            otp_key = key_files[0].stem

            if not tfa_valid(otp_key, otp_code):
                _logger.error(f'Invalid OTP code provided for account : {vault_account_name}')
                raise FileNotFoundError()
            
            vault_file_content = filemanager.read(
                filemanager.UPLOAD_PATH / vault_account_path / vault_account_path.with_suffix('.vault')
            ).decode('utf-8')
            
            return jsonify({
                'content': vault_file_content,
            })
        except FileNotFoundError:
            _logger.error(traceback.format_exc())
            return 'Username does not exist', 404
        except Exception:
            _logger.error(traceback.format_exc())
            return 'An error occurred', 400

    return 'Bad option', 400

@vaulture_bp.route('/update', methods=['POST'])
def vaulture_update():
    filemanager = get_file_manager()
    
    if request.method == 'POST':
        try:
            vault_account_name = request.form['vault_account_name']
            otp_code = request.form['otp_code']
            vault_file_content = request.form['vault_file_content']

            vault_account_path = Path(vault_account_name)

            if not filemanager.exists(filemanager.UPLOAD_PATH / vault_account_path):
                _logger.error(f'Trying to access non-existing account folder : {vault_account_name}')
                raise FileNotFoundError()
            
            key_files = sorted((filemanager.UPLOAD_PATH / vault_account_path).glob('*.key'))

            if not any(key_files):
                _logger.error(f'Account does not contain an OTP key : {vault_account_name}')
                raise FileNotFoundError()
            
            otp_key = key_files[0].stem

            if not tfa_valid(otp_key, otp_code):
                _logger.error(f'Invalid OTP code provided for account : {vault_account_name}')
                raise FileNotFoundError()
            
            vault_file_path = filemanager.UPLOAD_PATH / vault_account_path / vault_account_path.with_suffix('.vault')

            vault_file_path.write_bytes(vault_file_content)
            
            return 'Update done', 200
        except FileNotFoundError:
            _logger.error(traceback.format_exc())
            return 'Username does not exist', 404
        except Exception:
            _logger.error(traceback.format_exc())
            return 'An error occurred', 400

    return 'Bad option', 400

@vaulture_bp.route('/delete', methods=['POST'])
def vaulture_delete():
    raise NotImplementedError()

@vaulture_bp.route('/admin', methods=['GET'])
def vaulture_list():
    raise NotImplementedError()
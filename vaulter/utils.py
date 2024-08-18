import pyotp

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .constants import ALLOWED_EXTENSIONS


def valid_filename(file: FileStorage) -> str:
    secured_filename = secure_filename(file.filename)

    if not secured_filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        raise Exception('File not accepted')
    
    return secured_filename

def generate_secret_key() -> str:
    return pyotp.random_base32()


def generate_otpauth_url(secret_key: str, username: str) -> str:
    return pyotp.totp.TOTP(secret_key).provisioning_uri(name=username, issuer_name='Vaulter')


def tfa_valid(secret_key: str, code: str) -> bool:
    return pyotp.TOTP(secret_key).verify(code)

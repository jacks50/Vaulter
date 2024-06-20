import random
import os

from .constants import LEFT_SIDE_FILENAME, RIGHT_SIDE_FILENAME, ALLOWED_EXTENSIONS
from flask import current_app, flash
from werkzeug.utils import secure_filename


def file_is_allowed(file):
    # if file.size exceeds a certain amount -> raise
    return (file.filename
            and '.' in file.filename
            and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS)

def filename_exists(file):
    return False

def file_save(file):
    upload_folder = current_app.config['UPLOAD_FOLDER']

    filename = secure_filename(file.filename)

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    full_filepath = os.path.join(upload_folder, filename)

    if os.path.exists(full_filepath):
        raise FileExistsError

    file.save(full_filepath)

    return filename

def get_new_file_name():
    leftside_name = LEFT_SIDE_FILENAME[random.randrange(0, len(LEFT_SIDE_FILENAME-1))]
    rightside_name = RIGHT_SIDE_FILENAME[random.randrange(0, len(RIGHT_SIDE_FILENAME - 1))]
    random_number = random.randrange(0, 999)

    filename = f'{leftside_name}_{rightside_name}_{random_number}'

    if not filename_exists(filename):
        return get_new_file_name()

    return filename
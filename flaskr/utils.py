import random

from constants import LEFT_SIDE_FILENAME, RIGHT_SIDE_FILENAME

def filename_exists(filename):
    return False

def get_new_file_name():
    leftside_name = LEFT_SIDE_FILENAME[random.randrange(0, len(LEFT_SIDE_FILENAME-1))]
    rightside_name = RIGHT_SIDE_FILENAME[random.randrange(0, len(RIGHT_SIDE_FILENAME - 1))]
    random_number = random.randrange(0, 999)

    filename = f'{leftside_name}_{rightside_name}_{random_number}'

    if not filename_exists(filename):
        return get_new_file_name()

    return filename
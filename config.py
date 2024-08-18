import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'DO NOT USE IN PROD'
    CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

class ProductionConfig(Config):
    DEBUG = False
    STORAGE_URI = 'S3'
    UPLOAD_FOLDER = 'TODO_CHANGE_TO_S3_URL'
    TMP_FOLDER = 'TODO_CHANGE_TO_S3_TMP_URL'

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    STORAGE_URI = 'local'
    UPLOAD_FOLDER = 'vault_storage'
    TMP_FOLDER = 'tmp_vault_storage'

class TestingConfig(Config):
    TESTING = True
    STORAGE_URI = 'local'
    UPLOAD_FOLDER = 'vault_storage'
    TMP_FOLDER = 'tmp_vault_storage'

class DbConfig(Config):
    TESTING = True
    STORAGE_URI = 'DB'
    UPLOAD_FOLDER = 'vault_storage'
    TMP_FOLDER = 'tmp_vault_storage'
import abc
import boto3
import logging
import os
import traceback

import boto3.session
from botocore.exceptions import ClientError
from datetime import datetime
from flask import current_app, Flask
from pathlib import Path

from .constants import (
    DEFAULT_STORAGE_ACCESS_KEY_ID, 
    DEFAULT_STORAGE_BUCKET, 
    DEFAULT_STORAGE_REGION, 
    DEFAULT_STORAGE_SECRET_ACCESS_KEY
)

_logger = logging.getLogger(__name__)


def get_file_manager():
    with current_app.app_context():
        if current_app.config['STORAGE_URI'] == 'local':
            return InternalFileManager(current_app)
        elif current_app.config['STORAGE_URI'] == 'S3':
            return S3FileManager(current_app)
        elif current_app.config['STORAGE_URI'] == 'DB':
            return PostgresFileManager(current_app)
        else:
            raise ValueError

class FileManagerInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, 'exists') and callable(__subclass.exists) and
            hasattr(__subclass, 'create') and callable(__subclass.create) and
            hasattr(__subclass, 'write') and callable(__subclass.write) and
            hasattr(__subclass, 'delete') and callable(__subclass.delete) and
            hasattr(__subclass, 'read') and callable(__subclass.read) and
            hasattr(__subclass, 'move') and callable(__subclass.move) and
            hasattr(__subclass, 'list') and callable(__subclass.list) or
            NotImplemented
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManagerInterface, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, app: Flask) -> None:
        self.TMP_PATH = Path(app.config['TMP_FOLDER'])
        self.UPLOAD_PATH = Path(app.config['UPLOAD_FOLDER'])
    
    @abc.abstractmethod
    def exists(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def create(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def write(self, path: Path, content:bytes) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read(self, path: Path) -> bytes:
        raise NotImplementedError
    
    @abc.abstractmethod
    def move(self, path: Path, destination: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def list(self, path: Path) -> list:
        raise NotImplementedError


class InternalFileManager(FileManagerInterface):
    def __init__(self, app: Flask) -> None:
        super(InternalFileManager, self).__init__(app)

    def exists(self, path: Path) -> bool:
        return path.exists()
    
    def create(self, path: Path) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

        return True
    
    def write(self, path: Path, content:bytes) -> bool:
        path.write_bytes(content)

        return True
    
    def delete(self, path: Path) -> bool:
        if path.is_file():
            path.unlink(missing_ok=True)
        elif path.is_dir():
            path.rmdir()
        
        return True
    
    def read(self, path: Path) -> bytes:
        return path.read_bytes()
    
    def move(self, path: Path, destination: Path) -> bool:
        path.rename(destination)

        return True
    
    def list(self, path: Path) -> list:
        return [(f'{child.name} ({child.stat().st_size}B) '
                f'- Last edit : {datetime.fromtimestamp(child.stat().st_mtime)}')
                for child in path.iterdir()]


class PostgresFileManager(FileManagerInterface):
    def __init__(self, app: Flask) -> None:
        super(PostgresFileManager, self).__init__(app)

    def exists(self, path: Path) -> bool:
        raise NotImplementedError
    
    def create(self, path: Path) -> bool:
        raise NotImplementedError
    
    def write(self, path: Path, content:bytes) -> bool:
        raise NotImplementedError
    
    def delete(self, path: Path) -> bool:
        raise NotImplementedError
    
    def read(self, path: Path) -> bytes:
        raise NotImplementedError
    
    def move(self, path: Path, destination: Path) -> bool:
        raise NotImplementedError
    
    def list(self, path: Path) -> list:
        raise NotImplementedError


class S3FileManager(FileManagerInterface):
    def __init__(self, app: Flask) -> None:
        super(S3FileManager, self).__init__(app)

        try:
            s3_session = boto3.session.Session(
                aws_access_key_id=os.environ.get(DEFAULT_STORAGE_ACCESS_KEY_ID),
                aws_secret_access_key=os.environ.get(DEFAULT_STORAGE_SECRET_ACCESS_KEY),
                region_name=os.environ.get(DEFAULT_STORAGE_REGION),
            )

            self.s3_client = s3_session.resource('s3')
            self.s3_bucket = self.s3_client.Bucket(os.environ.get(DEFAULT_STORAGE_BUCKET))
        except ClientError:
            _logger.error(traceback.format_exc())

    def exists(self, path: Path) -> bool:
        try:
            return self.s3_bucket.Object(Key=path).load()
        except ClientError:
            _logger.error(traceback.format_exc())
            raise
    
    def create(self, path: Path) -> bool:
        return self.write(path, b'')
    
    def write(self, path: Path, content:bytes) -> bool:
        try:
            self.s3_bucket.put_object(Key=path, Body=content)

            return True
        except ClientError:
            _logger.error(traceback.format_exc())
            raise
    
    def delete(self, path: Path) -> bool:
        try:
            self.s3_bucket.Object(Key=path).delete()

            return True
        except ClientError:
            _logger.error(traceback.format_exc())
            raise
    
    def read(self, path: Path) -> bytes:
        try:
            return self.s3_bucket.Object(Key=path).get().get('Body', b'').read()
        except ClientError:
            _logger.error(traceback.format_exc())
            raise
    
    def move(self, path: Path, destination: Path) -> bool:
        try:
            return False
        except ClientError:
            _logger.error(traceback.format_exc())
            raise
    
    def list(self, path: Path) -> list:
        try:
            object_list = []

            for bucket_object in self.s3_bucket.objects.all():
                bucket_object_data = bucket_object.get()

                object_list.append(
                    f'{bucket_object.key} ({bucket_object_data.get("ContentLength")}B) '
                    f'- Last edit : {bucket_object_data.get("LastModified")}'
                )

            return object_list
        except ClientError:
            _logger.error(traceback.format_exc())
            raise

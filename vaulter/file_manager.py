import abc
import boto3
import logging
import traceback

from botocore.exceptions import ClientError
from datetime import datetime
from flask import current_app, Flask
from pathlib import Path

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
        return [f'{child.name} ({child.stat().st_size}B) - Last edit : {datetime.fromtimestamp(child.stat().st_mtime)}'
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
    def exists(self, path: Path) -> bool:
        raise NotImplementedError
    
    def create(self, path: Path) -> bool:
        raise NotImplementedError
    
    def create_dir(self, path: Path, recursive: bool=True) -> bool:
        raise NotImplementedError
    
    def write(self, path: Path, content:bytes) -> bool:
        raise NotImplementedError
    
    def delete(self, path: Path) -> bool:
        raise NotImplementedError
    
    def delete_dir(self, path: Path) -> bool:
        raise NotImplementedError
    
    def read(self, path: Path) -> bytes:
        raise NotImplementedError
    
    def list(self, path: Path) -> list:
        raise NotImplementedError

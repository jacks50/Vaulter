import abc
import os

from datetime import datetime
from flask import current_app
from pathlib import Path
from typing import Union


def get_file_manager():
    if current_app.config['STORAGE_URI'] == 'local':
        return InternalFileManager()
    elif current_app.config['STORAGE_URI'] == 'S3':
        return S3FileManager()
    elif current_app.config['STORAGE_URI'] == 'DB':
        return PostgresFileManager()
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
            hasattr(__subclass, 'list') and callable(__subclass.list) or
            NotImplemented
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManagerInterface, cls).__new__(cls)
        return cls.instance
    
    @abc.abstractmethod
    def exists(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def create(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def create_dir(self, path: Path, recursive: bool=True) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def write(self, path: Path, content:bytes) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_dir(self, path: Path) -> bool:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read(self, path: Path) -> bytes:
        raise NotImplementedError
    
    @abc.abstractmethod
    def list(self, path: Path) -> list:
        raise NotImplementedError


class InternalFileManager(FileManagerInterface):
    def __init__(self) -> None:
        # init folders here CORRECTLY
        Path('tmp_vaults').mkdir(exist_ok=True)
        Path('vault_storage').mkdir(exist_ok=True)

        super(InternalFileManager, self).__init__()

    def exists(self, path: Path) -> bool:
        return path.exists()
    
    def create(self, path: Path) -> bool:
        path.touch()

        return True
    
    def create_dir(self, path: Path, recursive: bool=True) -> bool:
        path.mkdir(parents=recursive)

        return True
    
    def write(self, path: Path, content:bytes) -> bool:
        path.write_bytes(content)

        return True
    
    def delete(self, path: Path) -> bool:
        path.unlink(missing_ok=True)
        
        return True
    
    def delete_dir(self, path: Path) -> bool:
        path.rmdir()

        return True
    
    def read(self, path: Path) -> bytes:
        return path.read_bytes()
    
    def list(self, path: Path) -> list:
        return [f'{child.name} ({child.stat().st_size}B) - Last edit : {datetime.fromtimestamp(child.stat().st_mtime)}'
                for child in path.iterdir()]


class PostgresFileManager(FileManagerInterface):
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

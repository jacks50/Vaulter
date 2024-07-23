import abc
import os

from flask import current_app
from pathlib import Path


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
            hasattr(__subclass, 'file_create') and callable(__subclass.file_create) and
            hasattr(__subclass, 'file_get') and callable(__subclass.file_get) and
            hasattr(__subclass, 'file_upload') and callable(__subclass.file_upload) and
            hasattr(__subclass, 'file_delete') and callable(__subclass.file_delete) and
            hasattr(__subclass, 'file_list') and callable(__subclass.file_list) or
            NotImplemented
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManagerInterface, cls).__new__(cls)
        return cls.instance

    @abc.abstractmethod
    def file_create(self, file_name, file_content, file_path):
        """
        Creates a file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_get(self, file_name, file_path):
        """
        Retrieves an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_update(self, file_name, file_content, file_path):
        """
        Updates an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_delete(self, file_name, file_content):
        """
        Deletes an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_list(self, file_path):
        """
        List files in the designed storage used
        :return:
        """
        raise NotImplementedError


class InternalFileManager(FileManagerInterface):

    def _check_dir_file_exists(self, file_name, file_path):
        file_dir = Path(file_path)

        if not (file_dir.exists() or file_dir.is_dir()):
            raise FileNotFoundError

        file_complete_path = file_dir / file_name

        if file_complete_path.exists() or not file_complete_path.is_file():
            raise FileExistsError

        return file_complete_path

    def file_create(self, file_name, file_content, file_path):
        file_complete_path = self._check_dir_file_exists(file_name, file_path)

        file_complete_path.touch()

        return file_complete_path

    def file_get(self, file_name, file_path):
        file_complete_path = self._check_dir_file_exists(file_name, file_path)

        return file_complete_path

    def file_update(self, file_name, file_content, file_path):
        file_complete_path = self._check_dir_file_exists(file_name, file_path)

        with file_complete_path.open(mode='w') as f:
            f.write(file_content)

        return file_complete_path

    def file_delete(self, file_name, file_path):
        file_complete_path = self._check_dir_file_exists(file_name, file_path)

        file_complete_path.unlink()

        return True

    def file_list(self, file_path):

        for file in Path(file_path).iterdir():

        pass


class PostgresFileManager(FileManagerInterface):

    def file_create(self, file_name, file_content, file_path):
        pass

    def file_get(self, file_name, file_path):
        pass

    def file_update(self, file_name, file_content, file_path):
        pass

    def file_delete(self, file_name, file_content):
        pass

    def file_list(self, file_path):
        pass


class S3FileManager(FileManagerInterface):

    def file_create(self, file_name, file_content, file_path):
        pass

    def file_get(self, file_name, file_path):
        pass

    def file_update(self, file_name, file_content, file_path):
        pass

    def file_delete(self, file_name, file_content):
        pass

    def file_list(self, file_path):
        pass

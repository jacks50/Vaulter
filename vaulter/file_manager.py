import abc

from flask import current_app


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
    def file_create(self):
        """
        Creates a file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_get(self):
        """
        Retrieves an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_update(self):
        """
        Updates an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_delete(self):
        """
        Deletes an existing file in the designed storage used
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def file_list(self):
        """
        List files in the designed storage used
        :return:
        """
        raise NotImplementedError


class InternalFileManager(FileManagerInterface):
    def file_create(self):
        pass

    def file_get(self):
        pass

    def file_update(self):
        pass

    def file_delete(self):
        pass

    def file_list(self):
        pass


class PostgresFileManager(FileManagerInterface):
    def file_create(self):
        pass

    def file_get(self):
        pass

    def file_update(self):
        pass

    def file_delete(self):
        pass

    def file_list(self):
        pass


class S3FileManager(FileManagerInterface):
    def file_create(self):
        pass

    def file_get(self):
        pass

    def file_update(self):
        pass

    def file_delete(self):
        pass

    def file_list(self):
        pass


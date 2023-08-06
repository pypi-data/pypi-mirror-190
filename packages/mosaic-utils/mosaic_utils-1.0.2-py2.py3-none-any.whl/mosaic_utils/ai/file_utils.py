# -*- coding: utf-8 -*-
import os
import tarfile
from zipfile import ZipFile
from uuid import uuid4
import zipfile

def make_tar(files, output_file):
    tar = tarfile.open(output_file, "w:gz")
    for file in files:
        tar.add(file, arcname=os.path.basename(file))
    tar.close()


def extract_tar(tar_file, output_dir):
    tar = tarfile.open(tar_file)
    tar.extractall(path=output_dir)
    tar.close()


def extract_zip(zip_file, output_dir):
    with ZipFile(zip_file, "r") as f:
        f.extractall(path=output_dir)


def pickle_dumps(obj, file_path):
    import cloudpickle
    out = open(file_path, "wb")
    cloudpickle.dump(obj, out)
    out.close()


def pickle_loads(file_path):
    import cloudpickle
    from os import path
    if path.exists(file_path):
        pickled_file = open(file_path, "rb")
        obj = cloudpickle.load(pickled_file)
        pickled_file.close()
        return obj



def create_model_tar(base_dir, tar_name=None, *files):
    if tar_name is None:
        tar_path = os.path.join(base_dir, "ml_model.tar.gz")
    else:
        tar_path = os.path.join(base_dir, f"{tar_name}.tar.gz")
    make_tar(files, tar_path)
    return tar_path


def uuid_generator():
    _uuid = uuid4()
    return str(_uuid)


def check_tar_zip(file_path, temp_dir, file_name, file_type):
    if file_type=='application/gzip':
        new_filename = file_name.split(".")[0]
        extract_tar(file_path, temp_dir+f"/{new_filename}/")
        return "tar", temp_dir+f"/{new_filename}/"
    if file_type in ['application/zip', 'application/x-zip', 'application/octet-stream', 'application/x-zip-compressed']:
        new_filename = file_name.split(".")[0]
        extract_zip(file_path, temp_dir+f"/{new_filename}/")
        return "zip", temp_dir+f"/{new_filename}/"
    return "file", file_name


def check_and_create_directory(path):
    """
    Checking if folder exist if folder is not exist then it will create the folders
    :param path
    :return:file_path
    """
    try:
        path_array = path.split("/")
        directory = "/"
        for split_path in path_array:
            directory = directory + split_path + "/"
            if not os.path.isdir(directory):
                os.mkdir(directory, 0o777)
        os.chmod(path, 0o777)
        return "Folder created successfully!"
    except Exception as ex:
        raise ex


def save_model_data(file_path, obj_file):
    """
    Save data at File path
    :param file_path - destination path
    :param obj_file - file path / file obj to be stored on destination path
    :return: file_name
    """
    try:
        if not obj_file:
            return False
        if type(obj_file) is str:
            # File path has been passed
            # Creating required directories & copy file at the required location
            check_and_create_directory(file_path)
            import shutil
            shutil.copy2(obj_file, file_path)
            file_name = obj_file.split(os.path.sep)[-1]
            return file_name
        else:
            # File object has been passed
            # Creating required directories & stroing file at the required location
            base_path = '/'.join(file_path.split('/')[:-1])
            check_and_create_directory(base_path)
            file = open(file_path, "wb")
            for _chunk in obj_file.stream(32 * 1024):
                file.write(_chunk)
            file.close()
            return file_path.split('/')[-1]
    except Exception as ex:
        raise ex


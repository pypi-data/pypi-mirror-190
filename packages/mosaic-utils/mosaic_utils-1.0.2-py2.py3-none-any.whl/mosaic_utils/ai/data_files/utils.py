# -*- coding: utf-8 -*-
import os
import io
import tempfile
import base64
import shutil
import math
from dateutil import tz
from datetime import datetime
from minio import Minio
from minio.error import ResponseError
import requests


def create_minio_client(minio_url, minio_access_key, minio_secret_key):
    return Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )


def parse_file_name(file_name, prefix):
    filename = file_name.split(prefix)[-1]
    return filename


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def format_datetime(date_obj):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = date_obj.replace(tzinfo=from_zone)
    # Convert time zone
    central = utc.astimezone(to_zone)
    return str(central.strftime("%b %d, %Y %H:%M"))


def fetch_dir_file_paths(path, exclude_file):
    list_of_paths = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            data_paths = os.path.join(root, file)
            data_paths = data_paths.split(path)[-1]
            print(data_paths)
            list_of_paths.append(data_paths)
    list_of_paths.remove(exclude_file.split(path)[-1])
    return list_of_paths


def fetch_data_files(
    minio_client, bucket, initial_object_key, folder_path, bucket_size_flag=False
):
    objects = minio_client.list_objects(
        bucket, prefix=f"{initial_object_key}/{folder_path}", recursive=True
    )
    file_list = list()
    total_files_size = 0
    for obj in objects:
        file_list.append(
            [
                {
                    "name": parse_file_name(obj.object_name, f"{initial_object_key}/"),
                    "size": convert_size(obj.size),
                    "last_modified": obj.last_modified,
                }
            ]
        )
        total_files_size += obj.size
    if bucket_size_flag:
        total_files_size = convert_size(total_files_size)
        return file_list, total_files_size
    return file_list


def delete_file(minio_client, bucket, initial_object_key, file_name):
    minio_client.remove_object(bucket, f"{initial_object_key}/{file_name}")
    return "File deleted successfully !"


def download_file(minio_client, bucket, initial_object_key, file_name):
    data = minio_client.get_object(bucket, f"{initial_object_key}/{file_name}")
    return data


def upload_file_data(minio_client, bucket, initial_object_key, upload_data):
    object_key = f"{initial_object_key}/{upload_data['file_path_to_upload_to']}"
    minio_client.fput_object(
        bucket, object_key, upload_data["file_path_to_upload_from"]
    )
    return "File uploaded successfully !"


def check_project_folder_exist(client, bucket, initial_object_key):
    """
    This function is used to check project exist or not on using minio.
    Create a dummy folder as well
    :param client:
    :param bucket
    :param initial_object_key
    :return:
    """
    import io

    try:
        client.get_object(bucket, initial_object_key)
    except Exception as e:
        if e.__class__.__name__ == "NoSuchKey":
            temp_file = initial_object_key + "temp"
            client.put_object(bucket, temp_file, io.BytesIO(b"hello"), 5)


def get_project_data_files_size(minio_client, bucket, initial_object_key, folder_path):
    objects = minio_client.list_objects(
        bucket, prefix=f"{initial_object_key}/{folder_path}", recursive=True
    )
    total_files_size = 0
    for obj in objects:
        total_files_size += obj.size
    return total_files_size


def convert_into_bytes(size_string):
    units = {"KB": 1024, "MB": 1024 * 1024, "GB": 1024 * 1024 * 1024}
    for unit in units:
        if unit in size_string:
            index = size_string.find(unit)
            size = size_string[:index].strip()
            unit = size_string[index:].strip()
            return float(size) * units[unit]


def get_project_resource_quota(project_id, minio_client, bucket, console_url, headers):
    """
    get project quota and consumed quota
    """
    total_consumed_quota = get_project_data_files_size(
        minio_client, bucket, f"{project_id}/{project_id}-Data", ""
    )
    project_details_url = f"{console_url}/secured/api/project/v1/resource/{project_id}"
    response = requests.get(project_details_url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        project_quota = response_json.get("resourceQuota")
        quota_in_bytes = convert_into_bytes(project_quota)
        return quota_in_bytes, total_consumed_quota
    raise Exception("Issue in fetching project resource quota")


def delete_files(minio_client, bucket, initial_object_key, file_names):
    """
    Delete multiple objects from minio bucket
    :param minio_client
    :param bucket
    :param initial_object_key
    :param file_names
    :return:
    """
    delete_file_names = []
    for file_name in file_names:
        delete_file_names.append(f"{initial_object_key}/{file_name}")

    for del_err in minio_client.remove_objects(bucket, delete_file_names):
        print("Deletion Error: {}".format(del_err))

    return "Files deleted successfully !"


def copy_file(minio_client, bucket, initial_object_key, old_filename, new_filename):
    """
    Copy file from one location to other
    :param minio_client
    :param bucket
    :param initial_object_key
    :param old_filename
    :param new_filename
    :return:
    """
    result = minio_client.copy_object(
        bucket,
        f"{initial_object_key}/{new_filename}",
        f"{bucket}/{initial_object_key}/{old_filename}",
    )

    return "Files copied successfully !"


def rename_file(minio_client, bucket, initial_object_key, old_filename, new_filename):
    """
    Renaming API is not present in minio API, We will renaming it by copying the
    file with new name and then delete the existing file.
    :param minio_client
    :param bucket
    :param initial_object_key
    :param old_filename
    :param new_filename
    :return:
    """
    copy_file(minio_client, bucket, initial_object_key, old_filename, new_filename)
    delete_file(minio_client, bucket, initial_object_key, old_filename)

    return "File renamed successfully !"


def create_folder(minio_client, bucket, initial_object_key, folder_name):
    """
    Creating a folder inside bucket
    :param minio_client
    :param bucket
    :param initial_object_key
    :param folder_name
    :return:
    """
    object_key = f"{initial_object_key}/{folder_name}/"

    value = ""
    value_as_bytes = value.encode("utf-8")
    value_as_a_stream = io.BytesIO(value_as_bytes)
    try:
        minio_client.put_object(
            bucket, object_key, value_as_a_stream, length=len(value_as_bytes)
        )
    except ResponseError as err:
        print(err)

    return "Folder created successfully !"


def upload_big_size_file_data(minio_client, bucket, initial_object_key, upload_data):
    """
    Creating a folder inside bucket
    :param minio_client
    :param bucket
    :param initial_object_key
    :param upload_data
    :return:
    """
    object_key = f"{initial_object_key}/{upload_data.filename}"
    size = os.fstat(upload_data.fileno()).st_size
    minio_client.put_object(bucket, object_key, upload_data, size)
    return "File uploaded successfully !"

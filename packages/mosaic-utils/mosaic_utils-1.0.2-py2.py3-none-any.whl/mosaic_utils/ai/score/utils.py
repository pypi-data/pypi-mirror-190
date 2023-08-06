import os
import minio

from .constants import Minio


def create_minio_client():
    url = os.environ[Minio.url]
    access_key = os.environ[Minio.access_key]
    secret_key = os.environ[Minio.secret_key]
    return minio.Minio(url, access_key=access_key, secret_key=secret_key, secure=False)
# -*- coding: utf-8 -*-
import base64
import requests
from urllib.parse import quote
import tempfile
import os
import shutil

from .constants import Notebook, MosaicVersionControl, Headers


def get_repo(project_id=None, email_address=None, mosaicid=None, username=None, repo_id=None):
    """
    Common function for getting enabled git repo for the project

    Args:
        :param project_id:
        :param email_address:
        :param mosaicid:
        :param username:
        :param repo_id:
    """
    try:
        from git import Repo
        nb_url = Notebook.url + \
                 (Notebook.get_repo_by_id_api+repo_id if repo_id else Notebook.git_access_api)
        headers = {
            'x-auth-email': email_address,
            'x-auth-userid': mosaicid,
            'x-auth-username': username,
            'x-project-id': project_id,
        }
        enabled_repo = requests.get(nb_url, headers=headers)
        if enabled_repo and enabled_repo.status_code == 200:
            repo_details = enabled_repo.json()
            repo_url = repo_details["repo_url"]
            url_parts = repo_url.split("//")
            repo_type = repo_details["repo_type"]
            # password = replace_special_chars_with_ascii(str(git_access_token))
            password = quote(repo_details["password"], safe='')

            remote_url = "{0}//{1}:{2}@{3}".format(
                url_parts[0],
                repo_details["username"],
                password,
                url_parts[1],
            )
            repository = {"url": remote_url,
                          "base_folder": repo_details["base_folder"],
                          "branch": repo_details["branch"],
                          "repo_url": repo_url,
                          "repo_type": repo_type,
                          }
        else:
            repository = None
    except Exception as ex:
        repository = None

    return repository


def validate_repo(remote_url, git_branch, file_path):
    """
    Common function for validating a git repo

    Args:
        :param remote_url:
        :param git_branch:
        :param file_path:
    """
    try:
        git_temp_dir = tempfile.mkdtemp()

        Repo.clone_from(remote_url, git_temp_dir)
        repo = Repo(git_temp_dir)

        branch_exist = True
        try:
            repo.git.checkout(git_branch)
        except Exception as ex:
            branch_exist = False

        path_exist = os.path.exists(os.path.join(git_temp_dir, file_path))
        shutil.rmtree(git_temp_dir)
        if branch_exist and path_exist:
            return "Success", True
        if branch_exist is False:
            return "Invalid branch name. Please provide a valid branch name.", False
        if path_exist is False:
            return "Invalid base path. Please provide a valid base path.", False

    except Exception as ex:
        return "Invalid details. Please provide the correct information.", False


def create_remote_url(data):
    """
    Creates git clone url in format http(s)://user:token@remoteurl/repo.git
    :param data:
    :return:
    """
    url_parts = data['repo_url'].split("//")
    password = quote(data["password"], safe='')
    remote_url = "{0}//{1}:{2}@{3}".format(
        url_parts[0],
        data["username"],
        password,
        url_parts[1],
    )
    return remote_url


def encode_b64(input_str):
    """
    Method encodes a string to base64 encoding
    :param input_str:
    :return:
    """
    return base64.b64encode(input_str.encode("UTF-8")).decode("UTF-8") if input_str else ""


def decode_b64(input_str):
    """
    Method decodes the base64 encoding
    :param input_str:
    :return:
    """
    return base64.b64decode(input_str.encode("UTF-8")).decode("UTF-8") if input_str else ""


def encode_password(repo_object, skip_access_cat=None):
    """
    Encode a password field from repo object to base64
    :param repo_object: The repository Object,
    :param skip_access_cat: skip Encoding for given access category
    :return:
    """
    return _encode_decode_password(repo_object, skip_access_cat, is_encode=True)


def decode_password(repo_object, skip_access_cat=None):
    """
    Decode a password field from repo object from base64 to plain text
    :param repo_object: The repository Object
    :param skip_access_cat: skip decoding for given access category
    :return:
    """
    return _encode_decode_password(repo_object, skip_access_cat, is_encode=False)


def _encode_decode_password(repo_object, skip_access_cat, is_encode=False):
    """
    Common function for encode and decode
    :param repo_object:
    :param skip_access_cat:skip encode/decode for given access category
    :param is_encode:
    :return:
    """
    skip_access_cat = skip_access_cat.upper() if skip_access_cat else skip_access_cat
    if repo_object and repo_object.get("access_category", "PUBLIC").upper() != skip_access_cat:
        secure_flag = str(repo_object.get("secure_flag", "true")).lower() == "true"
        if not secure_flag:
            passwd = repo_object.get("password", "")
            repo_object["password"] = encode_b64(passwd) if is_encode else decode_b64(passwd)
    return repo_object
  
    
def state_of_code(project_id, version_id, repo_id="", branch="", headers=None):
    """Method to maintain state of code"""
    url = MosaicVersionControl.url + MosaicVersionControl.git_tag.format(
        repo=project_id, version_id=version_id, repo_id=repo_id, branch=branch)
    if not headers:
    	headers = get_headers()
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response


def get_headers():
    """
    Create headers
    :return:
    """
    return {
        Headers.x_userid: os.getenv("userId"),
        Headers.x_project_id: os.getenv("PROJECT_ID"),
        Headers.x_username: os.getenv("userId"),
        Headers.x_email_id: os.getenv("userId")
    }

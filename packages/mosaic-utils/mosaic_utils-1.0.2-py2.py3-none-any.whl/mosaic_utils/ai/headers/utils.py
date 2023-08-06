from .constants import *
import requests
from flask import Response


def generate_headers(userid=None, email=None, username=None, project_id=None, x_request_id=None, access_control=None):
    """
    Common function for generating headers based on given parameters

    Args:
        :param access_control:
        :param x_request_id:
        :param project_id:
        :param username:
        :param email:
        :param userid:
    """
    # assigning headers for api
    final_headers = {
        Headers.x_auth_userid: userid,
        Headers.x_auth_email: email,
        Headers.x_auth_username: username,
        Headers.x_project_id: project_id,
        Headers.x_request_id: x_request_id,
        Headers.access_control_allow_origin: access_control,
        Headers.access_control_allow_methods: access_control,
        Headers.access_control_allow_headers: access_control
    }
    return final_headers


def check_project_access(console_url, userid, email, username, project_id, access=None):
    """
      Common function for checking project access

      Args:
          :param console_url:
          :param project_id:
          :param username:
          :param email:
          :param userid:
          :param access
      """
    headers = generate_headers(userid, email, username, project_id)
    project_access_url = f"{console_url}/secured/api/project/v1/access"
    response = requests.get(project_access_url, headers=headers)
    if response.status_code == 404 or response.status_code == 401:
        # raise exception
        return Response("Access denied", status=403)
    if response.status_code == 500:
        raise ValueError("Access denied")
    if response.status_code == 200 and access and response.json()["accessType"] not in ["OWNER", "CONTRIBUTOR", "VALIDATOR"]:
        raise ValueError("Access denied")

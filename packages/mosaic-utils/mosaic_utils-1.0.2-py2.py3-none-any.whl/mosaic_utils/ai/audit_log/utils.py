from .constants import *
import requests


def audit_logging(console_url, action_type, object_id, object_name, object_type, headers, message=None, object_json=None):
    """
    Calls Audit Logging API of console backend

    Args:
        object_json (json): json response received from API
        headers (dict): headers to be passed to API
        object_type (string): MODEL or NOTEBOOK ( type of object )
        object_name (string): name of model or notebook
        object_id (string): id of model or notebook
        action_type (string): CREATE,UPDATE,DELETE,DEPLOY
        console_url (string): url of console backend API
        message (string) : custom message for API
    Returns:
        dict
    """
    # assigning headers for api
    headers = {
        Headers.x_auth_userid: headers["X-Auth-Userid"],
        Headers.x_auth_email: headers["X-Auth-Email"],
        Headers.x_auth_username: headers["X-Auth-Username"],
        Headers.x_project_id: headers["X-Project-Id"],
    }
    # json payload for audit logging
    payload = {
        "actionType": action_type,
        "objectId": object_id,
        "objectName": object_name,
        "objectType": object_type,
        "objectJson": object_json,
        "projectId": headers["X-Project-Id"],
        "message": message
    }
    # creating the api url
    audit_log_url = f"{console_url}/secured/api/activity/v1"
    # hitting the api
    response = requests.post(audit_log_url, headers=headers, json=payload)
    # printing response to check errors
    print(response.text)

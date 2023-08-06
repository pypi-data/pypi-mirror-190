# -*- coding: utf-8 -*-
from uuid import uuid4
import requests
from .constants import *


def uuid_generator():
    """
    Method to generate uuid
    :return: uuid
    :rtype: str
    """
    _uuid = uuid4()
    return str(_uuid)



def notification_alert(notification_type, message_status, notification_url, headers):

    """
    Calls lens-manage-console api for storing and triggering notifications

    Args:
            notification_type (string): Notebooks/AutoML/Model/Schedule
            headers (dict): headers to be passed to API
            message_status (string): Description of the notification
            notification_url (string): redirect url

    Returns:
            response after hitting the api
    """


    notification_payload = {
        "user_id": headers["X-Auth-Username"],
        "status": "Success",
        "uuid": uuid_generator(),
        "notificationURL": notification_url,
        "notificationDescription": message_status,
        "notificationType": notification_type,  # the real deal
        "createdBy": headers["X-Auth-Username"],
        "notificationDetails": {
            "senderName": headers["X-Auth-Username"],
            "accessType": "FullAccess"
        }
    }

    final_headers = {
        "X-Auth-Username": headers["X-Auth-Username"],
        "X-Project-Id": headers["X-Project-Id"],
        "X-Auth-Userid": headers["X-Auth-Userid"],
        "X-Auth-Email": headers["X-Auth-Email"]
    }

    response = requests.post(Url.lens_manage_console_url, json=notification_payload, headers=final_headers)
    return response

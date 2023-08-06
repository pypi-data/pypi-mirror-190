# -*- coding: utf-8 -*-
import requests
from flask import jsonify
from .contants import InputParamPath, InputParamReferenceType


def get_all_input_params(env, headers, url, reference_id, reference_type):
    """
    Get all level input params
    reference type: MODEL, PROJECT, USER, NOTEBOOK
    """
    try:
        param_url = url + InputParamPath.input_params_path.format(
            reference_id=reference_id, inputReferenceType=reference_type
        )
        response = requests.get(param_url, headers=headers)

        if reference_type == InputParamReferenceType.ref_type_model:
            if response.status_code == 200:
                list_of_params = response.json()
                if list_of_params:
                    for param in list_of_params:
                        if param["inputParameterType"] != "SYSTEM":
                            env[str(param["inputParameterName"])] = str(
                                param["parameterValue"]
                            )
            return env
        else:
            return create_param_dict(env, response)

    except Exception:
        return []


@DeprecationWarning
def get_project_params(env, headers, url, project_id):
    """
    Get project level input params
    """
    try:
        param_url = url + InputParamPath.project.format(project_id=project_id)
        response = requests.get(param_url, headers=headers)
        return create_param_dict(env, response)
    except Exception:
        raise


@DeprecationWarning
def get_notebook_params(env, headers, url, notebook_id):
    """
    Get notebook level input params
    """
    try:
        param_url = url + InputParamPath.notebook.format(notebook_id=notebook_id)
        response = requests.get(param_url, headers=headers)
        return create_param_dict(env, response)
    except Exception:
        raise


@DeprecationWarning
def get_user_params(env, headers, url):
    """
    Get user level input params
    """
    try:
        param_url = url + InputParamPath.user
        response = requests.get(param_url, headers=headers)
        return create_param_dict(env, response)
    except Exception:
        raise


@DeprecationWarning
def get_model_params(env, headers, url, version_id):
    """
    Get model level input params
    """
    try:
        param_url = url + InputParamPath.model.format(version_id=version_id)
        response = requests.get(param_url, headers=headers)
        if response.status_code == 200:
            list_of_params = response.json()
            if list_of_params:
                for param in list_of_params:
                    if param["inputParameterType"] != "SYSTEM":
                        env[str(param["inputParameterName"])] = str(
                            param["parameterValue"]
                        )
        return env
    except Exception:
        raise


def create_param_dict(env, response):
    if response.status_code == 200:
        list_of_params = response.json()
        if list_of_params:
            for param in list_of_params:
                key_val = {
                    remove_special_char(param["inputParameterName"]): param[
                        "parameterValue"
                    ]
                }
                env.update(key_val)
    return env


def remove_special_char(var):
    """
    Method to remove spaces & special characters apart from '-' & "_" from var,
    returns only alphanumeric values
    :param var: variable name
    """
    return "".join(e for e in var if e == "-" or e == "_" or e.isalnum())

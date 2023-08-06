# -*- coding: utf-8 -*-
import os

import numpy as np
import pandas as pd

from .constants import Client, Headers, MLModelType
from ..build_time_metrics import metrics

from IPython.display import clear_output


def read_jwt():
    config_file = os.path.expanduser(Client.config_file)
    if os.path.exists(config_file):
        with open(config_file) as f:
            jwt = f.read().strip("\n")
        return jwt
    elif os.getenv("TOKEN"):
        jwt = os.getenv("TOKEN")
        return jwt
    else:
        print("Warning - JWT Token not set")


def get_headers():
    jwt = read_jwt()
    return {
        Headers.authorization: f"Token {jwt}",
        Headers.x_project_id: os.environ.get("PROJECT_ID"),
    }


def try_or(fn):
    try:
        out = fn()
        return out
    except:
        return None


def get_model_type_handler(model_type):
    if model_type == MLModelType.classification:
        return metrics.Classification
    if model_type == MLModelType.regression:
        return metrics.Regression


def get_array_type_handler(y_true, y_pred):
    if isinstance(y_true, list) and isinstance(y_pred, list):
        return "list"
    if isinstance(y_true, np.ndarray) and isinstance(y_pred, np.ndarray):
        return "ndarray"
    if isinstance(y_true, pd.core.series.Series) and isinstance(
        y_pred, pd.core.series.Series
    ):
        return "series"
    if isinstance(y_true, pd.core.frame.DataFrame) and isinstance(
        y_pred, pd.core.frame.DataFrame
    ):
        return "df"


def get_pred_and_true_values(y_true, y_pred):
    if len(y_true.columns) == 1 and len(y_pred.columns) == 1:
        return y_true.values, y_pred.values


def update_progress(progress):
    bar_length = 70
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1
    block = int(round(bar_length * progress))
    clear_output(wait=True)
    print("Calculating build time metrics\n")
    text = "Progress: {0} {1:.1f}%".format(
        "█" * block + " " * (bar_length - block), progress * 100
    )
    print(text)

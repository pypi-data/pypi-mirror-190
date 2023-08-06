# -*- coding: utf-8 -*-
import json
from .utils import NumpyArrayEncoder


def load_model(model_path):
    import cloudpickle

    return cloudpickle.load(open(model_path, "rb"))


def dump_model(model, path):
    import cloudpickle

    cloudpickle.dump(model, open(path, "wb"))


def get_model_structure(model_obj):
    ml_model_class = model_obj.__dict__
    ml_model_class["class"] = str(model_obj.__class__)[8:-2:]
    return json.dumps(ml_model_class, cls=NumpyArrayEncoder)

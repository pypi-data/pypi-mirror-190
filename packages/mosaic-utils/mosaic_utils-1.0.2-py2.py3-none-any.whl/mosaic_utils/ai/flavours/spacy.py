# -*- coding: utf-8 -*-
import json
from .utils import NumpyArrayEncoder


def load_model(model_path):
    import spacy

    return spacy.load(model_path)


def dump_model(model, path):
    model.to_disk(path)


def get_model_structure(model_obj):
    ml_model_class = model_obj.__dict__
    ml_model_class["class"] = str(model_obj.__class__)[8:-2:]
    return json.dumps(ml_model_class, cls=NumpyArrayEncoder)

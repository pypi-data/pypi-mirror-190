# -*- coding: utf-8 -*-


def load_model(model_path):
    from pypmml import Model

    model = Model.load(model_path)
    return model

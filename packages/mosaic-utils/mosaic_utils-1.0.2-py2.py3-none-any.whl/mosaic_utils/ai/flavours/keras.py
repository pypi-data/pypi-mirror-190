# -*- coding: utf-8 -*-
import json


def load_model(model_path):
    # WARNING:tensorflow Support For V1 is deprecated and will be removed in a future version.
    import tensorflow as tf
    if tf.__version__[:1] == "2":
        #WARNING:tensorflow Support For V1 is deprecated and will be removed in a future version.
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()
        from tensorflow.compat.v1 import keras
        
    else:
        from tensorflow import keras

    return keras.models.load_model(model_path)


def dump_model(model, path):
    model.save(path)


def get_model_structure(model_obj):
    ml_model_class = json.loads(model_obj.to_json())
    ml_model_class["class"] = str(model_obj.__class__)[8:-2:]
    return json.dumps(ml_model_class)

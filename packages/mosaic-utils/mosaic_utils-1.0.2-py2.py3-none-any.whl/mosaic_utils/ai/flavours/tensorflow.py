# -*- coding: utf-8 -*-
import json


def load_model(frozen_graph_path):
    """
    Load the model from frozen inference graph.

    Args:
        frozen_graph_path   :   path to frozen graph (.pb)

    Return:
        frozen graph that can be used directly for inference
    """
    import tensorflow as tf
    if tf.__version__[:1] == "2":
        detection_graph = tf.keras.models.load_model(frozen_graph_path)
    else:
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(frozen_graph_path, "rb") as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name="")

    return detection_graph


def dump_model(frozen_graph, path):
    """
    Save Tensorflow Frozen Inference Graph.

    Args:
        frozen_graph    :   tensorflow frozed inference graph
        path            :   path to save the frozen inference graph (.pb)
    """
    import tensorflow as tf
    if tf.__version__[:1] == "2":
        tf.keras.models.save_model(frozen_graph, path)
    else:
        with tf.gfile.GFile(path, "wb") as f:
            f.write(frozen_graph.as_graph_def().SerializeToString())


def get_model_structure(model_obj):
    ml_model_class = {"class": str(model_obj.__class__)[8:-2:]}
    return json.dumps(ml_model_class)

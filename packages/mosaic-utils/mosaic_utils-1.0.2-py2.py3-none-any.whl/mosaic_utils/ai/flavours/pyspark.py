# -*- coding: utf-8 -*-

"""Handler for PySpark Model Flavor."""

import os
import json
from .utils import NumpyArrayEncoder

# from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName(__name__).getOrCreate()


class ClassCreator(object):
    """Create class instance from its string representation."""

    @classmethod
    def get_class(cls, class_name):
        """
        Get an instance of class from class_name.

        :param class_name:
        :return:
        """
        parts = class_name.split(".")
        module = ".".join(parts[:-1])
        import_module = __import__(module)
        for comp in parts[1:]:
            import_module = getattr(import_module, comp)
        return import_module


def get_model_type(model_path):
    """Get type of pyspark model."""
    metadata_path = os.path.join(model_path, "metadata")
    metadata_files = os.listdir(metadata_path)
    metadata_file = [x for x in metadata_files if x.startswith("part-000")]
    if not metadata_file:
        raise FileNotFoundError("Model metadata file not found")
    metadata_file = metadata_file[0]
    with open(os.path.join(metadata_path, metadata_file), "r") as f_handle:
        model_metadata = f_handle.read()
    model_metadata = json.loads(model_metadata)
    model_class = model_metadata.get("class")
    if not model_class:
        raise AttributeError('Attribute "class" not found in model metadata')
    model_class = model_class.replace("org.apache.spark", "pyspark")
    return model_class


def load_model(model_path):
    """Load model from disk."""
    model_type = get_model_type(model_path)
    model_handler = ClassCreator.get_class(model_type)
    model_instance = model_handler.load(model_path)
    return model_instance


def dump_model(model, path):
    """Save the model to disk."""
    model.save(path)
    import time
    time.sleep(2)


def get_model_structure(model_obj):
    ml_model_class = model_obj.__dict__
    ml_model_class["class"] = str(model_obj.__class__)[8:-2:]
    return json.dumps(ml_model_class, cls=NumpyArrayEncoder)

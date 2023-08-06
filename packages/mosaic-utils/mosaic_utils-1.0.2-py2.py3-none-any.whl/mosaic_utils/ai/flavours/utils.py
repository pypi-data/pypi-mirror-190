# -*- coding: utf-8 -*-
from json import JSONEncoder
import numpy as np


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, np.ndarray) and obj.size >= 10:
            return None
        if isinstance(obj, np.ndarray) and obj.size <= 10:
            return obj.tolist()
        else:
            return str(obj)

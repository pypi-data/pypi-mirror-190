'''
POC: Testing Scenarios Not To Be Considered For Production
'''

import requests
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.DEBUG)
from abc import ABC, abstractmethod
from typing import Tuple, Union, List, Iterable, Any
from .constants import ScoreLabel
from .constants import ValidationBoxLabel as VBLabel
from .validators import RequestValidatorMixin, PayloadSchemaValidatorMixin

from .response import ScoreResponse
from .encoder import ScoreResponseEncoder
from collections import OrderedDict
from IPython.display import display

try:
    pd.set_option('display.max_colwidth', -1)
except Exception:
    pd.set_option('display.max_colwidth', None)


class ScoreBase(RequestValidatorMixin,
                PayloadSchemaValidatorMixin,
                ABC):
    each_request_processed_schema: OrderedDict = NotImplementedError
    each_pre_processed_schema: OrderedDict = NotImplementedError

    def __init__(self):
        self.meta = self.Meta()
        self.score_request = None
        self.score_response_collection = []
        self.n_input = None
        self.all_request_processed_payload = None
        self.all_clean_payload = None

        self.validation_box = pd.DataFrame(
            {
                "VALIDATION": pd.Series(VBLabel.VALIDATION,
                                        dtype=str),
                "COMPONENT": pd.Series(VBLabel.COMPONENT,
                                       dtype=str),
                "PASSED": pd.Series(VBLabel.PASSED,
                                    dtype=bool),
                "SKIPPED": pd.Series(VBLabel.SKIPPED,
                                     dtype=bool),
            }
        )

    @abstractmethod
    def request_processing_fn(self,
                              request,
                              *args,
                              **kwargs) -> Tuple[int, Union[List[np.ndarray], List[Any]]]:
        """
        Segregates Payload From Request Object
        Request Object -> (N,  List[Input data, ..])

        Input data could be:
            - List[ [Feature_Value1, .., Feature_ValueN], [...] ]
            - List[numpy.array(), numpy.array(), ...]
            - List[tf.Tensor, tf.Tensor, tf.Tensor, ...]
            - List[ SingleSample, SingleSample]

        A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
        A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
        A dict mapping input names to the corresponding array/tensors, if the model has named inputs.

        :return: (n_inputs, payload's)

        Warnings:

        1. Do not reshape your final output for single sample here(array.reshape(1, -1)), do it in prediction_fn.
           Else payloads will be invalidated for extraction at raw and extraction level.
        """
        pass

    @abstractmethod
    def pre_processing_fn(self,
                          each_payload: Union[np.ndarray, Any]) -> Union[np.ndarray, Any]:
        """
        Accepts Single Payload At a time and applies pre_processing_step before prediction

        :param each_payload: Single Payload
        :return: Preprocessed Payload
        """
        pass

    @abstractmethod
    def prediction_fn(self,
                      model: Any,
                      pre_processed_input: Union[np.ndarray, Any]
                      ):
        """
        Does the main prediction on pre_processed_input using supplied model.

        :param model: Supported Model
        :param pre_processed_input: Single Preprocessed Payload
        :return: Prediction Value From the model

        Recommended Notes:
        - Numpy:
            - Reshape your data array.reshape(1, -1) here before predictions as it contains a single sample.
        """
        pass

    def score(self,
              model,
              input_request,
              dry_run=False):
        self.reset()

        if self.can_run_pre_call_hooks():
            for each_hooks in self.meta.pre_call_hooks:
                each_hooks()

        _request_processed_fn_op = self.request_processing_fn(input_request)
        self.validate_request(_request_processed_fn_op)

        if dry_run:
            display(self.validation_box[:3])
            print(ScoreLabel.Note, "\n")

        if not self.validation_box["PASSED"].all():
            return {"error": "Validation Failed. Please run with dry_run=True to see all exceptions."}

        self.n_input, self.all_request_processed_payload = _request_processed_fn_op

        for each_request in self.get_processed_request_payload():
            _rp_payload_validated = False
            _clean_payload_validated = False

            if self.validate_with_schema_payload(self.each_request_processed_schema,
                                                 each_request):
                _rp_payload_validated = True

            _clean_payload = self.pre_processing_fn(each_request)
            if self.validate_with_schema_payload(self.each_pre_processed_schema,
                                                 _clean_payload):
                _clean_payload_validated = True

            _score_response = self.prediction_fn(model, _clean_payload)

            _response = ScoreResponse(score_request=input_request.json,
                                      request_processed_payload=each_request,
                                      rp_payload_validated=_rp_payload_validated,
                                      clean_payload=_clean_payload,
                                      clean_payload_validated=_clean_payload_validated,
                                      score_response=_score_response)

            self.score_response_collection.append(_response)

        if self.can_run_post_call_hooks():
            for each_hooks in self.meta.post_call_hooks:
                each_hooks()

        return self.score_response_collection

    def reset(self):
        self.score_request = None
        self.score_response_collection = []
        self.n_input = None
        self.all_request_processed_payload = None
        self.all_clean_payload = None

    def get_processed_request_payload(self) -> Iterable:
        """

        :return:  Iterables of Inputs
        """
        if isinstance(self.all_request_processed_payload, list):
            return iter(self.all_request_processed_payload)
        else:
            return iter([self.all_request_processed_payload])

    def get_clean_payload(self) -> Iterable:
        """

        :return:  Iterables of Inputs
        """

        if isinstance(self.all_clean_payload, list):
            return iter(self.all_clean_payload)
        else:
            return iter([self.all_clean_payload])

    def can_run_pre_call_hooks(self):
        """
        :return: True if this score has a `pre_call_hooks` attributes defined for with list of Callables,
        False otherwise.
        """
        return hasattr(self.__class__.Meta, "pre_call_hooks")

    def can_run_post_call_hooks(self):
        """
        :return: True if this score has a `post_call_hooks` attributes defined for with list of Callables,
        False otherwise.
        """
        return hasattr(self.__class__.Meta, "post_call_hooks")

    @staticmethod
    def download_template():
        from os.path import abspath, join, dirname
        get_cwd = dirname(abspath(__file__))
        with open(join(get_cwd, "templates.py"), 'r') as template_example:
            content = template_example.readlines()
            content = list(map(lambda each_line: each_line.strip("\n"), content))
            for lines in content:
                print(lines)

    class Meta:
        pass

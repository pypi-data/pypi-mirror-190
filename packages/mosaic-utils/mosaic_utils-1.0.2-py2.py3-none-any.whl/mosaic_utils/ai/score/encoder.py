import json
import copy
from json import JSONEncoder, JSONDecoder
from datetime import datetime
from numpy import ndarray
from .response import ScoreResponse
from .constants import ScoreResponseLabel as ScoreRLBL


class ScoreResponseDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        _uuid = dct["_uuid"]
        _timestamp = datetime.strptime(dct["timestamp"],
                                       ScoreRLBL.TIMESTAMP_FORMAT)
        _request_processed_payload = dct["request_processed_payload"]
        _rp_payload_validated = dct["rp_payload_validated"]
        _clean_payload = dct["clean_payload"]
        _clean_payload_validated = dct["clean_payload_validated"]
        _score_response = dct["score_response"]
        _score_request = dct["score_request"]

        return ScoreResponse(uuid=_uuid,
                             timestamp=_timestamp,
                             score_request=_score_request,
                             request_processed_payload=_request_processed_payload,
                             rp_payload_validated=_rp_payload_validated,
                             clean_payload=_clean_payload,
                             clean_payload_validated=_clean_payload_validated,
                             score_response=_score_response)


class ScoreResponseEncoder(JSONEncoder):
    def default(self, o):
        self._object = copy.deepcopy(o.__dict__)

        self._object["timestamp"] = self.encode_timestamp()
        self._object["request_processed_payload"] = self.encode_request_processed_payload()
        self._object["rp_payload_validated"] = self.encode_rp_payload_validated()
        self._object["clean_payload"] = self.encode_clean_payload()
        self._object["clean_payload_validated"] = self.encode_clean_payload_validated()
        self._object["score_request"] = self.encode_score_request()

        return self._object

    def encode_clean_payload_validated(self):
        return bool(self._object["clean_payload_validated"])

    def encode_rp_payload_validated(self):
        return bool(self._object["rp_payload_validated"])

    def encode_timestamp(self):
        return self.check_value_dtype(self._object["timestamp"])

    def encode_request_processed_payload(self):
        return self.check_value_dtype(self._object["request_processed_payload"])

    def encode_clean_payload(self):
        return self.check_value_dtype(self._object["clean_payload"])

    def encode_score_request(self):
        return self.check_value_dtype(self._object["score_request"])

    def check_value_dtype(self, value):
        if isinstance(value, datetime):
            return value.strftime(ScoreRLBL.TIMESTAMP_FORMAT)
        elif isinstance(value, ndarray):
            return value.tolist()
        elif hasattr(value, 'tolist'):
            # Either Torch Tensor
            return value.tolist()
        elif hasattr(value, 'numpy') and callable(value.numpy):
            # Either Tensorflow Tensor
            return value.numpy().tolist()
        elif isinstance(value, (list, str)):
            return value
        return []


import datetime
from uuid import uuid4
from .constants import ScoreResponseCollectionLabel as SCRLabel


class ScoreResponse(object):
    purpose = "<<ScoreResponse>>"
    fields = SCRLabel.SCORE_RESPONSE_FIELDS

    def __repr__(self):
        return self.purpose

    def __init__(self,
                 uuid=str(uuid4()),
                 timestamp=datetime.datetime.now(),
                 score_request=None,
                 request_processed_payload=None,
                 rp_payload_validated=False,
                 clean_payload=None,
                 clean_payload_validated=False,
                 score_response=None,
                 ):

        self._uuid = uuid
        self.timestamp = timestamp
        self.score_request = score_request
        self.request_processed_payload = request_processed_payload
        self.rp_payload_validated = rp_payload_validated
        self.clean_payload = clean_payload
        self.clean_payload_validated = clean_payload_validated
        self.score_response = score_response

    @property
    def uuid(self) -> str:
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str) -> None:
        if not isinstance(uuid, str):
            raise ValueError("UUID Field Must Be String")
        self._uuid = uuid

    def to_dict(self):
        tmp_ = dict.fromkeys(self.fields)
        for k, v in tmp_.items():
            tmp_[k] = getattr(self, k)
        return tmp_

import datetime
import json
import pandas as pd
from uuid import uuid4
from collections.abc import Iterable, Iterator
from typing import Union, List
from .response import ScoreResponse
from .constants import ScoreResponseCollectionLabel as SCRLabel
from .constants import ScoreResponseLabel as SCLabel
from .mixins import TimeTravelLoaderMixin
from IPython.display import display


class OrderIterator(Iterator):
    """
    Concrete Iterators implement various traversal algorithms. These classes
    store the current traversal position at all times.
    """

    """
    `_position` attribute stores the current traversal position. An iterator may
    have a lot of other fields for storing iteration state, especially when it
    is supposed to work with a particular kind of collection.
    """
    purpose = "<<OrderIterator>>"
    _position: int = None

    def __repr__(self):
        return self.purpose

    """
    This attribute indicates the traversal direction.
    """
    _reverse: bool = False

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class ScoreResponseCollection(TimeTravelLoaderMixin,
                              Iterable):
    """
    Concrete Collections provide one or several methods for retrieving fresh
    iterator instances, compatible with the collection class.
    """
    purpose = "<<ScoreResponseCollection>>"

    def __repr__(self):
        return self.purpose

    def __init__(self,
                 collection: List[ScoreResponse] = [],
                 mode="order",
                 tabulate=True,
                 tabulate_serialize=False,
                 score_cls=None,
                 *args,
                 **kwargs
                 ) -> None:
        super(ScoreResponseCollection, self).__init__(*args, **kwargs)

        self.tabulate = tabulate
        self.tabulate_serialize = tabulate_serialize
        self.score_cls = score_cls

        if tabulate:
            self.tabulate_frame = pd.DataFrame(columns=SCRLabel.SCORE_RESPONSE_FIELDS,
                                               )
            self.tabulate_frame["timestamp"] = pd.to_datetime(self.tabulate_frame["timestamp"],
                                                              format=SCLabel.TIMESTAMP_FORMAT)

        self._collection = []
        self.add_response(score_response=collection)
        self._mode = mode.lower()
        self.modes_available = {"order": OrderIterator,
                                }
        self._iterator_construct = self.modes_available.get(self._mode, OrderIterator)

        self.rp_payload_df: DataFrame = None
        self.clean_payload_df: DataFrame = None

    def __iter__(self) -> OrderIterator:
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """
        return self._iterator_construct(self._collection)

    def get_reverse_iterator(self) -> OrderIterator:
        return self._iterator_construct(self._collection, True)

    def add_response(self,
                     score_response: Union[ScoreResponse, List[ScoreResponse]]):

        if isinstance(score_response, ScoreResponse):
            score_response = [score_response]

        if all(isinstance(x, ScoreResponse) for x in score_response):
            self._collection.extend(score_response)
            if self.tabulate and self.tabulate_serialize:
                from .encoder import ScoreResponseEncoder

                serialize_ = json.dumps(score_response, cls=ScoreResponseEncoder)
                self.tabulate_frame = self.tabulate_frame.append(json.loads(serialize_),
                                                                 ignore_index=True)
            elif self.tabulate:
                for each_score in score_response:
                    self.tabulate_frame = self.tabulate_frame.append(each_score.to_dict(),
                                                                     ignore_index=True)

    def extend(self, collection):
        """
        :param collection: Must Be Instance of ScoreResponseCollection Iterable
        :return:
        """
        if type(collection) is type(self):
            self.add_response(score_response=list(collection))
        return

    def extract_rp_payload(self):
        if self.tabulate and self.score_cls:
            _valid_rp_payloads = self.tabulate_frame.loc[self.tabulate_frame['rp_payload_validated'] == True]['request_processed_payload']
            cols_ = list(self.score_cls.each_request_processed_schema.keys())
            self.rp_payload_df = pd.DataFrame([pd.Series(x, index=cols_) for x in _valid_rp_payloads],
                                              columns=cols_)

            display(self.rp_payload_df)
        else:
            print("Flag Must Be Set at Init: ['tabulate', 'score_cls'] ")

    def extract_clean_payload(self):
        if self.tabulate and self.score_cls:
            _valid_clean_payloads = self.tabulate_frame.loc[self.tabulate_frame['clean_payload_validated'] == True]['clean_payload']
            cols_ = list(self.score_cls.each_pre_processed_schema.keys())
            self.clean_payload_df = pd.DataFrame([pd.Series(x, index=cols_) for x in _valid_clean_payloads],
                                              columns=cols_)

            display(self.clean_payload_df)
        else:
            print("Flag Must Be Set at Init: ['tabulate', 'score_cls'] ")

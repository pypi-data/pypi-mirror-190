import os
import pickle
import pandas as pd
from datetime import datetime, timedelta, timezone

from .utils import create_minio_client
from .constants import Minio


class TimeTravelLoaderMixin:
    """
    Enables Retrieval of Objects across time range from serving models.
    """
    def __init__(self,
                 *args,
                 **kwargs):
        self.keys_to_exclude = ("score_func.pkl",)

    def load_from_time(self,
                       ml_model_id: str,
                       ml_version_id: str,
                       from_timestamp: datetime,
                       to_timestamp: datetime,
                       add_data_to_catalog: bool = False,
                       file_name: str = None,
                       minio_client: object = None
                       ):
        """
        This will retrieve payloads and valid payload from selected time frame.

        :param ml_model_id: Model Id String
        :param ml_version_id: Version Id String
        :param from_timestamp: From TimeStamp Must Be Timezone Aware (UTC) ex: datetime.now(timezone.utc)
        :param to_timestamp:  To TimeStamp Must Be Timezone Aware (UTC) ex: datetime.now(timezone.utc)
        :param add_data_to_catalog:
            if True data will be persisted in Mosaic AI DATA Section.
            Requires tabulate=True at Init.
            Note: This will first download data into your workspace.
        :param file_name:
            If Provided Will Upload Data With Same Name in Mosaic AI Data Catalog.
            Requires tabulate=True at Init.
        :param minio_client: MINIO Client Instance
        :return: Bool
        """
        self.minio_client = minio_client or create_minio_client()
        self.minio_response_path = f"{ml_model_id}/{ml_version_id}/"
        self.all_keys = self.minio_client.list_objects_v2(os.environ[Minio.bucket],
                                                          prefix=self.minio_response_path,
                                                          recursive=True)

        self.only_pickled_objects = [objects_ for objects_ in self.all_keys if objects_.object_name.endswith("pkl")
                                     and not objects_.object_name.endswith(self.keys_to_exclude)]

        self.keys_to_load = [pickled_items for pickled_items in self.only_pickled_objects \
                             if from_timestamp <= pickled_items.last_modified <= to_timestamp]


        self.temp_score_collection_ = []

        for item in self.keys_to_load:
            self.temp_score_collection_\
                .extend(pickle.load(self.minio_client.get_object(os.environ[Minio.bucket], item.object_name)))

        self.add_response(score_response=self.temp_score_collection_)

        if add_data_to_catalog and self.tabulate_frame is not None:
            from connector.mosaicio import MosaicioConnector
            self.io_connector = MosaicioConnector()
            name = file_name or "{}_{}.csv".format(datetime.strptime(from_timestamp, '%Y_%m_%d'),
                                                    datetime.strptime(to_timestamp, '%Y_%m_%d'))
            self.tabulate_frame.to_csv(name, index=False)
            self.io_connector.upload(name)


        return True

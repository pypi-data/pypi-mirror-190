# -*- coding: utf-8 -*-
import os


class MosaicAI:
    server = os.getenv("MOSAIC_AI_SERVER", "http://localhost:5000/registry/api")


class MLModelMetricsV1:
    lc = "/v1/ml-model/metrics"
    rud = "/v1/ml-model/metrics/{version_id}/{tag}"
    u = "/v1/pipeline/{pipeline_id}/tag/{tag}"


class Client:
    config_file = "~/.mosaic.ai"


class Headers:
    authorization = "Authorization"
    x_project_id = "X-Project-Id"


class MLModelType:
    classification = "classification"
    regression = "regression"

from datetime import  datetime


class ScoreLabel:
    Note= "Fields Marked Asterisk (*) Can Be Validated On Proper Input"
    Request_Return_Type = "Return Type Must Be Tuple (n_input, payloads)"
    Request_Return_Shape = "Tuple Must Be of length Two (n_input, payloads)"
    Request_Many_Payload_DType = "* if n_input > 1 payload type must be List (n_input, [np.ndarray, tf.Tensor, etc])"
    ERP_Schema_Dtype = "variable each_request_processed_schema must be of OrderedDict"
    Correct_Mapping_With_Schema = "Each Payload Is Successfully Validated With each_request_processed_schema" \
                                  " after request_processing_fn"


class ValidationBoxLabel:
    VALIDATION = [ScoreLabel.Request_Return_Type,
                  ScoreLabel.Request_Return_Shape,
                  ScoreLabel.Request_Many_Payload_DType,
                 ]

    COMPONENT = ["request_processing_fn",
                 "request_processing_fn",
                 "request_processing_fn",
                 ]

    PASSED = [False,
              False,
              True,
              ]

    SKIPPED = [True for i in range(3)]


class ScoreResponseLabel:
    TIMESTAMP_FORMAT = "%m/%d/%Y, %H:%M:%S"


class ScoreResponseCollectionLabel:
    SCORE_RESPONSE_FIELDS = ["_uuid",
                             "timestamp",
                             "score_request",
                             "request_processed_payload",
                             "rp_payload_validated",
                             "clean_payload",
                             "clean_payload_validated",
                             "score_response"]

    SCORE_RESPONSE_DTYPES = ['str',
                             'datetime',
                             'object',
                             'object',
                             'bool',
                             'object',
                             'bool',
                             'object'
                             ]


class Minio:
    url = "MINIO_URL"
    bucket = "MINIO_BUCKET"
    access_key = "MINIO_ACCESS_KEY"
    secret_key = "MINIO_SECRET_KEY"

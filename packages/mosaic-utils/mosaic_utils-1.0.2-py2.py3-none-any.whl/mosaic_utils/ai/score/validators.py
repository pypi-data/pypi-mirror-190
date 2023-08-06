from .constants import ScoreLabel
from collections import OrderedDict
import numpy as np


class GenericValidatorMixin:
    def update_validation_box(self, filter_condition, update_column, value):
        self.validation_box.loc[
            self.validation_box["VALIDATION"] == filter_condition,
            update_column
        ] = value
        return True


class PayloadSchemaValidatorMixin(GenericValidatorMixin):
    def validate_with_schema_payload(self,
                                     schema_variable: OrderedDict,
                                     validate_with_schema=None):

        if isinstance(schema_variable, OrderedDict):
            if hasattr(validate_with_schema, 'tolist') and callable(validate_with_schema.tolist):
                # Either Torch Tensor or Numpy
                validate_with_schema = validate_with_schema.tolist()
            elif hasattr(validate_with_schema, 'numpy') and callable(validate_with_schema.numpy):
                # Either Tensorflow Tensor
                validate_with_schema = validate_with_schema.numpy().tolist()

            val_ = all(map(lambda obj_, dtype: isinstance(obj_, dtype),
                           list(validate_with_schema),
                           list(schema_variable.values())
                           ))

            if not val_:
                print("Invalid: {} Expected {}".format(validate_with_schema,
                                                       list(schema_variable.values())))
                return False
        else:
            return False
        return True


class RequestValidatorMixin(GenericValidatorMixin):
    def validate_request(self, request_processed_input):
        if isinstance(request_processed_input, tuple):
            self.update_validation_box(ScoreLabel.Request_Return_Type, "PASSED", True)
        else:
            return
        self.update_validation_box(ScoreLabel.Request_Return_Type, "SKIPPED", False)

        if len(request_processed_input) == 2:
            self.update_validation_box(ScoreLabel.Request_Return_Shape, "PASSED", True)
            self.update_validation_box(ScoreLabel.Request_Return_Shape, "SKIPPED", False)

            n_input, payload = request_processed_input
        else:
            return

        if n_input > 1 and not isinstance(payload, list):
            self.update_validation_box(ScoreLabel.Request_Many_Payload_DType, "PASSED", False)
        self.update_validation_box(ScoreLabel.Request_Many_Payload_DType, "SKIPPED", False)


from mosaic_utils.ai.score.base import ScoreBase
from typing import Tuple, Union, List, Any
import tensorflow as tf
import numpy as np


class ScoreTemplateExample(ScoreBase):
    """
    This Class Demonstrate How To Implements ScoreBase Interface Class And It Basic Usage.
    """
    def request_processing_fn(self, request) -> Tuple[int,
                                                      Union[np.ndarray,
                                                            List[np.ndarray],
                                                            tf.Tensor,
                                                            List[tf.Tensor],
                                                      ]]:
        """
        Processes Request Object -> Input data. It could be:
                A Numpy array (or array-like), or a list of arrays (in case the model has multiple inputs).
                A TensorFlow tensor, or a list of tensors (in case the model has multiple inputs).
                A dict mapping input names to the corresponding array/tensors, if the model has named inputs.

        :return: (n_inputs, payload's)
        """
        final_payload = []
        raw_payload = request.json

        for each_payload in raw_payload:
            final_payload.append(np.asarray(each_payload))
        print("Processed Payload", (len(final_payload), final_payload))

        return (len(final_payload), final_payload)

    def pre_processing_fn(self,
                          payload: Union[np.ndarray, tf.Tensor]) -> Union[np.ndarray, tf.Tensor]:
        """
        Accepts Single Payload At a time and applies pre_processing_step before prediction
        :param each_payload: Single Payload
        :return: Preprocessed Single Payload
        """
        # Not Doing Any Preprocessing Hence Returned payload
        return payload

    def prediction_fn(self,
                      model: Any,
                      pre_processed_input: Union[np.ndarray, tf.Tensor]
                      ):
        """
                Does the main prediction on pre_processed_input using supplied model.

                :param model: Supported Model
                :param pre_processed_input: Single Preprocessed Payload
                :return: Prediction Value From the model
        """

        return model.predict(pre_processed_input)

    class Meta:
        # List of Callables() can be attached For Calling After And Before Scoring
        pre_call_hooks = []
        post_call_hooks = []


if __name__ == "__main__":
    class FlaskRequest:
        """This is A Dummy Request Mocking Input"""
        json = [[12, 5, 2, 4],
                [7, 6, 8, 8],
                [1, 6, 7, 7]]

    from random import randint

    class MockModel:
        """This is A Dummy Model Mocking Model Prediction"""
        def predict(self, input):
            return randint(0, 9)

    obj = ScoreTemplateExample()
    model_predictions = obj.score(MockModel(), FlaskRequest(), dry_run=True)

    print("Model Prediction")
    print(model_predictions)

    print("Model Prediction Encoding")
    import json
    from mosaic_utils.ai.score.encoder import ScoreResponseDecoder, ScoreResponseEncoder
    d = json.dumps(model_predictions, cls=ScoreResponseEncoder)
    print(d)

    print("Model Prediction Decoding")
    e = json.loads(d, cls=ScoreResponseDecoder)
    print(e)


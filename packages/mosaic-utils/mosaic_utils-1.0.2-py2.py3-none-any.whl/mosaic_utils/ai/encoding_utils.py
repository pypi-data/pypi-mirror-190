# -*- coding: utf-8 -*-
from base64 import b64decode, b64encode
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def base64_encode(data: str) -> str:
    """ Encodes input string in base64 format """
    data = data.encode("utf-8")
    data = b64encode(data)
    return data.decode("utf-8")


def fix_padding(encoded_string: str) -> str:
    """ method to correct padding for base64 encoding """
    required_padding = len(encoded_string) % 4
    return encoded_string + ("=" * required_padding)


def base64_decode(data: str) -> str:
    """ decodes input string from base64 format"""
    data = data.encode("utf-8")
    data = b64decode(data)
    return data.decode("utf-8")


class encoder:
    """Encode categorical features."""

    def __init__(self, cat_cols, encoder=None):
        if encoder:
            self.encoder = encoder
        else:
            self.encoder = OneHotEncoder(categories="auto")
        self.cat_cols = cat_cols

    def encode(self, features, fit=False):
        """
        Encode the categorical features and join return merged data.

        Args:
            features: numpy array of features
            fit:    : boolean default False
                      If yes, it performs fit_transform operation
                      else, it performs only transform operation
        Returns:
            Numpy Array with the non categorical features combined
            with the encoded categorical features.
        """
        if not self.cat_cols:
            return None, features

        non_cat_cols = (
            sorted(set(range(features.shape[1])) - set(self.cat_cols)))
        if fit:
            cat_data = self.encoder.fit_transform(features[:, self.cat_cols])
        else:
            cat_data = self.encoder.transform(features[:, self.cat_cols])
        features = np.hstack(
            (features[:, non_cat_cols].astype('float64'), cat_data.toarray()))
        return non_cat_cols, features

    def get_encoder(self):
        return self.encoder


def find_categorical(arry, unique_num_count=10):
    """
        Get categorical and non categorical columns.

        It will treat all non numeric fields for encoding along with
        numeric data having less than unique_num_count unique values.

        """
    df = pd.DataFrame(arry)
    num_cols = set(df._get_numeric_data().columns)
    df = df.apply(lambda x: pd.to_numeric(x, errors="ignore"))
    num_cols = set(df._get_numeric_data().columns)
    cat_cols = set(df.columns) - num_cols

    for col in num_cols:
        if df[col].nunique() <= unique_num_count:
            cat_cols.add(col)

    non_cat_cols = sorted(set(df.columns) - cat_cols)
    cat_cols = sorted(cat_cols)
    return cat_cols, non_cat_cols

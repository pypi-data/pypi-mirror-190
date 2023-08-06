
import sys
import os
from importlib import import_module
from sklearn.feature_extraction import text 
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from sklearn.preprocessing import OneHotEncoder
from importlib import import_module
from sklearn.compose import ColumnTransformer
import random
import re
import nltk
nltk.download('stopwords')
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
# init stemmer
stemmer = SnowballStemmer('english')
stops = list(stopwords.words('english'))
def preprocessor(text):
    # 1. Delete HTML 
    review_text = BeautifulSoup(text, 'html.parser').get_text()
    # 2. Make a space
    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)
    # 3. lower letters
    words = letters_only.lower().split()
    # 5. Stopwords 
    meaningful_words = [w for w in words if not w in stops]
    # 6. Stemming
    stemming_words = [stemmer.stem(w) for w in meaningful_words]
    # 7. space join words
    return( ' '.join(stemming_words))



import_loader = {
    'CountVectorizer': CountVectorizer(preprocessor=preprocessor,stop_words=stops)
}



def load_scoring_function(scoring_func):
    """
    converts mymodule.myfunc in the myfunc
    object itself so tpot receives a scoring function
    """
    if scoring_func and ("." in scoring_func):
        try:
            module_name, func_name = scoring_func.rsplit('.', 1)

            module_path = os.getcwd()
            sys.path.insert(0, module_path)
            scoring_func = getattr(import_module(module_name), func_name)
            sys.path.pop(0)

            print('manual scoring function: {}'.format(scoring_func))
            print('taken from module: {}'.format(module_name))
        except Exception as e:
            print('failed importing custom scoring function, error: {}'.format(str(e)))
            raise ValueError(e)

    return scoring_func

class IdentityTransformer(TransformerMixin, BaseEstimator):
    """Identity-transformer for doing literally nothing"""
    def fit(self, X, y=None, **fit_params):
        return self
    def transform(self, X):
        return X

class PreprocessTransformer(TransformerMixin):
    
    def __init__(self, numeric_columns=[], categorical_columns=[], text_columns=[],
    text_transformer = 'CountVectorizer'):
        self.numeric_columns = numeric_columns
        #self.categorical_columns = categorical_columns
        self.text_columns = text_columns
        self.text_transformer = text_transformer
        #self.categorical_transformer = categorical_transformer
        
    def _setup_columns(self):
        def text_to_list(text):
            if type(text) is list:
                return text
            return [text]
        self.numeric_columns = text_to_list(self.numeric_columns)
        #self.categorical_columns = text_to_list(self.categorical_columns)
        self.text_columns = text_to_list(self.text_columns)

        column_list = []
        if len(self.text_columns) > 0:
            load_func = import_loader.get(self.text_transformer, self.text_transformer)
            #load_func = load_func.__class__
            if isinstance(load_func, str):
                load_func = load_scoring_function(load_func)
            for idx, text in enumerate(self.text_columns):
                column_list.append(('text' + str(idx), load_func , text))
        
        if len(self.numeric_columns) > 0:
            column_list.append(('numeric', IdentityTransformer(), self.numeric_columns))
        '''
        if len(self.categorical_columns) > 0:
            load_func = import_loader.get(self.categorical_transformer, self.categorical_transformer)
            if isinstance(load_func, str):
                load_func = load_scoring_function(load_func)
            column_list.append(('categorical', load_func, self.categorical_columns))
        '''    
        self.column_transformer = ColumnTransformer(column_list)

    def fit(self, X, y=None):
        self._setup_columns()
        self.column_transformer.fit(X, y)
        return self
    def transform(self, X):
        return self.column_transformer.transform(X)  

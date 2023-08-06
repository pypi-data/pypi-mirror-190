# -*- coding: utf-8 -*-
"""
This Package Defines core structure for Revamped Model Scoring.
===================================================================

Model scoring version 2.0 Has replaced old linear scoring function.
The revamped scoring follows three steps:
    1. Request Level Segregation where user seggregates bulk payload.
    2. Preprocessing Level where data preprocessing takes place.
    3. Prediction Level Where Inference happens on using single sample at a time.

Returns: <<ScoreResponse>>

base.py: Core Logic For Defining Scoring Abstract Class <<ScoreBase>>
response.py: Defines Response Schema <<ScoreResponse>>

encoder.py:
    - ScoreResponseEncoder : [<<ScoreResponse>>,..] object to JSON Convertor
    - ScoreResponseDecoder: JSON -> To [<<ScoreResponse>>, .. ] Convertor
iterators.py: <<ScoreResponseCollection>> holds all the score response and makes it iterable
mixins.py: <<TimeTravelLoaderMixin>>

constants.py: Constants
utils.py: Utility
validators.py:  Validations

"""

__author__ = "Shivam Chaurasia (10670364)"
__description__ = "Revamped Model Scoring Package"
__version__ = "2.0"
__deprecated__ = False
__date__ = "26 Feb, 2021"

# -*- coding: utf-8 -*-
import functools
import sys
from flask import current_app
import logging


def log_decorator(_func=None):
    """Logging Decorator"""

    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(*args, **kwargs):
            """log function begining"""

            try:
                LOGGER = current_app.logger
            except:
                LOGGER = logging.getLogger("default_logger")

            LOGGER.info("Begin function: {0}".format(func.__name__))
            try:
                value = func(*args, **kwargs)
                LOGGER.info("End function: {0}".format(func.__name__))
            except:
                LOGGER.error(f"Exception: {str(sys.exc_info()[1])}")
                LOGGER.info("End function: {0} with exception".format(func.__name__))
                raise
            return value

        return log_decorator_wrapper

    if _func is None:
        return log_decorator_info
    return log_decorator_info(_func)

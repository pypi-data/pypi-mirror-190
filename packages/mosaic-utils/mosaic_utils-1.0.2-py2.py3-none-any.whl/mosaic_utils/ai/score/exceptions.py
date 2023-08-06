#! -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
""" This module contains different exceptions used by the mosaic AI serving """


class MosaicException(Exception):
    """ Common/Custom exceptions """

    code = 500
    message = "Internal Server Error"

    def __init__(self, message, code):
        self.message = message
        self.code = code

# -*- coding: utf-8 -*-
"""validators.py: Handler for handling all validations."""

__author__ = "Shivam Chaurasia (10670364)"
__description__ = "Implements ValidationHandler which composites all the validations present in validations.py"
__version__ = "0.1"

from .validations import *
from typing import List, Dict
import logging


class ValidationHandler(object):
    purpose = "Handler/MosaicAiClient/ValidatorEngine"

    def __repr__(self):
        return self.purpose

    def __init__(self,
                 mandatory_fields: Dict = None,
                 alphanum_uscore_excl: Dict = None,
                 if_present_validate_type: Dict = None,
                 if_present_sub_field_must_exist: Dict = None
                 ):
        '''
        Specify all the Parent and Subfield Name and Values for validations needs to be handled.
        ===============================================

        :param mandatory_fields
            : Dict[Name: Value]
            ex: {"variable_name": value, "variable_name": value, ..}
        :param alphanum_uscore_excl
            : Dict[Name: Value]
            ex: {"variable_name": value, "variable_name": value, ..}
        :param if_present_validate_type
            : Dict[Name:Tuple(DTypes)]
            ex:
            {
                "parent_var_name": tuple(parent_var_value, tuple(d_types,...)),
                "parent_var_name": tuple(parent_var_value, tuple(d_types,...)),
                ...
            }
        :param if_present_sub_field_must_exist
            : Dict[ParentName:Tuple(ParentValue, Dict[SubField: SubFieldValue])]
            ex:
            {
                "parent_var_name": (parent_var_value,
                                    {"sub_field_name": sub_field_value,
                                     "sub_field_name": sub_field_value,
                                     ...
                                     },..),
                "parent_var_name": (parent_var_value,
                                    {"sub_field_name": sub_field_value,
                                     "sub_field_name": sub_field_value,
                                     ...
                                     },..),
                ...
            }

        '''

        self._validations = dict()

        if mandatory_fields:
            self._validations.update({"mandatory_fields":
                                          MandatoryFields(mandatory_fields)})

        if alphanum_uscore_excl:
            self._validations.update({"alphanum_uscore_excl":
                                          ANumericUScoresExclusive(alphanum_uscore_excl)})
        if if_present_validate_type:
            self._validations.update({'if_present_validate_type':
                                          IfPresentTypeCheck(fields=if_present_validate_type)})

        if if_present_sub_field_must_exist:
            self._validations.update({'if_present_sub_field_must_exist':
                                          IfPresentSubfieldMustExist(fields=if_present_sub_field_must_exist)})

    def validate(self,
                 mandatory_fields=True,
                 alphanum_uscore_excl=True,
                 if_present_validate_type=True,
                 if_present_sub_field_must_exist=True):
        to_check = list()

        if mandatory_fields and "mandatory_fields" in self._validations.keys():
            to_check.append(self._validations["mandatory_fields"])

        if alphanum_uscore_excl and "alphanum_uscore_excl" in self._validations.keys():
            to_check.append(self._validations["alphanum_uscore_excl"])

        if if_present_validate_type and "if_present_validate_type" in self._validations.keys():
            to_check.append(self._validations["if_present_validate_type"])

        if if_present_sub_field_must_exist and "if_present_sub_field_must_exist" in self._validations.keys():
            to_check.append(self._validations["if_present_sub_field_must_exist"])

        for each_validation_test in to_check:
            status, message = each_validation_test.check()
            if status is False:
                return status, message

        return True, "validation_completed"

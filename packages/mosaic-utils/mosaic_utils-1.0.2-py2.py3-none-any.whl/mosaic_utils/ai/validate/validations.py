# -*- coding: utf-8 -*-
"""validations.py: Defines all validations."""

__author__ = "Shivam Chaurasia (10670364)"
__description__ = "Defines all validations by implementing IValidation Interface"
__version__ = "0.1"

from abc import ABC, abstractmethod
from typing import Dict, Tuple
import logging
import re


class IValidation(ABC):
    """
    Abstract Interface For Implementing Validations
    """
    purpose = NotImplementedError
    _fields = NotImplementedError

    def __init__(self,
                 fields: Dict = None):
        self._fields = dict()
        if fields:
            self._fields.update(fields)

    @abstractmethod
    def check(self) -> Tuple[bool, str]:
        """Interface Implementing Actual Validation"""
        pass

    def __repr__(self):
        return self.purpose


class MandatoryFields(IValidation):
    """
    Validates provided value must exist.

    Usage:
    MandatoryFields(fields: Dict=mandatory_fields)
    :example
        obj = MandatoryFields(fields = {"test_name", 1000})
        assert obj.check() == True
    """
    purpose = "Validation/MandatoryValues"

    def check(self):
        for field_name, value in self._fields.items():
            if value is None or value == '' or str(value).strip() == '':
                return False, f"{field_name} cannot be empty, blank or whitespace"
        else:
            message_ = "PASS:: Mandatory Validation :: {}".format(
                self._fields.keys()
            )
            logging.info(message_)
        return True, "Mandatory_Fields_Validated"


class ANumericUScoresExclusive(IValidation):
    """
    Validates provided value must be AlphaNumeric(A-Z,a-z,0-9) and underscores.
    Starting and Ending underscore are not allowed.

    Usage:
    ANumericUScoresExclusive(fields: Dict=mandatory_fields)
    :example
        obj = ANumericUScoresExclusive(fields = {"test_name", "Test_001"})
        assert obj.check() == True
    """
    purpose = "Validation/AlphaNumericAndUScoreExclusive"

    def check(self):
        pattern_alpnumeric = re.compile("^\w+$")
        for field_name, value in self._fields.items():
            if value.startswith("_") or value.endswith("_"):
                return False, f"{field_name} cannot start or ends with underscores"
            if not re.match(pattern_alpnumeric, value):
                return False, f"{field_name} can only contain alphanumeric and underscore"
        else:
            message_ = "PASS:: AlphaNumeric Validation :: {}".format(
                self._fields.keys()
            )
            logging.info(message_)
        return True, "Alphanumeric_Underscore_Exclusive_Fields_Validated"


class IfPresentTypeCheck(IValidation):
    """
    Validates if parent value exist check subfield instance datatypes.

    Usage:
    IfPresentTypeCheck(fields: Dict={"parent_field": (parent_field_val, (dtype_1, dtype_n) )})
    :example
        obj = IfPresentTypeCheck(fields: Dict={"test_parent_field": (True, (int, bool) )})
        assert obj.check() == True
    """
    purpose = "Validation/IfPresentTypeCheck"

    def check(self):
        for field_name, (if_present_value, tuple_of_dtypes) in self._fields.items():
            if if_present_value is not None:
                if not isinstance(if_present_value, tuple_of_dtypes):
                    return False, f"{field_name} must be of type - f{tuple_of_dtypes}"
        else:
            message_ = "PASS:: {} :: {}".format(
                repr(self),
                self._fields.keys()
            )
            logging.info(message_)
        return True, repr(self)


class IfPresentSubfieldMustExist(IValidation):
    """
    Validates if parent value exist check subfield must exist.

    Usage:
    IfPresentSubfieldMustExist(fields: Dict=
        {"parent_field": (parent_field_val,
                            {"subfield_n": subfield_n_value}
                        )
        })
    :example
        obj = IfPresentSubfieldMustExist(fields: Dict={"parent_field": (True,
                                                                            {"test_sub1": "non_empty_val",
                                                                             "test_sub2": "non_empty_val",
                                                                             }
                        )
        })
        assert obj.check() == True
    """
    purpose = "Validation/IfPresentSubfieldMustExist"

    def check(self):
        for field_name, (if_present_value, dict_of_sub_field) in self._fields.items():
            if if_present_value is not None and if_present_value is not False:
                for each_value in  dict_of_sub_field.values():
                    if each_value is None or each_value is '':
                        message_ = "If {field_name} present -> {fields_required} Mandatory"
                        message_ = message_.format(field_name=field_name,
                                                   fields_required=list(dict_of_sub_field.keys())
                                               )
                        return False, message_
        else:
            message_ = "PASS:: {} :: {}".format(
                repr(self),
                self._fields.keys()
            )
            logging.info(message_)
        return True, repr(self)
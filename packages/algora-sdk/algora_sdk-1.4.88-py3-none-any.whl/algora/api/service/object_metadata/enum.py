from typing import Union

from algora.common.base_enum import BaseEnum


class MetadataType(BaseEnum):
    CLASS = "CLASS"
    ENUM = "ENUM"
    ABSTRACT_CLASS = "ABSTRACT_CLASS"


class Type(BaseEnum):
    BUILT_IN = "BUILT_IN"
    ALIAS = "ALIAS"
    REF = "REF"
    CUSTOM = "CUSTOM"


class PythonTypes(BaseEnum):
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    NONE = "NONE"
    LIST = "LIST"
    SET = "SET"
    UNION = "UNION"

    @classmethod
    def from_primitive(cls, primitive):
        value_lookup = {
            bool: "BOOLEAN",
            int: "INTEGER",
            float: "FLOAT",
            str: "STRING",
            type(None): "NONE",
            None: "NONE",
            list: "LIST",
            set: "SET",
            Union: "UNION",
        }
        value = value_lookup[primitive]
        return cls(value=value)

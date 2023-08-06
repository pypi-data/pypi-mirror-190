from enum import Enum


class SapioAccessType(Enum):
    """
    All access types that are visible to webservice.
    """
    READ = 0
    WRITE = 1
    DELETE = 2

"""Enums used by functions."""
from enum import Enum

class MatchMode(Enum):
    """Match mode used by xmatch and xlookup"""
    EXACT = 0
    NEXT_LARGER = 1
    NEXT_SMALLER = -1
    WILDCARD = 2
    REGEX = 3

class SearchMode(Enum):
    """Search mode used by xmatch and xlookup"""
    FROM_FIRST = 1
    FROM_LAST = -1
    BINARY_FROM_FIRST = 2
    BINARY_FROM_LAST = -2

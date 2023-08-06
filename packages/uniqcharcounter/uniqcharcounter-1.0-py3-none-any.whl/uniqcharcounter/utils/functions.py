from collections import Counter
from functools import lru_cache
from typing import List

from .exceptions import CustomTypeErrorException


@lru_cache
def count_uniq_chars_in_string(string: str) -> int:
    """Receive "str" and return count of uniq chars in string"""
    if not isinstance(string, str):
        raise CustomTypeErrorException(
            f"Wrong data type {type(string)}, must be a {str}"
        )
    count_for_all_chars_in_string = Counter(string).values()
    count_uniq_chars = len(
        [number for number in count_for_all_chars_in_string if number == 1]
    )
    return count_uniq_chars


def count_uniq_chars_in_list(string_data: List[str]) -> List[int]:
    """Receive list["st1", "str2"] and return count of uniq chars list[count1, count2]"""
    if not isinstance(string_data, list):
        raise CustomTypeErrorException(
            f"Wrong data type {type(string_data)}, must be a {list}"
        )
    return list(map(count_uniq_chars_in_string, string_data))

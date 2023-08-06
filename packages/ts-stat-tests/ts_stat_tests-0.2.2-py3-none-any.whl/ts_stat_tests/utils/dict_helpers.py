from typing import List
from typing import Union


def dict_slice_by_keys(dictionary: dict, keys: Union[str, List[str]]):
    if isinstance(keys, str):
        keys = [keys]
    return {key: value for key, value in dictionary.items() if key in keys}

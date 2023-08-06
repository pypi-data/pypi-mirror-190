from functools import lru_cache
from collections import Counter


def count_unique_chars(string : str, cache : dict):
    if string in cache:
        return cache[string]
    chars = {}
    for char in string:
        chars[char] = chars.get(char, 0) + 1
    unique_count = 0
    for c_val in chars.values():
        if c_val == 1:
            unique_count += 1
    cache[string] = unique_count
    return unique_count

@lru_cache(maxsize=None)
def count_unique_chars2(string : str):
    counter = Counter(string)
    unique_count = 0
    for c_val in counter.values():
        if c_val == 1:
            unique_count += 1
    return unique_count
## collect_framework

This package allows you to count unique characters in a given string or a file. 

### Installation

pip install collect_framework

### Usage

collect_framework --string "your string"

collect_framework --file path_to_text_file

collect_framework --string “your string” --file path_to_text_file

### Tests

To run the tests, you can use `pytest` library, after installing it

### Note

For large file, package have two methods for counting unique characters, first one is using cache, second one is using lru_cache from functools library
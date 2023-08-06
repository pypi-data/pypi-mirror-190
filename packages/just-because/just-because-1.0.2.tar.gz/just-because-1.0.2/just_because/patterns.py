from typing import List
from os.path import join
from os.path import dirname
from re import compile as Compile
from itertools import product

def load_words(file_name: str) -> List[str]:
    """
    this function is used to load words from .txt file.
    """
    with open(join(dirname(__file__), 'words', f'{file_name}.txt'), 'r', encoding='utf8') as file:
        return list(file.read().strip())

ji_pattern = Compile('|'.join(load_words('ji')))
zhiyin_pattern = Compile('|'.join(x + y for x, y in product(load_words('zhi'), load_words('yin'))))

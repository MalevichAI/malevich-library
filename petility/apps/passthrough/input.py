from jls import jls, Context, DF, DFS, M
from typing import Any


@jls.input_true(collection_from='input_collection')
def from_input_collection():
    pass


@jls.input_true(collection_from='input_collection_1')
def from_input_collection_1():
    pass


@jls.input_true(collection_from='input_collection_2')
def from_input_collection_2():
    pass


@jls.input_true(collection_from='extra_collection')
def from_extra_collection():
    pass


@jls.input_true(collection_from='extra_collection_1')
def from_extra_collection_1():
    pass


@jls.input_true(collection_from='extra_collection_2')
def from_extra_collection_2():
    pass
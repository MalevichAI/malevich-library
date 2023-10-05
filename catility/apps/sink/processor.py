from jls import jls, DF
from typing import Any


@jls.processor()
def sink_2(_d1: DF[Any], _d2: DF[Any]):
    return _d1, _d2


@jls.processor()
def sink_3(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any]):
    return [_d1, _d2, _d3]


@jls.processor()
def sink_4(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any], _d4: DF[Any]):
    return [_d1, _d2, _d3, _d4]


@jls.processor()
def sink_5(_d1: DF[Any], _d2: DF[Any], _d3: DF[Any], _d4: DF[Any], _d5: DF[Any]):
    return [_d1, _d2, _d3, _d4, _d5]


# TODO:
# Develop a processor that will allow to pack an arbitrary number of dataframes
# def pack(*dfs: Sink[Any]): ...

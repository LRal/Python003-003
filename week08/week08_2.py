"""
自定义一个 python 函数，实现 map() 函数的功能。
"""

from typing import Callable, Sequence, Iterator


def map_(func: Callable, *seq: Sequence) -> Iterator:
    for args in zip(*seq):
        yield func(*args)

if __name__ == '__main__':
    a = map_(lambda x: x ** 2, range(100))
    print(next(a))
    print(list(a))

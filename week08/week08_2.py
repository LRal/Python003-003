"""
自定义一个 python 函数，实现 map() 函数的功能。
"""

from typing import Callable, Sequence, Iterator

def map_(func: Callable, seq: Sequence) -> Iterator:
    length = len(seq)
    for i in range(length):
        if func(i) in seq:
            yield func(i)

def square(x):
    return x ** 2

if __name__=='__main__':
    a = map_(square, range(100))
    print(next(a))
    print(list(a))

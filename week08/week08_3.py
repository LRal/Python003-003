"""
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
"""

import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.clock()
        func(*args, **kwargs)
        end_time = time.clock()
        print(end_time - start_time)
    return wrapper


@timer
def sum_(n):
    total = 0
    for num in range(n):
        total += num
    print(total)


if __name__ == '__main__':
    sum_(12345678)

# 装饰器

简单地说, 装饰器是修改其他函数的功能的函数/类
它主要有两个作用:

- 让代码更优雅
- 扩展函数功能

## 装饰器基础

### 实现一个最简单的装饰器

实现一个叫做 decorator 的装饰器

```python
def decorator(func):  # 把被装饰函数 func 作为对象传进 decorator 中, 注意把函数作为对象来使用的时候是不带括号的
    def wrapper():  # 真正运行的函数 wrapper
        # print('你可以在 func 前面做点事')
        func()  # 运行 func 函数, 或者进行与 func() 相关的操作
        # print('你也可以在 func 后面做点事')
    return wrapper  # 必须返回, 不然返回 NoneType, 不可被调用
```

> 真正运行的是 wrapper 函数, 让我们在不修改 func 的前提下扩展了 func 的功能

### 装饰器的使用

```python
@decorator
def function():
    print('hi')

# 上面代码等价于
def function():
    print('hi')
function = decorator(function)  # 重新定义 function
```

> 使用装饰器的代码更优雅、直观

### 装饰器对被装饰函数的影响

当一个函数在定义的时候被装饰过, 它就不是原来的函数了

```python
# 被装饰前
def function():
    """我是干净的, 没有被装饰过"""
    pass

function.__name__  # 查看 function 的名字, 输出: 'function'
function.__doc__  # 查看 function 的注释文档, 输出: '我是干净的, 没有被装饰过'

# 被装饰后
@decorator
def function():
    """我不干净了, 被装饰过了"""
    pass

function.__name__  # 输出: 'wrapper'
function.__doc__  # 输出为空
```

为了解决这个问题, python 提供了一个简单的函数 functools.wraps

```python
from functools import wraps

def decorator(func):
    @wraps(func)  # 在装饰器函数里加上这样一行代码, 使 func 结构不变
    def wrapper():
        func()
    return wrapper

@decorator
def function():
    """虽然不干净了, 被装饰过了, 但, 我还是原来的我"""
    pass

function.__name__  # 输出: 'function'
function.__doc__  # 输出: '虽然不干净了, 被装饰过了, 但, 我还是原来的我'
```

## 装饰器更高级的用法

### 带参数/返回值的被装饰函数

有时候被装饰函数会带有参数或者返回值, 对 wrapper 函数进行相应的处理即可

```python
def decorator(func):
    def wrapper(*args, **kwargs):  # 如果 func 带参数, wrapper 也要写上相应的参数
        return_ = func(*args, **kwargs)
        return return_  # 如果 func 有返回值, wrapper 也要有返回值
    return wrapper
```

### 带参数的装饰器

想给装饰器添加参数, 只要在原来的装饰器外嵌一层函数即可

```python
def decorator_with_arg(fargs):  # 带参数的装饰器
    def decorator(func):  # 原来的装饰器
        def wrapper():
            func()
            print(fargs)
        return wrapper
    return decorator
```

### 装饰器堆叠

有时候想给函数带上多个装饰器, 要注意装饰器堆叠的顺序

```python
@decorator1  # decorator1 装饰 装饰了 function 的 decorater2
@decorator2  # decorator2 装饰 function
def function():
    pass
```

### 装饰器与类

#### 类装饰器

当我们想用一个装饰器实现两个或多个功能, 除了嵌套函数, 还可以使用类继承的方式去实现
后者往往能使代码更整洁, 因此引入类装饰器

```python
# BaseDecorator 用来实现功能一
class BaseDecorator:
    # 在这个位置根据需要写 __init__ 方法, 通常声明 func 的参数和类装饰器本身的参数

    def __call__(self, func):  # 在 __call__ 方法写装饰器函数
        def wrapper1():
            func()  # 在这个位置实现功能一
        return wrapper

    def wrapper2(self):
        # 这个函数用于继承
        pass

# SubDecorator 用来实现功能二
class SubDecorator(BaseDecorater):
    def __init__(self):
        super().__init__()  # 继承类装饰器和 func 的参数

    def wrapper2(self):
        # 在这个位置实现功能二
        pass
```

从现在起, `@BaseDecorator` 能够实现功能一, `@SubDecorator` 能够实现功能一和功能二

#### 装饰类的装饰器

```python
# 在装饰器函数中直接写一个类
def decorator(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)

        def display(self):
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()
    return newClass

@decorator
class MyClass(object):
    def __init__(self, number):
        self.number = number

    # 重写display
    def display(self):
        print("number is",self.number)

six = MyClass(6)
for i in range(5):
    six.display()
```

## 装饰器常用应用

### lru_cache()

LRU 缓存机制, 适合用于装饰一些递归函数, 从而大幅提升程序性能, 如 Fibonacci 数列

```python
from functools import lru_cache

@lru_cache()  # 注意要带括号
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))

# 可以对比使用 lru_cache() 前后要花多久
```

### 授权

装饰器能有助于检查某个人是否被授权去使用一个 web 应用的端点(endpoint), 它们被大量使用于 Flask 和 Django web框架中

```python
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated
```

### 日志功能

```python
from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
   """Do some math."""
   return x + x
```

### 添加属性

```python
def attrs(**kwds):
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate

@attrs(versionadded="2.2", author="Guido van Rossum")
def mymethod(f):
    pass
```

### 函数参数观察(方便调试)

```python
import functools

def trace(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(f, args, kwargs)
        result = f(*args, **kwargs)
        print(result)
    return decorated_function

@trace
def greet(greeting, name):
    return '{}, {}!'.format(greeting, name)

greet('better','me')
```

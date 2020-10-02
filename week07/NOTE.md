# python 面向对象基础 - 封装篇

在 python 中，一切皆对象，类也是对象。
类这个对象，是一群有着相同属性和方法的对象的集合，作用是把这些属性和方法封装起来。

## 属性

### 如何查看对象属性

`dir()` 和 `__dict__`

#### `dir()`  查看所有属性

`dir()` 是一个函数，返回一个 list，里面包括对象所有的属性名。
当你想查看对象 <object\> 的某个属性时，可以先用 `<object>.dir()` 查看属性名 <attr\>，再使用 `<object>.<attr>` 了解其属性值。

```python
class Foo:
    pass

Foo.dir()  # 获取属性名列表
Foo.<attr>  # 在属性名列表中选取属性 <attr>，查看它的值
```

#### `__dict__`  查看可写属性

`__dict__` 本身是一个属性，返回一个字典，它储存了对象内**可写**属性的名称和值。
不是所有的对象都有 `__dict__` 属性。

### 属性类型

在类中声明一个属性时，我们不仅仅要考虑它的变量名，还需要考虑外部对它的操作权限。

#### 属性作用域

- `var`
    公有属性，能在类的内外部使用
- `_var`
    约定只在内部使用，不具有强制性。
    本质上还是公有属性，能在类的内外部使用。
    但是当使用通配符导入时（如 `from test import *`），将会被 python 解释器忽略。
    因此，任何时候都不建议使用通配符导入。
- `__var`
    私有属性，只能在类的内部使用。
    使用 `dir()` 或 `__dict__` 查看时，会发现私有属性的名称已经被解释器修改为 `_类名__var`。（因此你也可以通过这种方式去强制获取私有变量，但是不推荐）

> 下划线的其他用法：
> `__var__`: 魔法方法(magic method)，最好避免使用这种方式命名你自己的变量，以避免与将来Python语言的变化产生冲突。
> `var_`：避免与 python 关键字产生冲突的命名方式
> `_`: 用作临时或无意义变量的名称，也表示 python REPL（就是那个交互式解释器） 中最近一个表达式的结果。
> 下划线可以用在变量上，而不仅仅是类的属性和方法。

#### `@property` 装饰器

对属性的操作有三种：访问(`__get__`)、修改(`__set__`)、删除(`__delete__`)。
对于公有属性，外部可以自由进行三种操作；对于私有属性，外部不能进行任何操作。
但有时候，我们只想对属性进行其中的一种或两种操作，而公私属性都不能满足这种需求，这个时候，就可以引入 `@property` 装饰器。

##### 使用 `@property`

```python
class Person:
    def __init__(self):
        self._gender = None

    @property  # 属性的 getter 使用 @property 即可，无需使用 @*.getter
    def gender(self):
        print(self._gender)  # getter

    @gender.setter
    def gender(self, value):
        self._gender = value  # setter

    @gender.deleter
    def gender(self):
        del self._gender  # deleter

yan = Person()
# 经过 @property 修饰后，gender() 已经不再是一个函数，而是一个属性。
# 调用它也要用调用属性的方式，而不是使用调用函数的方式。
yan.gender = 'M'
yan.gender
del yan.gender
```

##### `@property` 原理

```python
# property 本质是一个类
class property(object):
    def __init__(self, fget: Optional[Callable[[Any], Any]] = ...,
                 fset: Optional[Callable[[Any, Any], None]] = ...,
                 fdel: Optional[Callable[[Any], None]] = ...,
                 doc: Optional[str] = ...) -> None: ...
    def getter(self, fget: Callable[[Any], Any]) -> property: ...
    def setter(self, fset: Callable[[Any, Any], None]) -> property: ...
    def deleter(self, fdel: Callable[[Any], None]) -> property: ...
    def __get__(self, obj: Any, type: Optional[type] = ...) -> Any: ...
    def __set__(self, obj: Any, value: Any) -> None: ...
    def __delete__(self, obj: Any) -> None: ...
    def fget(self) -> Any: ...
    def fset(self, value: Any) -> None: ...
    def fdel(self) -> None: ...
```

在 python 底层，实现访问修改删除三种操作的是 `__get__`, `__set__`, `__delete__` 三种方法，但是使用这三种方法的时候，（因为底层）可能需要加上一些和类本身无关的参数，这影响了代码的优雅和可读性。
因此，我们通常会把这三种方法写在 property 类中封装起来，然后通过装饰器 `@` 声明，来实现它们的功能。

### 属性的一些高级用法

#### `__getattribute__` 和 `__getattr__`

- `__getattribute__`: 无条件调用，即每次通过实例访问属性，都会调用一次
- `__getattr__`: 调用完 `__getattribute__` 后，当属性不存在时，会调用 `__getattr__`

```python
class Person:
    def __init__(self):
        self.age = 18

    def __getattribute__(self, value):
        print('call __getattribute__')
        return super().__getattribute__(value)  # 注意要用 super() 而不是 self
    # 如果使用 self，会再次触发__getattribute__方法的调用，代码将会陷入无限递归
    # 所以要使用 super() 把访问属性的方法指向一个更高级的超类

    def __getattr__(self, value):
        print('call __getattr__')
        return f'参数 {value} 不存在'

person = Person()
print(person.age)
print(person.name)

# 输出：
# call __getattribute__
# 18
# call __getattribute__
# call __getattr__
# 参数 name 不存在
```

> 通过修改 `__getattribute__` 和 `__getattr__`，为访问属性添加额外的功能。

## 方法

在类中，一共有三种方法。

```python
class Foo:
    def instance_method(self[, var]):
        print('实例方法')

    @classmethod
    def class_method(cls[, var]):
        print('类方法')

    @staticmethod
    def static_method([var]):
        print('静态方法')
```

### 实例方法

需要带 self 参数，是约定好的参数，表示把类的实例传进来。
只能被实例对象调用。

### 类方法

装饰器 `@classmethod`。
需要带 cls 参数，也是约定好的参数，表示把正在调用这个类方法的类传进来。
主要用来解决两个问题：一是实现不同的构造函数；二是在父类中创建类方法，子类通过调用这个类方法，修改变量的值。

```python
# 实现不同的构造函数
# 这里的类方法由 Person 类调用，cls 指 Person 类

class Person:
    def __init__(self, name):
        self.name = name

    @classmethod
    def process_name(cls, wierd_name):
        # 做一些处理，把 wierd_name 转化为 name，如：
        # name = str(wierd_name)
        return cls(name)

person1 = Person('name')  # 调用 __init__
person2 = Person.process_name('wierd_name')  # 调用类方法
```

```python
# 根据需求改变属性值
# 这里的类方法由 Apple 类调用，cls 指 Apple 类

class Fruit:
    """ 父类 Fruit """
    PRICE = 0

    @classmethod
    def set_price(cls, price):
        print(f' {cls} 的价格是 {price}')
        cls.PRICE = price

class Apple(Fruit):
    """ 子类 Apple """
    pass

Apple.set_price(100)
# <class '__main__.Apple'> 的价格是 100
```

### 静态方法

装饰器 `@staticmethod`。
不需要带特定参数。
如果一个函数不涉及到访问修改这个类的属性，而放到类外面又有点不恰当，这个时候就可以以静态方法的形式放到类中。它通常可以用来做一些简单独立的任务，比如判断。

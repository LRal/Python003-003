# 多进程

multiprocessing 是一个用于处理多进程的 python 内置模块。

## 0. 多线程与多进程，及相关概念

### 多线程与多进程的关系

两者可以共存，而且在 python 中往往一起使用。  
一个进程里可以创建多个线程。  

### 阻塞和非阻塞 与 同步和异步

#### 阻塞和非阻塞

这两个是调用方的概念。  
阻塞：得到调用结果之前，线程会被挂起（只能一次调用一个线程）  
非阻塞：不能立即得到结果，不会阻塞线程（可以同时调用多个线程）  

#### 同步和异步

这两个是被调用方的概念。  
同步：得到结果之前，调用不会返回
异步：请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果

## 1. 多进程的创建

Process 是 multiprocessing 的一个子模块，可用于创建进程。

```python
# multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={},)
    # group：很少使用
    # target：调用对象，即子进程要执行的任务。这里要注意调用的是方法名（如 function）还是方法的返回结果（如 function()）
    # name：为这个 Process 起个名字。
    # args：子进程用到的参数，元组形式。除了字典形式以外的参数，均用元组形式表示，即便只有一个参数
    # kwargs：子进程用到的参数，字典形式。
from multiprocessing import Process

def example_function(example_parameter):
    print('子进程启动')
    print(f'{example_parameter}')
    print('子进程结束')

if __name__ == '__main__': # 保护下面代码不被自动调用，以避免引发无限递归子进程
    print('父进程启动')
    process = Process(target=example_function, args=('example_parameter', )) # 创建子进程
    process.start() # 子进程启动
    process.join() # 阻塞父进程，等子进程结束再让父进程继续往下执行。
    print('父进程结束')
    # .join() 方法可添加参数 timeout ，这样 timeout 秒后，就算子进程不结束父进程也不再等待自行结束。

# 输出：
# 父进程启动
# 子进程启动
# example_parameter
# 子进程结束
# 父进程结束

# （以上代码需要运行才能生效，逐行运行无效）
```

### 相关属性介绍  

multiprocessing.cpu_count()：CPU 核心数量，可用于设置合适的进程数量  
p.pid：进程的 id  
p.name：进程的名称  

### 相关方法介绍  

process.close()：等进程运行完后，温柔地关闭进程
process.terminate()：简单粗暴直接杀死进程

## 2. 进程之间的通信

> 学会创建进程后，我们发现进程之间不能再用变量赋值来进行共享信息。  
> 为此，我们学习进程之间的通信方法。
> 进程之间的通信方法通常由三种：队列、管道、共享内存。其中队列最为常用。  

### 1. 队列

跟数据结构中的队列类似，特点是先进先出，后进后出。

#### 设置队列的长度

```python
from multiprocessing import Queue

# 创建一个长度为 666 的队列 queue
queue = Queue(666)
```

#### 两个基本方法

##### Queue.put(obj, block=True, timeout=None)

把 obj 放进队列。  
实际应用中通常用于写入。  

##### Queue.get(block=True, timeout=None)

取出元素，由于队列的特性，取出元素时就不需要 obj 参数了。  
实际应用中通常用于读取。  

> block：默认为True，如果队列满了会阻塞等待；如果设置为 False，会在队列满了的时候直接报错。  
> timeout：设置阻塞等待时间，如果等了 timeout 秒，队列还是满的话，报错。

#### 在进程中实现通信

```python
from multiprocessing import Process, Queue

def task(q):
    q.put('obj')

if __name__ == '__main__':
    queue = Queue() # 在父进程中创建队列 queue
    process = Process(target=task, args=(queue,)) # 创建子进程，并把 queue 传给子进程
    process.start() # 在子进程完成 put 操作
    print(queue.get()) # 在父进程完成 get 操作
    process.join()

# 输出：
# obj
```

### 2. 管道

管道是比队列更底层的实现方法，因为更底层，直接用于通信会比队列出现更多问题。  
所以了解一下就行了，一般不用的。  
管道与队列最大的不同在于管道有两个口，一个口进，另一个口出，不能在一个口又进又出。  

```python
from multiprocessing import Process, Pipe

def task(q):
    q.send('obj') # 相当于 Queue.put()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe() # 管道比队列多了一个口，因此多定义一个 Pipe()
    process = Process(target=task, args=(child_conn,))
    process.start()
    print(parent_conn.recv()) # 相当于 Queue.get()
    process.join()

# 输出：
# obj
```

### 3.共享内存

共享内存因为针对具体数据类型，效率会比队列更高一些，可使用 Value 或 Array 模块。  
尽管效率更高，但是适用的数据类型比队列少。  

```python
from multiprocessing import Process, Value

def task(n):
    n.value = 3.1415

if __name__ == '__main__':
    val = Value('d', 0.0) # 创建一个类型为 'd'，数值为 0.0 的数值 val
    process = Process(target=task, args=(val,))
    process.start() # 在子进程中将 value 赋值
    process.join()

    print() # value 在父进程中也发生了变化

# 输出：
# 3.1415
```

> 'd' 是 Array 模块使用的类型的 typecode，表示双精度浮点数；  
> 类似还有 'i'，表示符号整数。  

## 3. 进程锁

> 成功实现多进程之间的通信后，出现了新的问题。  
> 如果不同进程同时执行，会因为内存资源抢占而出问题：一开始进程1抢占到了资源，还没执行几行代码，就被进程2把资源抢占走，然后进程2没执行几秒钟又被别的进程抢走。各个进程的代码互相串行，使运行结果与我们的期望不符。  
> 为了解决这个问题，引入了进程锁。
> multiprocessing 中引入进程锁的模块为 Lock。  

### 不加锁的情况

```python
from multiprocessing import Process, Value
import time

def job(v, num):
    for _ in range(5): # 下划线表示啥也不取，就单纯想重复执行 5 次
        time.sleep(0.1) # 每次执行时暂停 0.1 秒，进程们利用这 0.1 秒疯狂抢夺内存资源
        v.value += num # 将 num 加 5 次

if __name__ == '__main__':
    v = Value('i', 0) # 定义共享变量，初始值为 0
    p1 = Process(target=job, args=(v, 1))
    p2 = Process(target=job, args=(v, 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(v.value) # 理论上输出结果为 20

# 实际输出结果是不确定的
```

### 加锁后

```python
from multiprocessing import Process, Value, Lock
import time

def job(v, num, l):
    l.accquire() # 上锁
    for _ in range(5):
        time.sleep(0.1) # 进程们不能在这 0.1 秒内抢夺资源了
        v.value += num
    l.release() # 解锁

if __name__ == '__main__':
    l = Lock() # 定义一个进程锁
    v = Value('i', 0)
    p1 = Process(target=job, args=(v, 1, l))
    p2 = Process(target=job, args=(v, 3, l))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(v.value)
```

## 4. 进程池

> 当创建了大量进程的时候，很容易超出计算机的承受范围。而且对于每一个进程，都要使用一次 .start(), .join() 等方法，会把我们累死。  
> 于是，进程池模块 Pool 出现了，以用于批量处理子进程。  

```python
from multiprocessing import Pool
import time
import random

def example_function(name):
    print(f'子进程{name}开始')
    time.sleep(random.choice([1, 2, 3])) # 可用于爬虫，利用sleep + random.choice，避免同时向服务器发起请求，从而降低反爬几率
    print(f'子进程{name}结束')

if __name__ == '__main__':
    print('父进程启动')
    pool = Pool(16) # 创建一个容量为 16 的进程池，容量由 CPU 核心数量而定
    for i in range(32):
        pool.apply_async(example_function, args=(i, )) # .apply_async() 异步处理
    pool.close()
    pool.join() # 使用进程池时， .join() 前必须加上 .close() 或 .terminate() 方法，否则会导致死锁
    print('父进程结束')
```

> 与异步处理相对的是同步处理 apply()，相当于让一个进程结束后在开启下一个进程。  
> 同步处理一般不使用，因为会失去进程池的意义。  

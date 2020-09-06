'''
输出格式：
output[i] = [a, b, c] (3 个整数)

a 哲学家编号；
b 指定叉子：{0：没叉，1：左叉， 2：右叉}；
c 指定行为：{1：拿起，2：放下，3：吃面}。

实现思路：
规定偶数编号的哲学家不能同时吃饭
'''


from threading import Lock, Thread
import time


class DiningPhilosophers(Thread):

    eatNum = 0

    def __init__(self, Pid, limitNum, forks, logs):
        super().__init__()
        self.Pid = Pid
        self.limitNum = limitNum
        self.forks = forks
        self.logs = logs

    def run(self):
        while self.eatNum < self.limitNum:
            self.wantsToEat()

    def wantsToEat(self):
        right_fork = self.Pid
        left_fork = (self.Pid + 1) % 5

        if self.Pid % 2 == 0:
            self.forks[right_fork].acquire()
            self.forks[left_fork].acquire()
        else:
            self.forks[left_fork].acquire()
            self.forks[right_fork].acquire()

        self.pickRightFork()
        self.pickLeftFork()
        self.eat()
        self.putLeftFork()
        self.putRightFork()

        if self.Pid % 2 == 0:
            self.forks[left_fork].release()
            self.forks[right_fork].release()
        else:
            self.forks[right_fork].release()
            self.forks[left_fork].release()

    def pickLeftFork(self):
        self.logs.append([self.Pid, 1, 1])

    def pickRightFork(self):
        self.logs.append([self.Pid, 2, 1])

    def eat(self):
        time.sleep(1)
        self.logs.append([self.Pid, 0, 3])
        self.eatNum += 1

    def putLeftFork(self):
        self.logs.append([self.Pid, 1, 2])

    def putRightFork(self):
        self.logs.append([self.Pid, 2, 2])


if __name__ == "__main__":

    limitNum = int(input('输入进餐次数：'))
    forks = [Lock() for _ in range(5)]
    logs = []

    threads = [DiningPhilosophers(i, limitNum, forks, logs) for i in range(5)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(logs)

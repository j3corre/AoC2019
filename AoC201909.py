from threading import Thread
from time import time
from itertools import permutations
import pandas as pd
import numpy as np

dprg = pd.read_csv("aoc09.csv", header=None)
dprg = dprg.values.tolist()[0]

dprg = dprg + list(np.zeros(10 * len(dprg),dtype = int))

class Machine(Thread):
    def __init__(self, name, prog, inputs):
        Thread.__init__(self)
        self.name = name
        self.prg = prog
        self.inputs = inputs
        self.talkto = None
        self.index = 0
        self.lastoutput = 0
        self.relbase = 0

    def settalkto(self, vm):
        self.talkto = vm

    def getinput(self):
        while len(self.inputs) < 1:
            pass
        return self.inputs.pop(0)

    def pushinput(self, inputval):
        self.inputs.append(inputval)

    def opp(self, ix):
        a, b, c, op = [0, 0, 0, 0]
        if self.prg[ix] > 99:
            a = int(self.prg[ix] / 10000)
            b = int((self.prg[ix] - 10000 * a) / 1000)
            c = int((self.prg[ix] - 10000 * a - 1000 * b) / 100)
        op = self.prg[ix] % 100

        if op == 1:
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3] + self.relbase if a == 2 else self.prg[ix + 3]
            self.prg[ci] = self.prg[ai] + self.prg[bi]
            return 4
        elif op == 2:
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3] + self.relbase if a == 2 else self.prg[ix + 3]
            self.prg[ci] = self.prg[ai] * self.prg[bi]
            return 4
        elif op == 3:
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            # val = input("Your input: ")
            self.prg[ai] = self.getinput()
            return 2
        elif op == 4:
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            self.lastoutput = self.prg[ai]
            # print(self.name + " -> " + str(self.lastoutput))
            # self.talkto.pushinput(self.prg[ai])
            print(self.prg[ai])
            return 2
        elif op == 5:  # jump if true
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            return self.prg[bi] - ix if self.prg[ai] != 0 else 3
        elif op == 6:  # jump if false
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            return self.prg[bi] - ix if self.prg[ai] == 0 else 3
        elif op == 7:  # less than
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3] + self.relbase if a == 2 else self.prg[ix + 3]
            self.prg[ci] = 1 if self.prg[ai] < self.prg[bi] else 0
            return 4
        elif op == 8:  # equal
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2] + self.relbase if b == 2 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3] + self.relbase if a == 2 else self.prg[ix + 3]
            self.prg[ci] = 1 if self.prg[ai] == self.prg[bi] else 0
            return 4
        elif op == 9:  # set relative base
            ai = ix + 1 if c == 1 else self.prg[ix + 1] + self.relbase if c == 2 else self.prg[ix + 1]
            self.relbase += self.prg[ai]
            return 2
        elif op == 99:
            return 0
        return -1

    def run(self):
        step = self.opp(self.index)
        while step != 0:
            self.index += step
            step = self.opp(self.index)


def runworkers(params):
    res = []
    for runno in range(len(params)):
        print('Run No. ' + str(runno + 1), end=': ')
        print(params[runno], end='  =>  ')
        m = [Machine("VM" + str(i), dprg.copy(), [params[runno][i]]) for i in range(5)]

        for i in range(5):
            m[i].settalkto(m[(i + 1) % 5])

        m[0].pushinput(0)

        for i in range(5):
            # m[i].daemon = True
            m[i].start()

        while any([m[i].isAlive() for i in range(5)]):
            pass

        print(m[4].lastoutput)
        res.append(m[4].lastoutput)
        m = [None for i in range(5)]

    res.sort(reverse=True)

    print("The best result is " + str(res[0]))

def main2():
    global dprg
    dprg = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]

    runworkers([[9, 8, 7, 6, 5]])

    dprg = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    runworkers([[9, 7, 8, 5, 6]])

def main():
    ts = time()

    m = Machine("VM0", dprg.copy(), [1])
    m.run()

    m = Machine("VM0", dprg.copy(), [2])
    m.run()

    print('Took %s', time() - ts)


if __name__ == '__main__':
    main()
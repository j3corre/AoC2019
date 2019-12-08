from threading import Thread
from time import time
from itertools import permutations
import pandas as pd

dprg = pd.read_csv("aoc07.csv", header=None)
dprg = dprg.values.tolist()[0]

# dprg = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

class Machine(Thread):
    def __init__(self, name, prog, inputs):
        Thread.__init__(self)
        self.name = name
        self.prg = prog
        self.inputs = inputs
        self.talkto = None
        self.index = 0
        self.lastoutput = 0

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
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3]
            self.prg[ci] = self.prg[ai] + self.prg[bi]
            return 4
        elif op == 2:
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3]
            self.prg[ci] = self.prg[ai] * self.prg[bi]
            return 4
        elif op == 3:
            ai = ix + 1 if a == 1 else self.prg[ix + 1]
            # val = input("Your input: ")
            self.prg[ai] = self.getinput()
            return 2
        elif op == 4:
            ai = ix + 1 if a == 1 else self.prg[ix + 1]
            self.lastoutput = self.prg[ai]
            self.talkto.pushinput(self.prg[ai])
            return 2
        elif op == 5:  # jump if true
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            return self.prg[bi] - ix if self.prg[ai] != 0 else 3
        elif op == 6:  # jump if false
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            return self.prg[bi] - ix if self.prg[ai] == 0 else 3
        elif op == 7:  # less than
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3]
            self.prg[ci] = 1 if self.prg[ai] < self.prg[bi] else 0
            return 4
        elif op == 8:  # equal
            ai = ix + 1 if c == 1 else self.prg[ix + 1]
            bi = ix + 2 if b == 1 else self.prg[ix + 2]
            ci = ix + 3 if a == 1 else self.prg[ix + 3]
            self.prg[ci] = 1 if self.prg[ai] == self.prg[bi] else 0
            return 4
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


def main():
    ts = time()

    param = list(permutations(range(0, 5)))
    runworkers(param)

    print('Took %s', time() - ts)

    ts = time()

    param = list(permutations(range(5, 10)))
    runworkers(param)

    print('Took %s', time() - ts)


if __name__ == '__main__':
    main()
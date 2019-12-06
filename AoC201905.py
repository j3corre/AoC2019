import pandas as pd

data = pd.read_csv("Inputs/aoc05.csv", header=None)
data = data.values.tolist()[0]


def opp(ix):
    a, b, c, op = [0, 0, 0, 0]
    if data[ix] > 99:
        a = int(data[ix] / 10000)
        b = int((data[ix] - 10000 * a) / 1000)
        c = int((data[ix] - 10000 * a - 1000 * b) / 100)
    op = data[ix] % 100
    # print(data[ix], ix, op, a, b, c)
    if op == 1:
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        c = ix + 3 if a == 1 else data[ix + 3]
        data[c] = data[a] + data[b]
        return 4
    elif op == 2:
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        c = ix + 3 if a == 1 else data[ix + 3]
        data[c] = data[a] * data[b]
        return 4
    elif op == 3:
        a = ix + 1 if a == 1 else data[ix + 1]
        val = input("Your input: ")
        data[a] = int(val)
        return 2
    elif op == 4:
        a = ix + 1 if a == 1 else data[ix + 1]
        print("Output is: " + str(data[a]))
        return 2
    elif op == 5:  # jump if true
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        if data[a] != 0:
            return data[b] - ix
        else:
            return 3
    elif op == 6:  # jump if false
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        if data[a] == 0:
            return data[b] - ix
        else:
            return 3
    elif op == 7:  # less than
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        c = ix + 3 if a == 1 else data[ix + 3]
        if data[a] < data[b]:
            data[c] = 1
        else:
            data[c] = 0
        return 4
    elif op == 8:  # equal
        a = ix + 1 if c == 1 else data[ix + 1]
        b = ix + 2 if b == 1 else data[ix + 2]
        c = ix + 3 if a == 1 else data[ix + 3]
        if data[a] == data[b]:
            data[c] = 1
        else:
            data[c] = 0
        return 4
    elif op == 99:
        return 0
    return 0


def worker():
    index = 0
    step = opp(index)
    while step > 0:
        index += step
        step = opp(index)


worker()

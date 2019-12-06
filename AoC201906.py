import time
import pandas as pd

start = time.process_time()

data = pd.read_csv("aoc06.csv", header=None)
data = data.values.tolist()

links, dest = [[], []]

for link in data:
    hlp = link[0].split(')')

    links.append(hlp)
    dest.append(hlp[0])


def orb(a):
    b = [x[0] for x in links if x[1] == a]
    if len(b) == 1:
        return b[0]
    return 'STOP'


def countorbits():
    cnt = 0
    for x in dest:
        res = orb(x)
        cnt += 1
        while res != 'STOP':
            res = orb(res)
            if res != 'STOP':
                cnt += 1
    print("Total number of orbits is " + str(cnt) + ".")


countorbits()


def getpath(node1, node2):
    res = orb(node1)
    pth = [[res, node1]]
    while res != node2:
        hlp = orb(res)
        pth.append([hlp, res])
        res = hlp
    return pth


def findparent(node1, node2):
    p1 = getpath(node1, 'COM')
    p2 = getpath(node2, 'COM')
    for a in p1:
        for b in p2:
            if a[0] == b[0]:
                break
        if a[0] == b[0]:
            break
    return a[0]


parentnode = findparent('YOU', 'SAN')
ys1 = getpath('YOU', parentnode)
ys2 = getpath('SAN', parentnode)

print("Distance from YOU to SAN is " + str(len(ys1) + len(ys2) - 2) + ".")

elapsed_time = time.process_time() - start

print("Elapsed time: " + str(elapsed_time) + " seconds.")

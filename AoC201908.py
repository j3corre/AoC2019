fin = open("aoc08.txt")

img = []

while True:
    line = fin.read(150)
    if len(line) > 0:
        img.append(line)
    else:
        break


def cntchr(line, chr):
    return len(line) - len(line.replace(chr, ''))


img = img[0:len(img) - 1]

nul = [[cntchr(img[i], '0'), i] for i in range(len(img))]

nul.sort()

print(cntchr(img[nul[0][1]], '1') * cntchr(img[nul[0][1]], '2'))


def replace(orig, char, position):
    return orig[0:position] + char + orig[position + 1:]


def mergeimg(full, added):
    res = full
    for i in range(len(full)):
        if added[i] != '2':
            res = replace(res, added[i], i)
    return res


resimg = img[99]

for i in range(99):
    resimg = mergeimg(resimg, img[99 - i - 1])

for i in range(6):
    print(resimg[25 * i:25 * (i + 1)])

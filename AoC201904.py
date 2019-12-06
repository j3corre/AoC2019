min = 138241
max = 674034
code = '000000'


def ch(c, i, j):
    c = c[:i] + str(j) + c[i + 1:]
    return c


def test(c):
    for i in range(0, 10):
        a = c.replace(str(i), '')
        if (len(a) == 4) & (len(a) < 6):
            return True
    return False


i = 0
for a in range(1, 7):
    code = ch(code, 0, a)
    for b in range(a, 10):
        code = ch(code, 1, b)
        for c in range(b, 10):
            code = ch(code, 2, c)
            for d in range(c, 10):
                code = ch(code, 3, d)
                for e in range(d, 10):
                    code = ch(code, 4, e)
                    for f in range(e, 10):
                        if (a != b) & (b != c) & (c != d) & (d != e) & (e != f):
                            break
                        if (int(code) < min) | (int(code) > max):
                            break
                        code = ch(code, 5, f)
                        i += 1
print(i)

i = 0
for a in range(1, 7):
    code = ch(code, 0, a)
    for b in range(a, 10):
        code = ch(code, 1, b)
        for c in range(b, 10):
            code = ch(code, 2, c)
            for d in range(c, 10):
                code = ch(code, 3, d)
                for e in range(d, 10):
                    code = ch(code, 4, e)
                    for f in range(e, 10):
                        code = ch(code, 5, f)
                        if (a != b) & (b != c) & (c != d) & (d != e) & (e != f):
                            break
                        if (int(code) < min) | (int(code) > max):
                            break
                        if test(code):
                            # print(code)
                            i += 1
print(i)

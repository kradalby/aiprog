from functools import reduce

def reduceLineLeft(xs): 
    def aux(acc, y):
        if len(acc) == 0: acc.append(y)
        elif acc[len(acc)-1] == y:
            acc[len(acc)-1] = y * 2
            acc.append(0)
        else: acc.append(y)
        return acc
    res = [x for x in reduce(aux, [x for x in xs if x!=0], []) if x!=0]
    res.extend([0 for i in range(0, len(xs)-len(res))])
    return res

def reduceLineRight(xs):
    return reduceLineLeft(xs[::-1])[::-1]

def reduceLeft(a):
    return list(map(reduceLineLeft, a))

def reduceRight(a):
    return list(map(reduceLineRight, a))

def reduceUp(a):
    return rotate(reduceLeft(rotate(a)))

def reduceDown(a):
    return rotate(reduceRight(rotate(a)))

def rotate(a):
    def auxset(i, j): b[j][i] = a[i][j]
    b = newEmpty(len(a))
    list(map(lambda i: [auxset(i, j) for j in range(0, len(a[i]))], list(range(0, len(a)))))
    return b

def newEmpty(size):
    return [[0 for i in range(0, size)] for i in range(0, size)]

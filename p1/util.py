from itertools import product
import copy

def make_function(variables, expression, envir=globals()):
    function = '(lambda ' + ','.join(variables) + ': ' + expression + ')'
    print(function)
    return eval(function, envir)

def generate_permutations(counts, length):
    if len(counts) == 0:
        row = []
        for x in range(length):
            row.append(0)
        return [row]

    permutations = []

    for start in range(length - counts[0] + 1):
        permutation = []
        for x in range(start):
            permutation.append(0)
        for x in range(start, start + counts[0]):
            permutation.append(1)
        x = start + counts[0]
        if x < length:
            permutation.append(0)
            x += 1
        if x == length and len(counts) == 0:
            permutations.append(permutation)
            break
        sub_start = x
        sub_rows = get_permutations(counts[1:len(counts)], length - sub_start)
        for sub_row in sub_rows:
            sub_permutation = copy.deepcopy(permutation)
            for x in range(sub_start, length):
                sub_permutation.append(sub_row[x-sub_start])
            permutations.append(sub_permutation)
    return permutations



def make_function(variables, expression, envir=globals()):
    function = '(lambda ' + ','.join(variables) + ': ' + expression + ')'
    print(function)
    return eval(function, envir)

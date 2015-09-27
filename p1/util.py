

def make_function(variables, expression, envir=globals()):
    return eval('(lambda ' + ','.join(variables)[:1] + ': ' + expression + ')', envir)

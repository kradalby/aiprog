

#def make_function(variables, expression, envir=globals()):
#    function = '(lambda ' + ','.join(variables) + ': ' + expression + ')'
#    print(function)
#    return eval(function, envir)


def make_function(self, varNames, expression, envir=globals()):
    args = ""
    for n in varNames: args = args + "," + n
    return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

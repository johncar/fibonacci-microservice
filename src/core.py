# here is the meat

# a simple task
def fibonacci(n):
    a, b = 1, 1
    for i in xrange(n - 1):
        a, b = b, a + b

    return a

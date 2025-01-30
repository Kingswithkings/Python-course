# The number(Factorial) of 5! is 5*4*3*2*1

def iterativeFactorial(n):
    result = 1
    for i in range(n, 0, -1):
        result = result * i
    return result

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))
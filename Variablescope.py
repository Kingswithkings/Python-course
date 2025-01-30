# Scope is the place where a variable exist
# There are two types of scope 1. global, 2. local

x = 10
def function():
    global x
    x = 20

function()
print(x)
class A:
    def method1(self):
        print('method 1')

    def method2(self):
        print('method 2')

class B(A):
    def __init__(self):
        super().__init__()
        print('b')

    def method3(self):
        print('method 3')

    def method4(self):
        print('method 4')

class C(B):  
# No need to inherit from A again because B already extends A
    def __init__(self):
        super().__init__()
        print('c')

    def method5(self):
        print('method 5')

# Creating instances
a = A()
b = B()
c = C()

# Calling methods
b.method1()
b.method2()  
b.method3()
b.method4()
c.method5()

# Functions are reusable type of code you can call
def myFunction():
    print('This is our function')

myFunction()





def betterPrint(string):
        for char in string:
            print(char)

betterPrint('hello')


def betterPrint(string = 'you have not set a parameter'):
        for char in string:
            print(char)

betterPrint()
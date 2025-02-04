
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error! Division by zero."
    return a / b



def  calculator():
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == '+':
        result = add(num1, num2)
    elif operator == '_':
        result = subtract(num1, num2)
    elif operator == '*':
        result = multiply(num1, num2)
    elif operator == '/':
        result = divide(num1, num2)
    else:
        result = "Invalid operator!"

        print("Result:", result)

    if __name__ == "__main__":
        calculator     


def calculator():
    try:
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, _, *, /): ")
        num2 = float(input("Enter second number: "))

        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)

        else:
            result = "Error! Invalid number input."

    except ValueError:
        result = "Error! Invalid number input."

        print("Result:", result)

if __name__ == "__main__":
    calculator()
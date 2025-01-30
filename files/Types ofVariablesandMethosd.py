class Employee:

    company = 'learn2code'

    def __init__(self, name, age, salary, gender):
        self.name = name
        self.age = age
        self.salary = salary
        self.gender = gender
        self.email = self.generateEmail()

    def generateEmail(self):
        return f'{self.name.lower()}@{Employee.company}.com'
    
    def showInfo(self):
        print(self.name, self.age, self.salary, self.gender, self.email)

    @classmethod
    def changeCompanyName(cls, newName):
        cls.company = newName

    @staticmethod
    def info():
        print('This is a class for creating employee objects. It requires parameters: name, age, salary, gender.')


# Creating an Employee object
obj = Employee('Kings', 34, '£30,000', 'M')

# Calling the static method correctly
Employee.info()

# Showing Employee info
obj.showInfo()

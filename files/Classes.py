# Object oriented program
class Employee:

    def __init__(self, name, age, salary, gender):
        self.name = name
        self.age = age
        self.salary = salary
        self.gender = gender
        self.email = self.generateEmail()

    def generateEmail(self):
        return f'{self.name}@company.com'
    
    def showInfo(self):
        print(self.name, self.age, self.salary, self.gender, self.email)

obj = Employee('Kings', '34', '£30,000', 'M',)

print(obj)

obj.showInfo()


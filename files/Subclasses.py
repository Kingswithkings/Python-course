class Employee:

    company = 'learn2code'

    def __init__(self, name, age, salary, gender, desig, dept, responsibility, cpu, gpu, ram):
        self.name = name
        self.age = age
        self.salary = salary
        self.gender = gender
        self.email = self.generateEmail()
        self.job = self.Job(desig, dept, responsibility)  # Creating an instance of Job
        self.computer = self.Computer(cpu, gpu, ram)  # Creating an instance of Computer

    def generateEmail(self):
        return f'{self.name.lower()}@{Employee.company}.com'
    
    def showInfo(self):
        print(self.name, self.age, self.salary, self.gender, self.email)

    @classmethod
    def changeCompanyName(cls, newName):
        cls.company = newName

    @staticmethod
    def info():
        print('This is a class for creating employee objects.')

    # Moving Job and Computer classes inside Employee but outside any method
    class Job:
        def __init__(self, designation, department, responsibility):
            self.designation = designation
            self.responsibility = responsibility
            self.department = department

        def showInfo(self):
            print(self.designation, self.department, self.responsibility)

    class Computer:
        def __init__(self, cpu, gpu, ram):
            self.cpu = cpu
            self.gpu = gpu
            self.ram = ram

        def showInfo(self):
            print(self.cpu, self.gpu, self.ram)


# Creating an Employee Object
obj = Employee('Kings', 34, '£30,000', 'M', 'Manager', 'IT', 'Servers', 'i7', 'gtx1016', '32GB')

# Calling showInfo for all objects
obj.showInfo()          # Prints Employee details
obj.job.showInfo()      # Prints Job details
obj.computer.showInfo() # Prints Computer details

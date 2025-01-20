#operators for conditional statements are 
# (==) means equal to
# != means not equal to
# > means greater than
# < means less than

#compare minimum marks to marks of the student
minMarks = 30
studentMarks = float(input('enter your marks: '))

if studentMarks >= minMarks:
    print("you are eligible")
else:
    print("you are not elligible")
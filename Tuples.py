# A list that cannot be edited by the user
tuple1 = (12, 13, 14, 15)
print(tuple1)
print(tuple1[1])

# Convert list into a tuple
list1 = [1, 2, 3, 4, 5]
tuple1 = tuple(list1)
print(tuple1)

tup1 = (1,2,3,5)
l1 = list(tup1)
l1[3] = 4
tup1 = tuple(l1)
print(tup1)
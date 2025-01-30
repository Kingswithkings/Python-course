myList = [1,2,3,4,5,6,7,8,9]
print (myList)

fruits = [
    'apple', # 0
    'bannana', # 1
    'pear', # 2
    'strawberries' # 3
]

print (fruits[1])

characters = ['a', 'b', 'd', 'd']
print(characters)
characters[2] = 'c'
print(characters)
# append is to add a character
characters.append('e')
print(characters)
# remove to delete a character
characters.remove('e')
print(characters)
# pop to display 
characters.pop(3)
print(characters)
# sort arrange
characters.sort
print(characters)
# reverse
characters.reverse
print(characters)


# bubble sort
kings = [8,3,1,4]

length = len(kings)
for i in range(length):
    for j in range(0, length-i-1):
        if kings[j] > kings[j+1]:
            kings[j], kings[j+1] = kings[j+1], kings[j]

            print(kings)
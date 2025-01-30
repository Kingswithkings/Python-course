# FilesHandling
# .txt files (w or w+ stands for write, a or a+ stands for add, r stands for read)


# Read files
with open('files/data.txt', 'r') as file:
    data = file.read()
    print(data)

# Write files
userInput = input('Enter your message you wish to save')

#with open('files/data.txt', 'w') as file:
with open('files/data.txt', 'a') as file:
    file.write(userInput + '\n')


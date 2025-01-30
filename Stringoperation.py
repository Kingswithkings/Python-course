string = 'string'
string.islower()
True

string = 'String'
string.islower()
False

string = 'STRING'
string.isupper
True

string = 'STRING'

string.lower()
'string'

string.upper()
'STRING'

# NUMERIC OPERATION ON STRING 
string = '29'
string.isdigit()
True

# REPLACE
string.replace('2', 'Hello')

# Split
string.split('o'), ['29']
string = string.replace('2', 'Hello')
string.split('o')
['Hell', '9']
string
'Hello9'

'e' in string
True

'{' in string
False

'2' in string
False

f'Hello my name is Kings'

# example 
a = 'ABC123DEF456'

def answer(string):
    alphabets = ''
    result = 0
    for char in string:
        if char.isdigit():
            result += int(char)
        else:
            alphabets += char
    return (alphabets, result)
        
print(answer(a))


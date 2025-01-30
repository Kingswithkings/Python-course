# Pickle has load dump (load is used to read and dump is used to write)

import pickle


# phonebook = {
#     'a' : '1',
#     'b' : '2',
#     'c' : '3'
# }

# with open('files/phonebook.dat', 'wb') as bin:
#     pickle.dump(phonebook, bin)

with open('files/phonebook.dat', 'rb') as bin:
    data = pickle.load(bin)
    print(data)
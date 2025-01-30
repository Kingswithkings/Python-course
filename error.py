#try: 
 #   a = int(input('~'))
#except Exception as error:
 #   print('User Error', 'error : ' + str(error))

try: 
    print('opened')
    a = int(input('~'))
except ValueError:
    print('invalid user input')
except TypeError:
    print('type error')
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    print('closed')
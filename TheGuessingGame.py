import random

score = 10
randomNumber = random.randint(1,10)

while True:
    userNumberInput = int(input('Guess : '))

    if userNumberInput == randomNumber:
        print("congratulations you guessed it right! your score is " + str(score))
        #break
    else:
        print('better luck next time')
        score -= 1
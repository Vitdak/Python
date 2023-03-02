import random

def guessing_game(range):
    random_number = random.randint(1, range)
    guess = 0
    while guess != random_number:
        while True:
            try:
                guess = int(input(f'Enter a number between 1 and {range}: '))
                if guess < random_number:
                    print('Try harder, number is higher')
                elif guess > random_number:
                    print('Try even harder, number is lower')
                break
            except ValueError:
                print('Ooopsy, that is not a number, try again :)')

    print('Congrats, You guessed the number !!!')

guessing_game(100)

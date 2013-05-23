# Rock-paper-scissors-lizard-Spock template

import random


def number_to_name(number):
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        print 'the name is incorrect'
    return name
    
def name_to_number(name):
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3
    elif name == 'scissors':
        number = 4
    else:
        print 'the name is incorrect'
    return number


def rpsls(name): 

    player_number = name_to_number(name)

    comp_number = random.randrange(0,5)

    diff = (player_number - comp_number) % 5

    if diff > 2:
        result = "Computer wins!"
    elif diff == 0:
        result = "Player and computer tie!"
    else:
        result = "Player wins!"
        
    player_guess = name
    computer_guess = number_to_name(comp_number)

    print ''
    print 'Player chooses', player_guess
    print 'Computer chooses', computer_guess
    print result
    
# test the code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")




# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors


import random

# helper functions

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
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # compute difference of player_number and comp_number modulo five
    diff = (player_number - comp_number) % 5
    # use if/elif/else to determine winner
    if diff > 2:
        result = "Computer wins!"
    elif diff == 0:
        result = "Player and computer tie!"
    else:
        result = "Player wins!"
    # convert comp_number to name using number_to_name
    player_guess = name
    computer_guess = number_to_name(comp_number)
    # print results
    print ''
    print 'Player chooses', player_guess
    print 'Computer chooses', computer_guess
    print result
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


#http://www.codeskulptor.org/#user10_pwlMEeVFcjsjB1h.py

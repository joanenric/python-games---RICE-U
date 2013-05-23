
import random
import math
import simplegui


range_max = 100
max_turns = math.ceil(math.log(range_max+1,2))

def init():
    global secret_num
    secret_num = random.randrange(0, range_max)
    global turn
    turn = 0
    print ""
    print "New game. the range is from 0 to",range_max
    print "Number of remaining guesses is", max_turns
    print ""

    
def range100():
    global range_max
    range_max = 100
    global max_turns
    max_turns = math.ceil(math.log(range_max+1,2))    
    init()
    
def range1000():
    global range_max
    range_max = 1000
    global max_turns
    max_turns = math.ceil(math.log(range_max+1,2))
    init()
   
def get_input(guess):
    # main game logic 
    global turn
    turn +=1
    guess = float(guess)
    print "Guess was",guess
    print "Number of remaining guesses is", max_turns - turn
    if guess > secret_num and max_turns - turn > 0:
        print "Lower!"
        print ""
    elif guess < secret_num and max_turns - turn > 0:
        print "Higher!"
        print ""
    elif guess == secret_num:
        print "Correct!!"
        init()
    else:
        print "You ran out of guesses. The number was", secret_num
        init()
        
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is (0, 100]", range100, 200)
frame.add_button("Range is (0, 1000]", range1000, 200)
frame.add_input("Enter a guess", get_input, 200)

# start frame
frame.start()
init()


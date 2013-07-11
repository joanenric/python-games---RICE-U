# implementation of card game - Memory

import simplegui
import random

CARD_W = 50
CARD_H = 100
VALUES = range(8)*2

values = []
state = 0
turn = [-1, -2]
count = 0
# helper function to initialize globals
def init():
    global values, state, turn, count
    values = [[str(n), False] for n in VALUES]
    random.shuffle(values)
    state = 0
    turn  = [-1, -2]
    count = 0
    label.set_text("Moves = " + str(count))
     
# define event handlers
def mouseclick(pos):
    global state, turn, values, count
    card_pressed = pos[0] // CARD_W #select the card pressed
    if not values[card_pressed][1]: #if card is flipped
        if state == 0:
            values[card_pressed][1] = True #unflip
            turn[0] = card_pressed #store value
            state = 1 #change state
        elif state == 1:
            values[card_pressed][1] = True #unflip
            turn[1] = card_pressed #store value
            state = 2 #change state
            count += 1 #inc count
        else:
            if values[turn[0]][0] != values[turn[1]][0]: #if different unflipped
                values[turn[0]][1], values[turn[1]][1] = False, False 
            turn = [card_pressed, -2] 
            values[card_pressed][1] = True
            state = 1
    label.set_text("Moves = " + str(count))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    offset = 0
    for value in values:
        if value [1]:
            canvas.draw_text(value[0], (CARD_W//2 + offset - 10, 1.3*CARD_H//2), 50, "Red")
        else:
            canvas.draw_polygon([[offset, 0], [CARD_W + offset, 0], [CARD_W + offset, CARD_H], [offset, CARD_H]], 4, "red", "green")
        offset +=50

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

#http://www.codeskulptor.org/#user14_VXTE6MytW8vnMhI.py
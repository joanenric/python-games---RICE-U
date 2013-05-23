# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH//2, HEIGHT//2]
ball_vel = [0,0]

paddle1_pos = HEIGHT//2
paddle2_pos = HEIGHT//2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
total_score = "0 / 0"



def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH//2, HEIGHT//2]
    hor = random.randrange(120, 240)
    ver = -random.randrange(60, 180)
    if not right:
        hor *=-1
    ball_vel[0] = hor/60
    ball_vel[1] = ver/60

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    ball_init(True)
    paddle1_pos = HEIGHT//2
    paddle2_pos = HEIGHT//2

    
def update_paddle(paddle_pos, vel):
    if paddle_pos + vel >= HALF_PAD_HEIGHT and paddle_pos + vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle_pos += vel
    return paddle_pos
def draw(c):
    global total_score, score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = update_paddle(paddle1_pos, paddle1_vel)
    paddle2_pos = update_paddle(paddle2_pos, paddle2_vel)

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White") 
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White") 
    c.draw_text(str(score1), (WIDTH//2-120, HEIGHT//2 - 100), 50, "Red", "serif")
    c.draw_text(str(score2), (WIDTH//2+100, HEIGHT//2 - 100), 50, "Red", "serif")
    # update ball
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS - 1:
        ball_vel[1] *=-1

    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if abs(ball_pos[1] - paddle1_pos) <= HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            ball_init(True)
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if abs(ball_pos[1] - paddle2_pos) <= HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            ball_init(False)
            
    total_score = str(score1) + " - " + str(score2)    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    
    

    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= acc


    
    
# create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button2 = frame.add_button("Restart", new_game, 50)

# start frame
frame.start()
new_game()


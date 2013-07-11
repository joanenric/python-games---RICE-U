# template for "Stopwatch: The Game"

import simplegui

# define global variables
time = 0
counter_stop = 0
points = 0
is_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def nice_format(n):
    """print the number n in two digits"""
    s = str(n)
    if len(s) < 2:
        s = '0'+s
    return s
       
def format(t):
    minutes = nice_format(t//60000)
    temp = t % 60000
    secs = nice_format(temp//1000)
    de_secs = temp % 1000 // 100
    return minutes+":"+secs+"."+str(de_secs)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global is_running
    is_running= True

def stop():
    global counter_stop, is_running
    timer.stop()
    if is_running:
        is_point()
        counter_stop += 1
        is_running = False

def reset():
    stop()
    global time, counter_stop, points
    time, counter_stop, points = 0, 0, 0
    
    
def is_point():
    global points
    s = format(time)
    if s[-1] == "0":
        points += 1
        return True
    else:
        return False

def result():
    return str(points)+"/"+str(counter_stop)

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time +=100

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), (75, 160), 52, "Red")
    canvas.draw_text(result(), (250, 40), 20, "Green")

    
# create frame
f = simplegui.create_frame("StopWatch", 300, 300)

# register event handlers
f.set_draw_handler(draw_handler)
f.add_button("Start", start, 200)
f.add_button("Stop", stop, 200)
f.add_button("Reset", reset, 200)


timer = simplegui.create_timer(100,tick)

# start frame
f.start()



# http://www.codeskulptor.org/#user12_Aqtn0uQqk2la15t.py
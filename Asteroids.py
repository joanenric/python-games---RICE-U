# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations

def init():
    global my_ship, rock_group, missile_group, started, score, lives, soundtrack
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])
    started = False
    soundtrack.rewind()
    soundtrack.play()
    ship_thrust_sound.pause()

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def key_down(key):
    global my_ship, started
    if started:
        if key == simplegui.KEY_MAP["left"]:
            my_ship.turn(-1) # -1 means counter clockwise
        elif key == simplegui.KEY_MAP["right"]:
            my_ship.turn(1) # 1 means clockwise
        elif key == simplegui.KEY_MAP["up"]:
            ship_thrust_sound.play()
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP["space"]:
            my_ship.shoot()

        
def key_up(key):
    global my_ship, started
    if started:
        if key == simplegui.KEY_MAP["left"]:
            my_ship.turn(1)
        elif key == simplegui.KEY_MAP["right"]:
            my_ship.turn(-1)
        elif key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust(False)
            ship_thrust_sound.rewind()

def create_explosion(element):
    global explosion_group
    a_explosion = Sprite(element.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info)
    explosion_group.add(a_explosion)
    explosion_sound.play()
        
        
def process_sprite_group(group, canvas):
    for element in set(group):
        passed = element.update()
        element.draw(canvas)
        if passed: group.remove(element)
        
def group_collide(group, other_object):
    global explosion_group
    coll_count = 0
    for element in set(group):
        if element.collide(other_object):
            group.remove(element)
            create_explosion(element)
            coll_count += 1
    return coll_count

def group_group_collide(group1, group2):
    coll_count = 0
    for element2 in set(group2):
        hit = group_collide(group1, element2)
        if hit > 0: group2.remove(element2)
        coll_count += hit
    return coll_count
        

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        offset = self.image_size[0] if self.thrust else 0
        canvas.draw_image(ship_image, [self.image_center[0] + offset,
                                       self.image_center[1]], self.image_size,
                                       self.pos, self.image_size, self.angle)
    def get_pos(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # canvas wrap
        self.pos = canvas_wrap(self.pos)

        # friction
        fric = 0.008
        self.vel[0] *= (1 - fric)
        self.vel[1] *= (1 - fric)
        
        # thrust acceleration
        self.angle += self.angle_vel
        fwd_vec = angle_to_vector(self.angle)
 
        if self.thrust:
            thrust_power = 0.08
            self.vel[0] += (thrust_power*fwd_vec[0])
            self.vel[1] += (thrust_power*fwd_vec[1])
    
    def turn(self,orientation):
        self.angle_vel += (orientation * 0.1)
        
    def set_thrust(self, is_thrust):
        self.thrust = is_thrust
        
    def shoot(self):
        global missile_group
        shoot_power = 10
        fwd_vec = angle_to_vector(self.angle)
        cannon_pos = [self.pos[0] + self.radius * fwd_vec[0], self.pos[1] + self.radius * fwd_vec[1]]
        missile_vel = [self.vel[0] + shoot_power * fwd_vec[0], self.vel[1] + shoot_power * fwd_vec[1]]
        a_missile = Sprite([cannon_pos[0], cannon_pos[1]], [missile_vel[0], missile_vel[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            self.image_center[0] = 64 + (128 * self.age)
            
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos = canvas_wrap(self.pos)
        self.angle += self.angle_vel
        self.age += 1
        return self.age >= self.lifespan
            
        
    def get_pos(self):
        return self.pos        
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_pos()) < self.radius + other_object.get_radius()
      
def canvas_wrap(pos):
    if pos[0]< 0 or pos[0] > WIDTH:
        pos[0] = pos[0] % WIDTH
    if pos[1]< 0 or pos[1] > HEIGHT:
        pos[1] = pos[1] % HEIGHT 
    return pos    
    
def draw(canvas):
    global time, score, lives, started, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)

    # draw the group of missiles
    process_sprite_group(missile_group, canvas)
    
    # draw the group of rocks
    process_sprite_group(rock_group, canvas)
    
    # draw explosions
    process_sprite_group(explosion_group, canvas)
    
    # update ship 
    my_ship.update()
    
    # scores and lifes
    pos = 40
    canvas.draw_text("Lives: " + str(lives), (20, pos), 25, "Red")
    canvas.draw_text("Score: " + str(score), (WIDTH - 120, pos), 25, "Red")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    # collisions
    collisions = group_collide(rock_group, my_ship)
    lives -= collisions
    
    rocks_down = group_group_collide(rock_group, missile_group)
    score += rocks_down
    
    #GAME OVER
    if lives <= 0:
        init()
    
    
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    pos_hor = random.randrange(0, WIDTH)
    pos_ver = random.randrange(0, HEIGHT)
    vel_hor = (random.randrange(0,20) - 10) * random.randrange(20, 30) / 200
    vel_ver = (random.randrange(0,20) - 10) * random.randrange(20, 30) / 200
    rot = random.randrange(0, 6)
    ang_vel = random.randrange(10, 60)
    ang_vel *=0.001
    
    is_pos_valid = dist([pos_hor, pos_ver], my_ship.get_pos()) > my_ship.get_radius()*3
    
    if len(rock_group) < 12 and started and is_pos_valid:
        a_rock = Sprite([pos_hor, pos_ver], [vel_hor, vel_ver], rot, ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
soundtrack.play()


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
    
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()


# http://www.codeskulptor.org/#user16_Tve3ygH6vJ3ji0J.py
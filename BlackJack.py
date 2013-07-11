# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand"
result = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        description = "Hand contains"
        for i in self.hand:
            description += (" " + str(i))
        return description

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        self.value = 0
        is_A = False
        for i in self.hand:
            self.value += VALUES[i.get_rank()]
            if i.get_rank() == "A":
                is_A = True
                
        if is_A and self.value + 10 <= 21:
            return self.value + 10
        else:
            return self.value
        print self.value
  
    def draw(self, canvas, pos):
        offset = 0
        for i in self.hand:
            i.draw(canvas, [pos[0] + offset, pos[1]])
            offset += CARD_SIZE[0] + 10
  
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j))

    def shuffle(self):
        # add cards back to deck and shuffle
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        description = "Deck contains:"
        for i in self.deck:
            description += (" "+str(i))
        return description

 
#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, result
    result = ""
    #create deck instance
    deck = Deck()
    deck.shuffle()
    
    #create hands instances
    dealer = Hand()
    player = Hand()
    
    #init hands
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    #print "PLAYER'S",player
    #print "DEALER'S",dealer
    if in_play:
        result = "You Lose"
        outcome = "New Deal?"
        score -=1
    else:
        outcome = "Hit or Stand?"
        
    in_play = True
    

def hit():
    global player, dealer, deck, score, outcome, in_play, result
 
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            result = "You have busted, YOU LOSE"
            outcome = "New deal?"
            in_play = False
            score -= 1
    
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, score, in_play, result
    if in_play:
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            outcome = "New deal?"
            result = "Dealer has busted, You WIN"
            score += 1
        else:
            if dealer.get_value() >= player.get_value():
                result = "You Lose"
                outcome = "New deal?"
                score -= 1
            else:
                result = "You Win"
                outcome = "New deal?"
                score += 1
    in_play = False
                
# draw handler    
def draw(canvas):
    canvas.draw_text(outcome, [100, 500], 20, "white")
    canvas.draw_text(result, [300, 500], 20, "white")
    canvas.draw_text("Blackjack", [220, 40], 40, "white", "serif")
    canvas.draw_text("Score: " + str(score), [400, 90], 20, "red")
    canvas.draw_text("Dealer", [100, 80], 20, "red")
    canvas.draw_text("Player", [100, 280], 20, "red")

#global dealer, player
    dealer.draw(canvas, [100, 100])
    player.draw(canvas, [100, 300])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [101 + CARD_BACK_CENTER[0], 101 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()
deal()

#http://www.codeskulptor.org/#user14_mDLmnJZxfhsenjk.py
import random

suits = ('Hearts', "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two":2, "Three":3, "Four":4, "Five": 5, "Six":6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King":10, "Ace":11}

class Card():
    def __init__(self, suit, rank):
        self.suite = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suite

class Deck():
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def dealOne(self):
        return self.all_cards.pop()

class Player():
    
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.all_cards = []

    def removeOne(self):
        return self.all_cards.pop(0)

    def addCard(self, new_cards):
        if type(new_cards)==type([]):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def __str__ (self):
        return f'Player {self.name} has {len(self.all_cards)} cards'

class Dealer(Player):
    def __init__(self):
        self.all_cards = []

currentDeck = Deck()
currentDeck.shuffle()

player = Player("One", 50)
dealer = Dealer()
playerCards = []
dealerCards=[]

global betAmount
global restart
global gameOn
gameOn = True
betAmount = input("How much would you like to bet?: ")
betAmount = int(betAmount)

def startGame():
    while gameOn:
        player.addCard(currentDeck.dealOne())
        player.addCard(currentDeck.dealOne())
        dealer.addCard(currentDeck.dealOne())
        dealer.addCard(currentDeck.dealOne())
        print(f"You have a {player.all_cards[0]} and a {player.all_cards[1]}. The dealer has a {dealer.all_cards[0]}")

        if (player.all_cards[0].rank) == "Ace":
            aceValue = int(input("Do you want Ace to be worth 1 or 11: "))
            player.all_cards[0].value = aceValue
        elif (player.all_cards[1].rank) == "Ace":
            aceValue = int(input("Do you want Ace to be worth 1 or 11: "))
            player.all_cards[1].value = aceValue

        global playerSum
        playerSum = 0
        for x in range(0, len(player.all_cards)):
            playerSum = player.all_cards[x].value + playerSum

        print(f"Player sum is {playerSum}")
        continueGameVar = True
        break

def restartFunc():
    global restart
    global betAmount
    if restart == "Yes":
        betAmount = input("How much would you like to bet?: ")
        betAmount = int(betAmount)

        if int(betAmount)>player.bankroll:
            payRollCheck = 1
        else:
            payRollCheck = 0

        while payRollCheck == 1:
            print("You cannot bet a number larger than your bankroll. Try again")
            betAmount = input("How much would you like to bet?: ")
            betAmount = int(betAmount)
            if int(betAmount)>player.bankroll:
                payRollCheck = 1
            else:
                payRollCheck = 0
                break
        player.all_cards.clear()
        dealer.all_cards.clear()
        gameOn= True
        continueGameVar = True
        startGame()
    if restart == "No":
        print("Good game")
        gameOn = False
        continueGameVar = False
        exit() 

def continueGameFunc():
    while gameOn:
        while continueGameVar:
            player.addCard(currentDeck.dealOne())
            print(f"You have a {player.all_cards[-1]}.")

            if (player.all_cards[-1].rank) == "Ace":
                aceValue = int(input("Do you want Ace to be worth 1 or 11: "))
                player.all_cards[-1].value = aceValue

            global playerSum
            playerSum = 0
            for x in range(0, len(player.all_cards)):
                playerSum = player.all_cards[x].value + playerSum

            print(f"Player sum is {playerSum}")
            break
        break

def standCheck():
    global dealerSum
    global restart
    global betAmount
    dealerSum = 0
    dealerCheck = 1
    while dealerCheck == 1:
        for x in range(0, len(dealer.all_cards)):
            dealerSum = dealer.all_cards[x].value + dealerSum

        if dealerSum>21:
            ###PLAYER WINS  
            dealerCheck = 0   
            print("You have won.")
            continueGameVar = False
            gameOn = False
            player.bankroll = player.bankroll + betAmount
            restart = input(f"You have {player.bankroll} in your account. Do you want to play again? ")
            restartFunc()     
        if dealerSum>playerSum:
            if dealerSum<21:
                ##DEALER WINS
                dealerCheck = 0   
                print(f"The dealer had {dealerSum}")
                print("You have lost.")
                continueGameVar = False
                gameOn = False
                player.bankroll = player.bankroll + betAmount
                restart = input(f"You have {player.bankroll} in your account. Do you want to play again? ")
                restartFunc()
        if dealerSum<=playerSum:
                dealer.addCard(currentDeck.dealOne())
                print(f"The dealer has picked a {dealer.all_cards[-1]}")

def lostGame():
    print("You have lost")
    player.bankroll = player.bankroll - betAmount
    restart = input(f"You have {player.bankroll} in your account. Do you want to play again? ")
    restartFunc()

def gameCheck():
    global restart
    global betAmount
    while playerSum>=21:
        gameOn = False
        continueGameVar = False
        lostGame()
        # exit()
        break
    else:
        gameOn = True
    while gameOn == True:
        if playerSum == 21:
            print("You have won.")
            continueGameVar = False
            gameOn = False
            player.bankroll = player.bankroll + betAmount
            restart = input(f"You have {player.bankroll} in your account. Do you want to play again? ")
            restartFunc()
            break
        if playerSum>21:
            print("You have lost")
            continueGameVar = False
            gameOn = False
            player.bankroll = player.bankroll - betAmount
            restart = input(f"You have {player.bankroll} in your account. Do you want to play again? ")
            restartFunc()
        if playerSum<21:
            continueGame = input("Do you want to hit or stand: ")
            if continueGame == "Hit":
                continueGameVar = True
                continueGameFunc()
            if continueGame == "Stand":
                #current value of cards - if greater win, else pickup new card
                standCheck()
                gameOn = False
            

if int(betAmount)>player.bankroll:
    payRollCheck = 1
else:
    payRollCheck = 0

while payRollCheck == 1:
    print("You cannot bet a number larger than your bankroll. Try again")
    betAmount = input("How much would you like to bet?: ")
    betAmount = int(betAmount)
    if int(betAmount)>player.bankroll:
        payRollCheck = 1
    else:
        payrollCheck = 0
        break

startGame()
continueGameVar = True
while continueGameVar == True:
    gameCheck()
while continueGameVar == False:
    break
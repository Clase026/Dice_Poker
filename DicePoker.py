__author__ = 'Anthony Clasen'

'''
A game of dice poker

After a beginning wager is agreed on, both players roll 5 dice, and can increase their wagers depending on how confident
they are in their starting hand of dice. Both players then choose dice they don't want to keep in their hand and re-roll
them. Both players' hands are then scored and the pot is awarded to the winner. Hand values are scored as follows:
- 5-of-a-kind: 80. Five dice with the same value, higher dice values break ties.
- 4-of-a-kind: 70. Four dice with the same value, higher dice values in the four-of-a-kind break ties.
- Full house: 60. Three dice of one value, and two of another, higher dice values in the three-of-a-kind break ties.
- 6 High Straight: 50. A Hand of 6-5-4-3-2
- 5 High Straight: 40. A hand of 5-4-3-2-1
- 3-of-a-kind: 30. Three dice with the same value, higher dice values in the three-of-a-kind break ties.
- Two Pairs: 20. Two sets of two dice with the same value. Higher dice values of the higher pair break ties.
- 2-of-a-kind: 10. Two dice with the same value, higher dice values in the two-of-a-kind break ties.
- Nothing: 0. Not meeting the requirements of any other hand. The highest die breaks ties.
'''

import random
import os


def main():
    firstPlayer = Player()
    secondPlayer = Player()
    setPlayerNames(firstPlayer, secondPlayer)
    keepPlaying = True
    while keepPlaying == True:
        pot = wager(False, 0)  # Players bet some initial amount
        # Players roll 5 dice to get their initial hands
        rollFirstHand(firstPlayer, secondPlayer)
        pot = wager(True, pot)  # Player can increase their wager after seeing their first hand
        # Players decide which dice to drop, and keep the rest
        chooseDiceToDrop(firstPlayer)
        chooseDiceToDrop(secondPlayer)
        # Dice that were not kept are re-rolled
        firstPlayer.hand.rollNonKeptDice()
        secondPlayer.hand.rollNonKeptDice()
        # The final hand and its value are displayed
        print(str.format("{0}'s final hand is {1}", firstPlayer.name, firstPlayer.hand.displayHand()))
        print(str.format("{0}'s final hand is {1}", secondPlayer.name, secondPlayer.hand.displayHand()))
        # The winner is determined, and the pot is awarded to them
        determineWinner(firstPlayer, secondPlayer, pot)
        shouldContinue = raw_input('Hit enter to exit, or enter in anything else to continue ')
        os.system('cls')
        if shouldContinue == "":
            keepPlaying = False


def setPlayerNames(firstPlayer, secondPlayer):
    firstPlayer.name = raw_input(str.format("Enter a name for the first player, or hit enter to keep the default: "))
    if firstPlayer.name == "":
        firstPlayer.name = "Player 1"
    secondPlayer.name = raw_input(str.format("Enter a name for the second player, or hit enter to keep the default: "))
    if secondPlayer.name == "":
        secondPlayer.name = "Player 2"

def wager(isRaise, potAmount):
    if isRaise:
        wantToRaise = raw_input("Do you want to raise? (Y/N) ")
        wantToRaise = validateYesNo(wantToRaise)
        if wantToRaise == "Y":
            strRaiseAmount = raw_input("How many chips do you want to raise? ")
            raiseAmount = validateInteger(strRaiseAmount)
            potAmount = potAmount + 2 * raiseAmount
    else:
        strWagerAmount = raw_input("How many chips do you want to wager? ")
        wagerAmount = validateInteger(strWagerAmount)
        potAmount = wagerAmount * 2
        print(str.format('Opponent accepts your wager, pot is at {0} chips', potAmount))
    return potAmount
    #TODO: Add a minimum wager; allow non-raising player to either take the wager or forfeit the round.

def rollFirstHand(firstPlayer, secondPlayer):
    firstPlayer.hand.rollHand()
    print(str.format("{0} rolled: {1}", firstPlayer.name, firstPlayer.hand.displayHand()))
    secondPlayer.hand.rollHand()
    print(str.format("{0} rolled: {1}", secondPlayer.name, secondPlayer.hand.displayHand()))


def chooseDiceToDrop(player):
    choosingDice = True
    while (choosingDice):
        os.system('cls')
        print(str.format('{0}, enter the number corresponding to the die that you want to keep or re-roll and hit enter.'
            ' \n Repeat until you only have the dice you want to keep', player.name))
        i = 1
        for die in player.hand.dice:
            if die.kept == True:
                print(str.format('{0}. {1}  Keep', i, die.value))
            else:
                print(str.format('{0}. {1}  Roll', i, die.value))
            i = i + 1
        print('6. Done choosing')
        strChosenDie = raw_input()
        chosenDie = validateInteger(strChosenDie, 1, 6)
        if chosenDie == i:
            choosingDice = False
            os.system('cls')
        else:
            if player.hand.dice[chosenDie - 1].kept == True:
                player.hand.dice[chosenDie - 1].kept = False
            else:
                player.hand.dice[chosenDie - 1].kept = True


def determineWinner(firstPlayer, secondPlayer, pot):
    firstPlayer.hand.determineHandValue()
    secondPlayer.hand.determineHandValue()
    if firstPlayer.hand.value > secondPlayer.hand.value:
        print(str.format('{0} wins with a {1}, taking {2} chips in victory', firstPlayer.name, firstPlayer.hand.handName, pot))
    elif firstPlayer.hand.value < secondPlayer.hand.value:
        print(str.format('{0} wins with a {1}, taking {2} chips in victory', secondPlayer.name, secondPlayer.hand.handName, pot))
    else:
        print('The round is a draw')


def validateYesNo(stringToValidate):
    Validated = False
    while Validated == False:
        if not (stringToValidate == "Y" or stringToValidate == "N"):
            stringToValidate = raw_input('Please enter "Y" or "N" ')
        else:
            Validated = True
    return stringToValidate


def validateInteger(stringToValidate, minimumValue = 0, maximumValue = 100):
    Validated = False
    SendMessage = False
    while Validated == False:
        if SendMessage:
            stringToValidate = raw_input(str.format('Please enter an integer number between {0} and {1}: ', minimumValue, maximumValue))
        try:
            intToValidate = int(stringToValidate)
        except ValueError:
            SendMessage = True
            continue
        if (intToValidate < minimumValue) or (intToValidate > maximumValue) :
            SendMessage = True
        else:
            Validated = True
    return intToValidate


class Player:
    """One of the people playing dice poker"""

    playerNum = 1

    def __init__(self):
        self.name = 'Player ' + str(Player.playerNum)
        Player.playerNum += 1
        self.hand = Hand()


class Die:
    """A six-sided die"""

    def __init__(self):
        self.value = random.randint(1,6)
        self.kept = True

    def roll(self):
        self.value = random.randint(1,6)


class Hand:
    """A hand of up to five six-sided dice"""

    def __init__(self, dice = None):
        self.dice = []
        self.setStartingHand()


    def setStartingHand(self):
        for num in range(0,5):
            die = Die()
            self.dice.append(die)


    def rollHand(self):
        for die in self.dice:
            die.roll()
            die.kept = True


    def rollNonKeptDice(self):
        for die in self.dice:
            if die.kept == False:
                die.roll()


    def displayHand(self):
        handDisplayString = ''
        for die in self.dice:
            handDisplayString += str(die.value) + " "
        return handDisplayString


    def getDiceValues(self):
        diceValues = []
        for die in self.dice:
            diceValues.append(die.value)
        return diceValues


    def determineHandValue(self):
        score = 0
        diceValues = self.getDiceValues()
        num1s = diceValues.count(1)
        num2s = diceValues.count(2)
        num3s = diceValues.count(3)
        num4s = diceValues.count(4)
        num5s = diceValues.count(5)
        num6s = diceValues.count(6)
        diceOccurrences = [num1s, num2s, num3s, num4s, num5s, num6s]
        # 5 of a kind is the best hand, higher dice numbers break ties
        if 5 in diceOccurrences:
            self.handName = "five of a kind"
            score = 80 + self.breakTies(diceOccurrences, 5)
        # 4 of a kind is the second best hand, higher dice numbers break ties
        elif 4 in diceOccurrences:
            self.handName = "four of a kind"
            score = 70 + self.breakTies(diceOccurrences, 4)
        # full house (3 of one number and 2 of another) is the next best hand)
        # higher 3 of a kinds break ties
        elif (2 in diceOccurrences) and (3 in diceOccurrences):
            self.handName = "full house"
            score = 60 + self.breakTies(diceOccurrences, 3)
        # 6 high straight (2,3,4,5,6) is the next best hand
        elif diceOccurrences == [0, 1, 1, 1, 1, 1]:
            self.handName = "six high straight"
            score = 50
        # 5 high straight (1,2,3,4,5) is the next best hand
        elif diceOccurrences == [1, 1, 1, 1, 1, 0]:
            self.handName = "five high straight"
            score = 40
        # 3 of a kind is the next best hand, the die number of the 3 of a kind breaks ties
        elif 3 in diceOccurrences:
            self.handName = "three of a kind"
            score = 30 + self.breakTies(diceOccurrences, 3)
        # 2 pairs is the next best hand, the die number of the higher pair breaks ties
        elif diceOccurrences.count(2) == 2:
            self.handName = "two pairs"
            score = 20 + self.breakTies(diceOccurrences, 2)
        # 2 of a kind is the next best hand, the die number of the 2 of a kind breaks ties
        elif 2 in diceOccurrences:
            self.handName = "pair"
            score = 10 + self.breakTies(diceOccurrences, 2)
        # If nothing else, the score is determined by the highest die in the hand
        else:
            self.handName = "nothing"
            score = self.breakTies(diceOccurrences, 1)

        self.value = score


    def breakTies(self, diceOccurrences, numOccurrences):
        tieBreakerScore = 0
        if diceOccurrences[5] == numOccurrences:
            tieBreakerScore = 6
        elif diceOccurrences[4] == numOccurrences:
            tieBreakerScore = 5
        elif diceOccurrences[3] == numOccurrences:
            tieBreakerScore = 4
        elif diceOccurrences[2] == numOccurrences:
            tieBreakerScore = 3
        elif diceOccurrences[1] == numOccurrences:
            tieBreakerScore = 2
        else:
            tieBreakerScore = 1
        return tieBreakerScore
    #TODO: Break secondary ties, e.g., 3,3,3,3,2 winning over 3,3,3,3,1. This would also resolve ties between two hands of nothing

main()

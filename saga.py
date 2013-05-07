#!/usr/bin/env python
# saga.py
"""
This program is a simple simulation of the game 'Saga'
by Wolgang Kramer and Horst-Rainer Rosner.

Ian Mahoney 2010, GPL
"""

def sumcards(n):
	"""
	Adds up the total strength of a list of cards.
	
	Returns a single number.
	
	>>> a = [1, 6, 9, 9, 12, 14, 16, 18, 23, 27, 27, 28]
	>>> sumcards(a)
	30
	"""
	a = 0
	for i in n:
		i = i%5
		a += i
	return a

pictures = \
{1:'blue 1',	2:'blue 2',		3:'blue 3',		4:'blue 4',\
6:'green 1',	7:'green 2',	8:'green 3',	9:'green 4',\
11:'yellow 1',	12:'yellow 2',	13:'yellow 3',	14:'yellow 4',\
16:'red 1',		17:'red 2',		18:'red 3',		19:'red 4',\
21:'purple 1',	22:'purple 2',	23:'purple 3',	24:'purple 4',
26:'gold 1',	27:'gold 2',	28:'gold 3',	29:'gold 4'}

tree = [1, 6, 9, 9, 12, 14, 16, 18, 23, 27, 27, 28]
castle = [2, 2, 3, 8, 11, 16, 19, 19, 22, 24, 26, 28]
sword = [1, 3, 7, 9, 12, 12, 13, 18, 21, 26, 29, 29]
cross = [2, 4, 6, 8, 13, 17, 17, 18, 21, 24, 24, 26]
lion = [3, 7, 7, 8, 11, 14, 14, 16, 21, 23, 27, 29]
# missing = [1, 4, 4, 6, 11, 13, 17, 19, 22, 22, 23, 28]

class Player:
	def __init__(self, name, hand):
		"""
		Creates a player with a name and a list of knight cards in hand.
		
		Requires 2 inputs: a string to be the name of the player, and a list of knights.
		
		>>> Player_1 = Player('Joe', tree)
		>>> Player_1.name
		'Joe'
		>>> Player_1.hand
		[1, 6, 9, 9, 12, 14, 16, 18, 23, 27, 27, 28]
		"""
		self.name = name
		self.hand = hand
		self.fame = 0
		self.attacks = {}
	
	def moreFame(self, n):
		self.fame += n
	
	def lessFame(self, n):
		self.fame -= n
	
	def addCard(self, cards):
		self.hand.append(cards)
	
	def showHand(self):
		for i in self.hand:
			print pictures[i]
	
	def startAttack(self, card):
		"""
		Creates an attacking force with the card given.
		
		The key for the attack in self.attacks is the color of the attacker.
		The item is the strength of the attack
		
		>>> self.startAttack(1)
		>>> self.attacks
		{'blue': 1}
		"""
		a = pictures[card]
		b = ' %s' %a[-1]
		c = a.strip(b)
		
		a.attacks[c] = [card%5]
	
	def moreAttack(self, color, card):
		self.attacks[color].append(card)
		
		for kingdom in kingdom_list:
			if (kingdom.color == color) and (kingdom.defense < sumcards(self.attacks[color])):
				kingdom.conquer(self, self.attacks[color])


class Kingdom:
	def __init__(self, color, defenders):
		self.color = color
		self.defenders = defenders
		self.defense = sumcards(defenders)
		self.owner = None
	
	def conquer(self, player, attackers):
		self.owner = player
		self.defenders = attackers
		self.defense = sumcards(attackers)

def setup(basic):
	if basic == True:
		SeaLand = Kingdom('blue', [19, 3])
		ForestLand = Kingdom('green', [2, 8])
		FieldLand = Kingdom('yellow', [28, 11])
		CastleLand = Kingdom('red', [24, 16])
		ShadowLand = Kingdom('purple', [2, 22])
		GoldLand = Kingdom('gold', [19, 26])
	
	kingdom_list = [SeaLand, ForestLand, FieldLand, CastleLand, ShadowLand, GoldLand]

def main():
	setup(True)
	
	


def _test():
	from doctest import testmod
	testmod()
if __name__=="__main__":
	_test()
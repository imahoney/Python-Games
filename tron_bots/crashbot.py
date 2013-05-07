#!/usr/bin/python

"""
A bot which attempts to crash into its opponent.

It isn't very smart about it, though...
"""

import tron, utilities, random

debug = utilities.LogFile("logs/crashbot.txt")

def which_move(board):
	
	my_moves = board.moves()
	
	them_y, them_x = board.them()
	me_y, me_x = board.me()

	if (them_y < me_y) and 1 in my_moves:
		debug.log("They're North of me!")
		return 1
	elif (them_y > me_y) and 3 in my_moves:
		debug.log("They're South of me!")
		return 3
	elif (them_x < me_x) and 4 in my_moves:
		debug.log("They're West of me!")
		return 4
	elif (them_x > me_x) and 2 in my_moves:
		debug.log("They're East of me!")
		return 2
	
	else:
		direction = random.choice(board.moves())
		debug.log("They're in the airvents!!!! Moving %s!!!" % str(direction))
		return direction
		

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
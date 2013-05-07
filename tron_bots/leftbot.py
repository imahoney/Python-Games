#!/usr/bin/python

"""
leftbot.py

Follows along the wall to it's left.

If it does not start next to a wall, it will move one space North,
then spiral outwards following that wall to the left.
"""

import tron, utilities, random

debug = utilities.LogFile("logs/leftbot.txt")

facing = [0]

first_move = [True]

def which_move(board):
	my_moves = board.moves()
	debug.log("moves are " + str(my_moves))
	
	right_side = {1:2, 2:3, 3:4, 4:1}
	left_side = {1:4, 2:1, 3:2, 4:3}
	behind = {1:3, 2:4, 3:1, 4:2}
	
	if first_move[0]:
		"""
		Checks to see whether or not there are any walls next to it,
		then sets its facing to an appropriate direction.
		
		If there isn't a wall next to it, it just faces North
		"""
		first_move[0] = False
		for i in range(1, 5):
			if (i in my_moves) and (left_side[i] not in my_moves):
				facing[0] = i
				break
			else:
				facing[0] = 1
	
	if len(my_moves) == 4:
		facing[0] = 1
		debug.log("4 moves, facing " + str(facing[0]))
		return facing[0]
	
	elif len(my_moves) == 3:
		for i in range(1, 5):
			if i not in my_moves:
				facing[0] = right_side[i]
				debug.log("3 moves, facing " + str(facing[0]))
				return facing[0]

	elif (len(my_moves) == 2):
		if left_side[facing[0]] in my_moves:
			facing[0] = left_side[facing[0]]
		debug.log("2 moves, facing " + str(facing[0]))
		return facing[0]
	
	else:
		facing[0] = random.choice(board.moves())
		debug.log("1 moves, facing " + str(facing[0]))
		return facing[0]
		

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
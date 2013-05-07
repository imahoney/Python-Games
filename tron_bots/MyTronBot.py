#!/usr/bin/python

"""
MyTronBot.py

This is currently just a combination of my two previous bots: crashbot and leftbot.

If the opponent is not within 5 spaces, it behaves like the leftbot.

If the opponent is within 5 spaces, it behaves like the crashbot.
"""

import tron, utilities, random

debug = utilities.LogFile("logs/MyTronBot.txt")

#Preliminary Planning!
#
#1. determine strategy to use
#		in same area as opponent?
#		how far away is opponent?
#		how much space is left where?

#2. use that strategy to determine a move
#		seperate from opponent: try to fill space as efficiently as possible
#		far from opponent: try to divide area
#		near opponent: try to cut him off and force him into smaller area.

#3. make that move
#
# 1 - North
# 2 - East
# 3 - South
# 4 - West

facing = [0]

first_move = [True]

def check_them(them_y, them_x, me_y, me_x):
	if ((them_y - me_y < 6)\
		and (them_y - me_y > -6))\
		and ((them_x - me_x < 6)\
		and (them_x - me_x > -6)):
		
		return "near"
	else:
		return "far"
	

def which_move(board):
	my_moves = board.moves()
	them_y, them_x = board.them()
	me_y, me_x = board.me()
	
	strategy = check_them(them_y, them_x, me_y, me_x)
	#debug.log("----")
	#debug.log("I am at " + str(me_y) + ", " + str(me_x))
	#debug.log("They are at " + str(them_y) + ", " + str(them_x))
	#debug.log("My strategy is " + str(strategy))
	
	if strategy == "far":
		debug.log("moves are " + str(my_moves))
		
		right_side = {1:2, 2:3, 3:4, 4:1}
		left_side = {1:4, 2:1, 3:2, 4:3}
		behind = {1:3, 2:4, 3:1, 4:2}
		
		if first_move[0]:
			for i in range(1, 5):
				if (i in my_moves) and (left_side[i] not in my_moves):
					facing[0] = i
					first_move[0] = False
					break
		
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
	
	elif strategy == "near":
		if (them_y < me_y) and 1 in my_moves:
			debug.log("They're North of me!")
			facing[0] = 1
			return facing[0]
		elif (them_y > me_y) and 3 in my_moves:
			debug.log("They're South of me!")
			facing[0] = 3
			return facing[0]
		elif (them_x < me_x) and 4 in my_moves:
			debug.log("They're West of me!")
			facing[0] = 4
			return facing[0]
		elif (them_x > me_x) and 2 in my_moves:
			debug.log("They're East of me!")
			facing[0] = 2
			return facing[0]
		else:
			direction = random.choice(board.moves())
			debug.log("They're in the airvents!!!! Moving %s!!!" % str(direction))
			facing[0] = direction
			return facing[0]

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
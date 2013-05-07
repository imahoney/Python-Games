#!/usr/bin/python

"""
smartbot.py

This is currently just a combination of my two previous bots: crashbot and leftbot.

If the opponent is not within 5 spaces, it behaves like the leftbot.

If the opponent is within 5 spaces, it behaves like the crashbot.
"""

import tron, utilities, random

from tron import NORTH, EAST, SOUTH, WEST

debug = utilities.LogFile("logs/smartbot.txt")

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

class Status:
	def __init__(self):
		self.facing = 0
		self.first_move = True
		self.last_move = 0
		self.strategy = "far"

# facing = [0]

# first_move = [True]

right_side = {NORTH:EAST, EAST:SOUTH, SOUTH:WEST, WEST:NORTH}
left_side = {NORTH:WEST, EAST:NORTH, SOUTH:EAST, WEST:SOUTH}
behind = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
move_names = {1:"North", 2:"East", 3:"South", 4:"West"}

def go(direction, strategy):
	"""
	Sets the current facing to the given direction, then returns a direction.
	Sends a message to the log appropriate to the current strategy.
	"""
	if status.strategy == "near":
		debug.log("They're %s of me!") % move_names[direction]
	else:
		debug.log("No sign of them yet.  Facing %s.") % move_names[direction]
	
	status.facing = direction
	return status.facing

def check_narrow(moves):
	"""
	Recieves a list of moves, then checks how many moves can be made from each of
	those possible locations.  If only one or fewer moves can be made from that
	location, that move is removed from the list of possible moves.
	
	Returns a revised list of moves.
	"""
	
	new_list = list(moves)
	for move in moves:
		counter = 0
		checking = board.rel(move)
		future_moves = {NORTH:(checking[0], checking[1]-1), EAST:(checking[0]+1, checking[1]),\
						SOUTH:(checking[0], checking[1]+1), WEST:(checking[0]-1, checking[1])}
		#debug.log("checking " + str(move))
		for i in future_moves:
			if board.passable(future_moves[i]):
				counter += 1
		#debug.log("counter = " + str(counter))
		if counter < 2:
			new_list.remove(move)
	return new_list

#def stays_narrow(stuff):
#	if (stuff stays narrow):
#		return True
#	else:
#		return False
		

def check_strat(them_y, them_x, me_y, me_x, status):
	if (abs(them_y - me_y) < 6) and (abs(them_x - me_x) < 6):
		status.strategy = "near"
	else:
		status.strategy = "far"

	return status.strategy
	

def which_move(board):
	my_moves = board.moves()
	them_y, them_x = board.them()
	me_y, me_x = board.me()
	strategy = check_strat(them_y, them_x, me_y, me_x)
	
	#debug.log("all moves are " + str(my_moves))
	if strategy == "far":
		a = check_narrow(my_moves)
		if a:
			my_moves = a
	
	move = get_move(board, my_moves, them_y, them_x, me_y, me_x, strategy)
	return move

def get_move(board, my_moves, them_y, them_x, me_y, me_x, strategy):
	
	#debug.log("----")
	#debug.log("I am at " + str(me_y) + ", " + str(me_x))
	#debug.log("They are at " + str(them_y) + ", " + str(them_x))
	#debug.log("My strategy is " + str(strategy))
	
	if strategy == "far":
		move_list = []
		for i in my_moves:
			move_list.append(move_names[i])
		debug.log("moves are " + str(move_list))
		
		if strategy.first_move:
			for i in [NORTH, EAST, SOUTH, WEST]:
				if (i in my_moves) and (left_side[i] not in my_moves):
					facing[0] = i
					strategy.first_move = False
					break
		
		if len(my_moves) == 4:
			facing[0] = NORTH
			debug.log("4 moves, facing " + move_names[1])
			return facing[0]
		elif len(my_moves) == 3:
			for i in [NORTH, EAST, SOUTH, WEST]:
				if i not in my_moves:
					facing[0] = right_side[i]
					debug.log("3 moves, facing " + move_names[facing[0]])
					return facing[0]
		elif (len(my_moves) == 2):
			if left_side[facing[0]] in my_moves:
				facing[0] = left_side[facing[0]]
			debug.log("2 moves, facing " + move_names[facing[0]])
			return facing[0]
		elif (len(my_moves) == 1):
			facing[0] = my_moves[0]
			debug.log("1 move, facing " + move_names[facing[0]])
			return facing[0]
		else:
			return NORTH
	
	elif strategy == "near":
		if abs(them_y - me_y) >= abs(them_x - me_x):
			if (them_y < me_y) and NORTH in my_moves:
				debug.log("They're North of me!")
				facing[0] = NORTH
				return facing[0]
			elif (them_y > me_y) and SOUTH in my_moves:
				debug.log("They're South of me!")
				facing[0] = SOUTH
				return facing[0]
			elif (them_x < me_x) and WEST in my_moves:
				debug.log("They're West of me!")
				facing[0] = WEST
				return facing[0]
			elif (them_x > me_x) and EAST in my_moves:
				debug.log("They're East of me!")
				facing[0] = EAST
				return facing[0]
			else:
				direction = random.choice(board.moves())
				debug.log("They're in the airvents!!!! Moving %s!!!" % move_names[direction])
				facing[0] = direction
				return facing[0]
		else:
			if (them_x < me_x) and WEST in my_moves:
				debug.log("They're West of me!")
				facing[0] = WEST
				return facing[0]
			elif (them_x > me_x) and EAST in my_moves:
				debug.log("They're East of me!")
				facing[0] = EAST
				return facing[0]
			elif (them_y < me_y) and NORTH in my_moves:
				debug.log("They're North of me!")
				facing[0] = NORTH
				return facing[0]
			elif (them_y > me_y) and SOUTH in my_moves:
				debug.log("They're South of me!")
				facing[0] = SOUTH
				return facing[0]
			else:
				direction = random.choice(board.moves())
				debug.log("They're in the airvents!!!! Moving %s!!!" % move_names[direction])
				facing[0] = direction
				return facing[0]

# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
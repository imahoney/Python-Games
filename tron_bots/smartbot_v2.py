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

right_side = {NORTH:EAST, EAST:SOUTH, SOUTH:WEST, WEST:NORTH}
left_side = {NORTH:WEST, EAST:NORTH, SOUTH:EAST, WEST:SOUTH}
behind = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
move_names = {1:"North", 2:"East", 3:"South", 4:"West"}

class Status:
	def __init__(self):
		self.facing = 0
		self.first_move = True
		self.strategy = "far"

status = Status()

# facing = [0]

# first_move = [True]

def go(direction, strategy):
	"""
	Sets the current facing to the given direction, then returns a direction.
	Sends a message to the log appropriate to the current strategy.
	"""
	if status.strategy == "near":
		debug.log("They're %s of me!" % move_names[direction])
	elif status.strategy == "far":
		debug.log("No sign of them yet.  Facing %s." % move_names[direction])
	else:
		debug.log("They're in the airvents!!!! Moving %s!!!" % move_names[direction])
		
	
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

def check_strat(them_y, them_x, me_y, me_x, status):
	"""
	Adjusts the current strategy based on the distance from the opponent.
	
	Changes status.strategy to "near" if they are within 5 spaces.
	Changes status.strategy to "far" if they aren't.
	
	Notifies the log if the strategy has changed.
	"""
	if (abs(them_y - me_y) < 6) and (abs(them_x - me_x) < 6):
		if status.strategy == "far":
			debug.log("I've spotted them!  Attack mode activated!")
		status.strategy = "near"
	else:
		if status.strategy == "near":
			debug.log("I've lost them.  Changing to sweep pattern.")
		status.strategy = "far"
	

def which_move(board, status):
	my_moves = board.moves()
	them_y, them_x = board.them()
	me_y, me_x = board.me()
	check_strat(them_y, them_x, me_y, me_x, status)
	
	#debug.log("all moves are " + str(my_moves))
	a = check_narrow(my_moves)
	if a:
		my_moves = a
	
	move = get_move(board, my_moves, them_y, them_x, me_y, me_x, status)
	return move

def get_move(board, my_moves, them_y, them_x, me_y, me_x, status):
	
	#debug.log("----")
	#debug.log("I am at " + str(me_y) + ", " + str(me_x))
	#debug.log("They are at " + str(them_y) + ", " + str(them_x))
	#debug.log("My strategy is " + str(strategy))
	
	if len(my_moves) == 0:
		debug.log("I have no moves!  Oh, @#$\%!")
		return NORTH
	
	if status.first_move:
		debug.log("And so it begins...")
		for i in [NORTH, EAST, SOUTH, WEST]:
			if (i in my_moves) and (left_side[i] not in my_moves):
				status.facing = i
				status.first_move = False
				break
	
	if status.strategy == "far":
		move_list = []
		for i in my_moves:
			move_list.append(move_names[i])
		debug.log("Searching... moves are " + str(move_list))
		
		if len(my_moves) == 4:
			return go(NORTH, status.strategy)
		elif len(my_moves) == 3:
			for i in [NORTH, EAST, SOUTH, WEST]:
				if i not in my_moves:
					return go(right_side[i], status.strategy)
		elif (len(my_moves) == 2):
			if left_side[status.facing] in my_moves:
				return go(left_side[status.facing], status.strategy)
			else:
				return go(status.facing, status.strategy)
		elif (len(my_moves) == 1):
			return go(my_moves[0], status.strategy)
		else:
			debug.log("something went wrong... no moves, but moving?")
			return go(NORTH, status.strategy)
	
	elif status.strategy == "near":
		if abs(them_y - me_y) >= abs(them_x - me_x):
			if (them_y < me_y) and NORTH in my_moves:
				return go(NORTH, status.strategy)
			elif (them_y > me_y) and SOUTH in my_moves:
				return go(SOUTH, status.strategy)
			elif (them_x < me_x) and WEST in my_moves:
				return go(WEST, status.strategy)
			elif (them_x > me_x) and EAST in my_moves:
				return go(EAST, status.strategy)
			else:
				direction = random.choice(my_moves)
				return go(direction, "freaking out")
		else:
			if (them_x < me_x) and WEST in my_moves:
				return go(WEST, status.strategy)
			elif (them_x > me_x) and EAST in my_moves:
				return go(EAST, status.strategy)
			elif (them_y < me_y) and NORTH in my_moves:
				return go(NORTH, status.strategy)
			elif (them_y > me_y) and SOUTH in my_moves:
				return go(SOUTH, status.strategy)
			else:
				direction = random.choice(board.moves())
				return go(direction, "freaking out")

# you do not need to modify this part, but I did slightly.
for board in tron.Board.generate():
    tron.move(which_move(board, status))
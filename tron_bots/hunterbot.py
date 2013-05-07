#!/usr/bin/python

"""
hunterbot.py

Occasionally referred to as the "SHOOTEMINTHEHEAD!!!" bot.

This is a bot designed to compete in a tron game.
It requires the use of the tron.py file and the utilities.py file.
Information on how to run a tron game can be found in the tron.py file.

This particular bot employs two main strategies:
	If it is within five spaces of the opponent, it attempts to ram the opponent.
	If it is not within fice spaces of the opponent, it follows the left hand wall.

In addition, it does not enter a tunnel (a corridor which is only one space wide)
unless that tunnel opens up again within three moves.

Ian Mahoney, Marlboro College | GPL | Feb Mar 11, 2010
"""

import tron, utilities, random

from tron import NORTH, EAST, SOUTH, WEST

Logs = False
# ^^^ --> To prevent logs from being recorded, change this to: Logs = False
# To activate them again, change it to: Logs = True

if Logs: debug = utilities.LogFile("logs/hunterbot.txt")

right_side = {NORTH:EAST, EAST:SOUTH, SOUTH:WEST, WEST:NORTH}
left_side = {NORTH:WEST, EAST:NORTH, SOUTH:EAST, WEST:SOUTH}
behind = {NORTH:SOUTH, EAST:WEST, SOUTH:NORTH, WEST:EAST}
move_names = {1:"North", 2:"East", 3:"South", 4:"West"}

class Status:
	"""
	The status class keeps track of information for the bot as it runs.
	
	self.facing is the direction the bot was last facing.
	self.first_move records whether or not this
	"""
	def __init__(self):
		self.facing = 0
		self.first_move = True
		self.strategy = "far"
		self.checking = None
		self.last_checked = None
		self.iterations = 0
		self.turn = 0

status = Status()

# facing = [0]

# first_move = [True]

def go(direction, strategy):
	"""
	Sets the current facing to the given direction, then returns a direction.
	Sends a message to the log appropriate to the current strategy.
	"""
	if Logs:
		if strategy == "near":
			debug.log("They're %s of me!" % move_names[direction])
		elif strategy == "far":
			debug.log("No sign of them yet.  Facing %s." % move_names[direction])
		else:
			debug.log("They're in the airvents!!!! Moving %s!!!" % move_names[direction])
	
	status.facing = direction
	return status.facing

# V1
#def check_narrow(moves):
#	"""
#	Recieves a list of moves, then checks how many moves can be made from each of
#	those possible locations.  If only one or fewer moves can be made from that
#	location, that move is removed from the list of possible moves.
#	
#	Returns a revised list of moves.
#	"""
#	
#	new_list = list(moves)
#	for move in moves:
#		counter = 0
#		checking = board.rel(move)
#		future_moves = {NORTH:(checking[0], checking[1]-1), EAST:(checking[0]+1, checking[1]),\
#						SOUTH:(checking[0], checking[1]+1), WEST:(checking[0]-1, checking[1])}
#		#debug.log("checking " + str(move))
#		for i in future_moves:
#			if board.passable(future_moves[i]):
#				counter += 1
#		#debug.log("counter = " + str(counter))
#		if counter < 2:
#			new_list.remove(move)
#	return new_list

# V2
def check_narrow(moves, status, board):
	"""
	Recieves a list of moves (NORTH, SOUTH, EAST, or WEST) and calls the stays_narrow function
	on each one, then removes from the list any moves which enter a tunnel.
	
	Returns an updated list of the moves.
	"""
	new_list = list(moves)
	for move in moves:
		status.iterations = 0
		if stays_narrow(move, status, board):
			new_list.remove(move)
#	debug.log("The new list is: " + str(new_list))
	return new_list

def stays_narrow(move, status, board):
	"""
	Checks to see if there is a tunnel in the given direction.
	
	Uses the is_narrow function to check if a given tile is in a tunnel.
	If that tile is in a tunnel, it checks the next tile.  Once either the tunnel ends, or four
	tiles have been checked, it returns the results.
	
	Returns True if the given direction is a tunnel.
	Returns False if the given direction does not remain a tunnel.
	"""
	move = board.rel(move)
	while is_narrow(move, status, board) and status.iterations <= 30:
		status.iterations += 1
		move = status.checking
	if is_narrow(move, status, board):
		return True
	else:
		return False

def is_narrow(move, status, board):
	"""
	Checks a single tile to see if it is in a tunnel or not.
	
	If the tile is in a tunnel, it prepares to check the next one and returns True.
	If the tile is a dead end, it stops checking and returns True.
	If the tiles is not in a tunnel, it returns False.
	"""
	open = []
	adjacent = board.adjacent(move)
	for tile in adjacent:
		if board.passable(tile):
			open.append(tile)
#	debug.log("Checking " + str(move))
#	debug.log("open = " + str(open))
#	debug.log("last_checked = " + str(status.last_checked))
	if status.last_checked in open:
		open.remove(status.last_checked)
	if len(open) == 1:
		status.last_checked = move
		status.checking = open[0]
		return True
	elif len(open) == 0:
		status.iterations = 31
		return True
	else:
		return False

def check_strat(them_y, them_x, me_y, me_x, status):
	"""
	Adjusts the current strategy based on the distance from the opponent.
	
	Changes status.strategy to "near" if they are within 5 spaces.
	Changes status.strategy to "far" if they aren't.
	
	Notifies the log if the strategy has changed.
	"""
	if (abs(them_y - me_y) < 6) and (abs(them_x - me_x) < 6):
		if status.strategy == "far" and Logs:
			debug.log("I've spotted them!  Attack mode activated!")
		status.strategy = "near"
	else:
		if status.strategy == "near" and Logs:
			debug.log("I've lost them.  Changing to sweep pattern.")
		status.strategy = "far"
	

def which_move(board, status):
	"""
	Checks the board for the bot's location, the opponents location, what moves are available,
	and what strategy should be used.
	
	Returns a move (NORTH, SOUTH, EAST, or WEST), determined by the get_move function.
	"""
	
	my_moves = board.moves()
	them_y, them_x = board.them()
	me_y, me_x = board.me()
	check_strat(them_y, them_x, me_y, me_x, status)
	
	if status.turn == 0:
		if Logs: debug.log("And so it begins...")
		for i in [NORTH, EAST, SOUTH, WEST]:
			if (i in my_moves) and (left_side[i] not in my_moves):
				status.facing = i
				status.first_move = False
				break
	
	#debug.log("all moves are " + str(my_moves))
	a = check_narrow(my_moves, status, board)
	if a:
		my_moves = a
	
	move = get_move(board, my_moves, them_y, them_x, me_y, me_x, status)
	
	status.turn += 1
	return move

def get_move(board, my_moves, them_y, them_x, me_y, me_x, status):
	"""
	Determines what move should actually be made based on the current strategy and available moves.
	
	Returns a move by calling the go function (NORTH, SOUTH, EAST, or WEST).
	"""
	#debug.log("----")
	#debug.log("I am at " + str(me_y) + ", " + str(me_x))
	#debug.log("They are at " + str(them_y) + ", " + str(them_x))
	#debug.log("My strategy is " + str(strategy))
	
	if len(my_moves) == 0:
		if Logs: debug.log("I have no moves!  Oh, @#$\%!")
		return NORTH
	
	if status.strategy == "far":
		move_list = []
		for i in my_moves:
			move_list.append(move_names[i])
		if Logs: debug.log("Day %i, my clear paths are: " % status.turn + str(move_list))
		
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
			if Logs: debug.log("something went wrong... no moves, but moving?")
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
				direction = random.choice(my_moves)
				return go(direction, "freaking out")

# you do not need to modify this part, but I did slightly.
for board in tron.Board.generate():
    tron.move(which_move(board, status))
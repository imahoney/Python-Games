#iteration = [0]
#last_move = status.facing
#
#def check_narrow(moves):
#	new_list = list(moves)
#	for move in moves:
#		move_counter = 0
#		checking = board.rel(move)
#		future_moves = {NORTH:(checking[0], checking[1]-1), EAST:(checking[0]+1, checking[1]),\
#						SOUTH:(checking[0], checking[1]+1), WEST:(checking[0]-1, checking[1])}
#		#debug.log("checking " + str(move))
#		for i in future_moves:
#			if i not behind[last_move]:
#				if board.passable(future_moves[i]):
#					move_counter += 1
#		#debug.log("counter = " + str(counter))
#		if counter < 2 and :
#			new_list.remove(move)
#	return new_list



def check_narrow(moves, status, board):
	new_list = list(moves)
	for move in moves:
		status.iterations = 0
		if stays_narrow(move, status, board):
			new_list.remove(move)
	return new_list

def stays_narrow(move, status, board):
	move = board.rel(move)
	while is_narrow(move) and status.iterations <= 3:
		status.iterations += 1
		move = status.last_checked
	if is_narrow(move):
		return True
	else:
		return False

def is_narrow(move, status, board):
	open = []
	adjacent = board.adjacent(move)
	for tile in adjacent:
		if board.passable(tile):
			open.append(tile)
	if status.last_checked in open:
		open.remove(status.last_checked)
	if len(open) == 1:
		status.last_checked = open[0]
		return True
	elif len(open) == 0:
		status.iterations = 4
		return True
	else:
		return False
# twixt.py
# Ian Mahoney
# 12/01/2008
"""
This program is a simulation of the game Twixt.
Two players, red and black, each try to form a line from one side of the board to the other.
They do this by placing pegs in the holes on the board.  If a peg is a knight's move away (L-shape)
then a bridge is built between the two pegs.  Requires two players to play.

This program makes use of the graphics module by John Zelle from "Python Programming: An Intro
To Computer Science."
"""

from graphics import *


class Board:
	"""
	Stores the size of the board, a list of all of the holes on the board (legal moves),
	where all the red pegs are, where all the black pegs are, and what turn it is.
	Also stores information for the check_win function: the last peg played,
		the pegs that have been checked so far, all of the bridges that have been made so far,
		and whether or not the game is over.
	Also, creates a GraphWin object (self.win) which other functions can draw to.
	"""
	def __init__(self, size):
		self.turn = 1
		self.size = size
		self.winSize = size * 20	#size of board in pixels (for the window)
		self.win = GraphWin(Board, self.winSize+10, self.winSize)
		
		self.holes = []
		for x in range(0, self.size):
			for y in range(0, self.size):
				self.holes.append((x+0.5, y+0.5))
		
		self.black_pegs = []
		self.red_pegs = []
		self.bridges = {}
		
		self.last_peg = (0, 0)
		self.checked_pegs = []
		self.done = False

def make_board(board):
	"""
	Draws the board using the given board object.
	The size of the board is X by X where X = size.
	size must be an integer, input must be a board object.
	"""
	
	for hole in board.holes:
		a = Circle(Point(hole[0], hole[1]), 0.3)
		a.setFill("grey")
		a.draw(board.win)
	
	for x in [1, (board.size-1)]:	#draw red lines
		a = Line(Point(x, 0), Point(x, board.size))
		a.setOutline("red")	#red plays horizontally
		a.draw(board.win)
	
	for y in [1, (board.size-1)]:	#draw black lines
		a = Line(Point(0, y), Point(board.size, y))
		a.setOutline("black")	#black plays vertically
		a.draw(board.win)
	

def play_round(turn, board):
	"""
	Determine whose turn it is, then play one turn.
	Afterwards, increments the turn counter (board.turn) by one.
	"""

	if (turn%2) == 0:
		color = "black"
	else:
		color = "red"
	
	player = Circle(Point(board.size+1.5, (board.size*1.0)/2), 1)
	player.setFill(color)
	player.draw(board.win)

	tf = False
	while tf == False:	#only continues once a valid point is selected
		point, tf = get_click(board, color)
	
	mod_lists(point, color, board)
	place_peg(point, color, board)
	
	board.turn = (board.turn)+1

def check_win(board):
	"""
	Checks for a winner.  Only checks if there is a peg in an end zone.
	Returns the value of board.done (True or False)
	Uses the check_peg() function.
	"""
	for peg in board.red_pegs:
		if (peg[0] < 1):
#			print "checking right"	#debug
			board.done = (check_peg(board, peg, "right") or board.done)
			
	for peg in board.black_pegs:
		if (peg[1] < 1):
#			print "checking up"	#debug
			board.done = (check_peg(board, peg, "up") or board.done)
	
	board.checked_pegs = []
	
	if board.done:
		if (board.turn%2) == 0:
			color = "red"
		else:
			color = "black"
		
		for i in [-4, -2, 2, 4]:
			winner = Circle(Point(board.size+1.5, ((board.size*1.0)/2)+i), 1)
			winner.setFill(color)
			winner.draw(board.win)
	
	return board.done

def check_peg(board, point, direction):
	"""
	Recursive function.  Checks to see if the current peg is in an end zone,
	then checks each peg connected to it.
	Takes advantage of the fact that a boolean can be converted to a number,
	1 for True, 0 for False.
	"""
	board.checked_pegs.append(point)
#	print "checked pegs are", board.checked_pegs	#debug
	if (direction == "right"):
		color = "red"
	else:
		color = "black"
	
	if (direction == "right") and (point[0] > board.size-1):
		return True
	elif (direction == "up") and (point[1] > board.size-1):
		return True
	
	bridge_distance = [ (point[0]-2, point[1]+1), (point[0]-2, point[1]-1),
						(point[0]-1, point[1]+2), (point[0]-1, point[1]-2),
						(point[0]+1, point[1]+2), (point[0]+1, point[1]-2),
						(point[0]+2, point[1]+1), (point[0]+2, point[1]-1),]
	bridges = []
	for peg in bridge_distance:
		a = [point, peg]
		a.sort()
		if (str(a) in board.bridges) and (peg not in board.checked_pegs):
#			print point, "is now in"	#debug
			bridges.append(peg)
#			print bridges	#debug
	
	if bridges == []:
		return False
	
	accum = 0
	for bridge in bridges:
		accum += check_peg(board, bridge, direction)
#		print "accum =", accum	#debug
	
	if accum > 0:
		return True
	else:
		return False
	
def mod_lists(point, color, board):
	"""
	Updates the list of possible moves by removing it from (board.holes) and adding it
	to the list of the corresponding color.
	"""
	if color == "red":
		c = board.red_pegs
	else:
		c = board.black_pegs
	c.append(board.holes.pop(board.holes.index(point)))
#	print board.red_pegs	#debug
#	print board.black_pegs	#debug

def get_click(board, color):
	"""
	Waits for the player to click, checks to see if it's a valid place to play,
	then returns the coordinates of the peg to be placed and whether it's valid or not.
	The color is a string (either "red" or "black") which shows whose turn it is.
	Returns a tuple and a boolean.
	"""
	
	point = board.win.getMouse()
	
	point = ((int(point.getX()))+0.5, (int(point.getY()))+0.5)
#	print point				#debug

	if (color == "red") and ((point[1] < 1) or (point[1] > board.size-1)):
		return (point), False	
	elif (color == "black") and ((point[0] < 1) or (point[0] > board.size-1)):
		return (point), False
	else:
		return (point), (point in board.holes)
	

def place_peg(point, color, board):
	"""
	Creates a circle of the given color at the given point and draws it in the window.
	"""
	peg = Circle(Point(point[0], point[1]), 0.3)
	peg.setFill(color) #color is either red or black depending on the turn
	peg.draw(board.win)
	bridge(point, color, board)
	board.last_peg = point
#	print "last peg is", board.last_peg	#debug

def bridge(point, color, board):
	"""
	Checks to see if a bridge can be drawn from the newly placed peg.
	Calls the draw_bridge() function for each valid bridge.
	"""
	bridge_distance = [ (point[0]-2, point[1]+1), (point[0]-2, point[1]-1),
						(point[0]-1, point[1]+2), (point[0]-1, point[1]-2),
						(point[0]+1, point[1]+2), (point[0]+1, point[1]-2),
						(point[0]+2, point[1]+1), (point[0]+2, point[1]-1),]
	
	if color == "red":
		c = board.red_pegs
	else:
		c = board.black_pegs

	for hole in bridge_distance:
		if hole in c:
			draw_bridge(point, hole, color, board)

def draw_bridge(peg_1, peg_2, color, board):
	"""
	Draws a bridge between the two points to board.win.
	Also updates board.bridges to inclued the newly added bridge.
	"""
	
	if not bridge_test(peg_1, peg_2, board):
		return
	
	a = [peg_1, peg_2]
	a.sort()
	a = str(a)
	b = {a : False}
	board.bridges.update(**b)
#	print board.bridges		#debug
	
	line = Line(Point(peg_1[0], peg_1[1]), Point(peg_2[0], peg_2[1]))
	line.setOutline(color)
	line.draw(board.win)

def bridge_test(peg_1, peg_2, board):
	"""
	Checks to make sure there isn't a line in the way of the bridge being built.
	Returns a boolean.
	"""
	pegs = [peg_1, peg_2]
	pegs.sort()
	p1 = pegs[0]
	p2 = pegs[1]
	x = p1[0]
	y = p1[1]
	x2 = p2[0]
	y2 = p2[1]
	
	if ((x - x2)%2 == 1) and (y < y2):
		blockers = [str([(x-1,y), (x+1,y+1)]),
					str([(x-1,y+1), (x+1,y)]),
					str([(x-1,y+2), (x+1,y+1)]),
					str([(x,y+1), (x+1,y-1)]),
					str([(x,y+1), (x+2,y)]),
					str([(x,y+1), (x+2,y+2)]),
					str([(x,y+2), (x+1,y)]),
					str([(x,y+2), (x+2,y+1)]),
					str([(x,y+3), (x+1,y+1)])]
#		print "line vu"	#debug

	elif ((x - x2)%2 == 0) and (y < y2):
		blockers = [str([(x-1,y+1), (x+1,y)]),
					str([(x,y+1), (x+1,y-1)]),
					str([(x,y+1), (x+2,y)]),
					str([(x,y-1), (x+1,y+1)]),
					str([(x+1,y+1), (x+2,y-1)]),
					str([(x+1,y+1), (x+3,y)]),
					str([(x,y+2), (x+1,y)]),
					str([(x+1,y+2), (x+2,y)]),
					str([(x+1,y), (x+2,y+2)])]
#		print "line hu"	#debug
				
	elif ((x - x2)%2 == 1) and (y > y2):
		blockers = [str([(x-1,y), (x+1,y-1)]),
					str([(x-1,y-1), (x+1,y)]),
					str([(x-1,y-2), (x+1,y-1)]),
					str([(x,y-1), (x+1,y+1)]),
					str([(x,y-1), (x+2,y)]),
					str([(x,y-1), (x+2,y-2)]),
					str([(x,y-2), (x+1,y)]),
					str([(x,y-2), (x+2,y-1)]),
					str([(x,y-3), (x+1,y-1)])]
#		print "line vd"	#debug
				
	elif ((x - x2)%2 == 0) and (y > y2):
		blockers = [str([(x-1,y-1), (x+1,y)]),
					str([(x,y-1), (x+1,y+1)]),
					str([(x,y-1), (x+2,y)]),
					str([(x,y+1), (x+1,y-1)]),
					str([(x+1,y-1), (x+2,y+1)]),
					str([(x+1,y-1), (x+3,y)]),
					str([(x,y-2), (x+1,y)]),
					str([(x+1,y-2), (x+2,y)]),
					str([(x+1,y), (x+2,y-2)])]
#		print "line hd"	#debug
	
	for bridge in blockers:
		try:
			return board.bridges[bridge]
		except:
#			print bridge, "wasn't a problem"	#debug
			None
		
	return True
	

def main():
	a = True
	while a:
		size = input("How big is the board? (ex. 24)  ")
		size = int(size)
		if (size < 37) and (size > 5):
			a = False
	
	board = Board(size)
	board.win.setCoords(-0.5, -0.5, board.size+2.5, board.size+0.5)
	
	make_board(board)
	
	while not check_win(board):
		play_round(board.turn, board)

	board.win.getMouse()
	board.win.close()

main()
# TicTacToe.py
# by Ian Mahoney
# 9/29/2008
# Allows you to play a game of Tic Tac Toe.

from graphics import *

win = GraphWin("Board", 600, 600)
win.setCoords(-0.3, -0.3, 3.3, 3.3)

squares = [ \
(0.5, 0.5), (1.5, 0.5), (2.5, 0.5), \
(0.5, 1.5), (1.5, 1.5), (2.5, 1.5), \
(0.5, 2.5), (1.5, 2.5), (2.5, 2.5)]
# creates a list of all of the points which represent spaces on the board.
# They are arranged as shown:
#	squares[6] I squares[7] I squares[8]
#	--------------------------------
#	squares[3] I squares[4] I squares[5]
#	--------------------------------
#	squares[0] I squares[1] I squares[2]


conditions = [(squares[0], squares[1], squares[2]), (squares[3], squares[4], squares[5]), \
(squares[6], squares[7], squares[8]), (squares[0], squares[3], squares[6]) \
(squares[1], squares[4], squares[7]), (squares[3], squares[5], squares[8]) \
(squares[0], squares[4], squares[8]), (squares[2], squares[4], squares[6])]
# List of winning conditions.

def setup():
	"""Prints info about the program and asks for the number of players."""
	print "This program lets you play Tic Tac Toe without wasting paper!"
	print "Player 1 plays X and Player 2 plays O."
	print
	
	while True:
		players = input("Please enter number of human players (1 or 2): ")
		
		if (players == 1) or (players == 2):
			return players
		
		else:
			print "You have to enter either \"1\" or \"2\""
			print

def drawboard():
	L1 = Line(Point(1,0), Point(1,3))
	L2 = Line(Point(2,0), Point(2,3))
	L3 = Line(Point(0,1), Point(3,1))
	L4 = Line(Point(0,2), Point(3,2))
	L1.setWidth(2)
	L2.setWidth(2)
	L3.setWidth(2)
	L4.setWidth(2)
	L1.draw(win)
	L2.draw(win)
	L3.draw(win)
	L4.draw(win)

def getclick():
	while True:
		click = win.getMouse()
		if (click.getX() < 0) or (click.getX() >= 3) \
		or (click.getY() < 0) or (click.getY() >= 3):
			print "Please click inside a square."
			print
		
		else:
			return click

def xDraw(click):
		x = click.getX()
		x = float(int(x)) + 0.5
		y = click.getY()
		y = float(int(y)) + 0.5
		
		#debug print x, y
		
		if (x, y) not in squares:
			print "That square is full."
			print
			return False
		
		else:
			#draw an X at Point(x, y)
			X1 = Line(Point((x-0.4), (y-0.4)), Point((x+0.4), (y+0.4)))
			X1.setWidth(2)
			X1.setOutline("Blue")
			X2 = Line(Point((x+0.4), (y-0.4)), Point((x-0.4), (y+0.4)))
			X2.setWidth(2)
			X2.setOutline("Blue")
			X1.draw(win)
			X2.draw(win)
			
			return (x, y)

def oDraw(click):
		x = click.getX()
		x = float(int(x)) + 0.5
		y = click.getY()
		y = float(int(y)) + 0.5
		
		#debug print x, y
		
		if (x, y) not in squares:
			print"That square is full."
			print
			return False
		
		else:
			o = Circle(Point(x, y), 0.4)
			o.setWidth(2)
			o.setOutline("red")
			o.draw(win)
			
			return (x, y)

def change_square(point, symbol):
	for i in range(9):
		if point == squares[i]:
			squares[i] = symbol
	#debug print squares

def checkwin(symbol):
	for i in range(len(conditions)):
		if condtions[i] == (symbol, symbol, symbol):
			winner(symbol)
			return True
		
		else:
			return False
		
def winner(symbol):
	if symbol == "X":
		print "Player 1 wins!"
		print
	
	elif symbol == "O":
		print "Player 2 wins!"
		print
	
	else:
		print "Something went wrong!"


def P2_game():
	for i in range(4):
		print "Player 1, please click a square."
		print
		
		x = False
		
		while x == False:
			click = getclick()
			x = xDraw(click)
		
		change_square(x, "X")
		a = checkwin("X")
		if a == True:
			break
		
		print "Player 2, please click a square."
		print
		
		o = False
		
		while o == False:
			click = getclick()
			o = oDraw(click)
		
		change_square(o, "O")
		a = checkwin("O")
		if a == True:
			break
		
	if a == False:
		print "Player 1, please click a square."
		print
		
		x = False
		
		while x == False:
			click = getclick()
			x = xDraw(click)
		
		change_square(x, "X")
		a = checkwin("X")
		if a == True:
			print "Click again to close"
		
		else:
			print "It's a tie..."
			print
			
	print "Click again to close"
	win.getMouse()
	win.close()

def P1_game():
	print "You haven't Programmed this yet, you jerk!"
	print "Maybe you can program it another time."
	
def main():
	drawboard()
	players = setup()
	
	if players == 2:
		P2_game()
	
	elif players == 1:
		P1_game()
	
main()
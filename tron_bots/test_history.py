#!/usr/bin/python
"""
 test_history.py 

 Confirmation that things are working as expected is that in the log file,
 'this' for move n is 'last' for move n+1.

 $ tron -v -B maps/empty-room.txt $pybots/test_history.py $pybots/randbot.py
 $ more lots/test_history.txt
 --- 'logs/test_history.txt' at Thu Feb 25 23:33:24 2010 --- 
 1 this, last : south, north 
 2 this, last : east, south 
 3 this, last : east, east 
 4 this, last : north, east 
 5 this, last : east, north 
 6 this, last : east, east 
 7 this, last : south, east 
 8 this, last : west, south 
 9 this, last : south, west 
 10 this, last : east, south 
 11 this, last : east, east 
 12 this, last : north, east 
 13 this, last : east, north 
 14 this, last : north, east 
 15 this, last : east, north 

 Jim Mahoney | Feb 2010 | GPL
"""

import random, tron, utilities

history = utilities.BotHistory()
debug = utilities.LogFile("logs/test_history.txt")

def which_move(board):
  history.update(board)
  move = random.choice(board.moves())
  direction = utilities.direction2string[move]
  lastDirection = utilities.direction2string[history.lastDirection()]
  debug.log("%i this, last : %s, %s " % \
              (history.length(), direction, lastDirection))
  return move

# --- main -------------------
for board in tron.Board.generate():
  tron.move(which_move(board))

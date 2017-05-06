# rule 1: stay close to your neighbors
# rule 2: if they get too close, get away
# rule 3: match the speed of neighbors


###############################################################################

import curses
import cursestools
import time
import strategies.flock as flock
import os
from matrix import Matrix


###############################################################################

screen_rows, screen_columns = map(lambda x: int(x), os.popen('stty size', 'r').read().split())
sim = None

# simulation settings
DELAY = 0.01
HEIGHT = screen_rows - 3
WIDTH = screen_columns - 2
NUM_DRONES = 50

# flock settings
SEARCH_RADIUS = 5
FLOCK_THRESHHOLD = 0
WANDER_THRESHHOLD = 30


###############################################################################

def main(scr):
	curses.curs_set(0)
	curses.start_color()
	scr.nodelay(1)
	sim = Matrix(scr, HEIGHT, WIDTH)

	my_flock = flock.strategy(SEARCH_RADIUS, FLOCK_THRESHHOLD, WANDER_THRESHHOLD)

	for i in range(0, NUM_DRONES):
		sim.add_drone(my_flock)

	draw_border(scr, 0, 0)
	bottom_bar(scr, '[ Esc to exit ]')

	while scr.getch() != 27:
		sim.draw(1, 1)
		sim.next()
		time.sleep(DELAY)


def draw_border(scr, top, left):
	for row in range(0, HEIGHT + 1):
		cursestools.addstrc(scr, top + row, left, '|', 7, 0)
		cursestools.addstrc(scr, top + row, left + WIDTH + 1, '|', 7, 0)

	for col in range(0, WIDTH + 1):
		cursestools.addstrc(scr, top, left + col, '-', 7, 0)
		cursestools.addstrc(scr, top + HEIGHT + 1, left + col, '-', 7, 0)

	cursestools.addstrc(scr, top, left, '+', 7, 0)
	cursestools.addstrc(scr, top, left + WIDTH + 1, '+', 7, 0)
	cursestools.addstrc(scr, top + HEIGHT + 1, left, '+', 7, 0)
	cursestools.addstrc(scr, top + HEIGHT + 1, left + WIDTH + 1, '+', 7, 0)


def bottom_bar(scr, text):
	text += ' ' * (screen_columns - len(text) - 1)
	cursestools.addstrc(scr, screen_rows - 1, 0, text, 0, 7)


###############################################################################

curses.wrapper(main)
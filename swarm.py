import curses
import cursestools
import time
import strategies.flock as flock
import os
from random import randint
from matrix import Matrix


###############################################################################

screen_rows, screen_columns = map(lambda x: int(x), os.popen('stty size', 'r').read().split())
matrix = None

# simulation settings

DELAY = 0.01
TURN_LENGTH = 0
HEIGHT = screen_rows - 3
WIDTH = screen_columns - 2

# flock settings

NUM_DRONES = 50
SEARCH_RADIUS = 7		# the radius that a drone searches for neighbors
WANDER_THRESHHOLD = 30	# the percentage chance that the drone random walks

# flock threshhold is the distance at which a drone is repulsed from its neighbors.
# if this constant is an integer, one flock strategy will be generate with that flock threshhold.
# if this constant is an array, a flock strategy will be generated for each value.
FLOCK_THRESHHOLD = [0, 5]


###############################################################################

def main(scr):
	curses.curs_set(0)
	curses.start_color()
	scr.nodelay(1)

	matrix = Matrix(scr, HEIGHT, WIDTH)

	threshhold_values = []
	if type(FLOCK_THRESHHOLD) is list:
		threshhold_values = FLOCK_THRESHHOLD
	else:
		threshhold_values = [FLOCK_THRESHHOLD]
	flock_strategies = map(lambda f: flock.strategy(SEARCH_RADIUS, f, WANDER_THRESHHOLD), threshhold_values)

	colors = [1, 6, 2, 3, 9, 14, 10, 11]

	for i in range(0, NUM_DRONES):
		i = randint(0, len(flock_strategies) - 1)
		matrix.add_drone(colors[i], flock_strategies[i])

	draw_border(scr, 0, 0)
	bottom_bar(scr, '[ Esc to exit ]')

	last_time = time.time()
	while scr.getch() != 27:
		matrix.draw(1, 1)
		matrix.next()

		diff = TURN_LENGTH - (time.time() - last_time)
		if diff > 0:
			time.sleep(diff)
		last_time = time.time()


###############################################################################

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


###############################################################################

def bottom_bar(scr, text):
	text += ' ' * (screen_columns - len(text) - 1)
	cursestools.addstrc(scr, screen_rows - 1, 0, text, 0, 7)


###############################################################################

curses.wrapper(main)
import curses

last_pair = 1
color_dict = dict()

COLORS = [
	curses.COLOR_BLACK,
	curses.COLOR_BLUE,
	curses.COLOR_GREEN,
	curses.COLOR_CYAN,
	curses.COLOR_RED,
	curses.COLOR_MAGENTA,
	curses.COLOR_YELLOW,
	curses.COLOR_WHITE,
	curses.COLOR_BLACK,
	curses.COLOR_BLUE,
	curses.COLOR_GREEN,
	curses.COLOR_CYAN,
	curses.COLOR_RED,
	curses.COLOR_MAGENTA,
	curses.COLOR_YELLOW,
	curses.COLOR_WHITE
]


def addstrc(scr, row, col, str, fore, back):
	global last_pair
	pair_index = -1
	color_pair = (COLORS[fore], COLORS[back])

	if color_pair not in color_dict:
		curses.init_pair(last_pair, COLORS[fore], COLORS[back])
		color_dict[color_pair] = last_pair
		pair_index = last_pair
		last_pair += 1
	else:
		pair_index = color_dict[color_pair]

	color_attr = curses.color_pair(pair_index)
	if fore > 7:
		color_attr |= curses.A_BOLD
	if back > 7:
		color_attr |= curses.A_REVERSE

	scr.addstr(row, col, str, color_attr)

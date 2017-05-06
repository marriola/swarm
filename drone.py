import math

next_letter	= 0

class Drone:
	def __init__(self, color, row, col, strategy=None):
		global next_letter
		self.fore_color = 7 if color in [1,4,5,8] else 0
		self.color = color
		self.row = row
		self.col = col
		self.strategy = strategy
		self.letter = chr(65 + next_letter % 26)
		next_letter	+= 1

	def distance_from(self, other):
		return math.sqrt((self.row - other.row) ** 2 + (self.col - other.col) ** 2)

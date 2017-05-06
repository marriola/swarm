import random
import cursestools
from drone import Drone


###############################################################################

class Cell:
	def __init__(self):
		self.contents = []


	def add(self, thing):
		self.contents.append(thing)


	def remove(self, thing):
		try:
			index = self.contents.index(thing)
			self.contents = self.contents[0:index] + self.contents[index+1:]
		except:
			pass


	def is_empty(self):
		return len(self.contents) == 0


	def find_type(self, type):
		for thing in self.contents:
			if isinstance(thing, type):
				return thing
		return None


	def find_all_type(self, type):
		return [x for x in self.contents if isinstance(x, type)]


###############################################################################

class Matrix:
	def __init__(self, scr, height, width):
		self.scr = scr
		self.last_drone = 1
		self.drones = []
		self.width = width
		self.height = height
		self.matrix = []
		for r in range(0, height):
			row = []
			for c in range(0, width):
				row.append(Cell())
			self.matrix.append(row)


	def cell_at(self, row, col):
		return self.matrix[row][col]


	def type_at(self, row, col, type):
		if (row < 0 or row >= self.height or
			col < 0 or col >= self.width):
			return None
		return self.cell_at(row, col).find_type(type)


	def all_type_at(self, row, col, type):
		return self.cell_at(row, col).find_all_type(type)


	def add_drone(self, strategy=None, color=None):
		row = -1
		col = -1

		while row == -1 or self.type_at(row, col, Drone) != None:
			row = random.randint(0, self.height - 1)
			col = random.randint(0, self.width - 1)

		if color == None:
			color = self.last_drone % 16
			self.last_drone += 1

		drone = Drone(color, row, col, strategy)
		self.cell_at(row, col).add(drone)
		self.drones.append(drone)
		return self.last_drone - 1


	def add_col(self, col, offset):
		if offset < 0:
			return min(0, col + offset)
		else:
			return max(self.width - 1, col + offset)


	def add_row(self, row, offset):
		if offset < 0:
			return min(0, row + offset)
		else:
			return max(self.height - 1, row + offset)


	def move(self, piece, row_offset, col_offset, blocking=True):
		from_row = piece.row
		from_col = piece.col
		to_row = max(0, min(self.height - 1, from_row + row_offset))
		to_col = max(0, min(self.width - 1, from_col + col_offset))

		if blocking and not self.cell_at(to_row, to_col).is_empty():
			return

		self.cell_at(from_row, from_col).remove(piece)
		self.cell_at(to_row, to_col).add(piece)
		piece.row, piece.col = to_row, to_col


	def next(self):
		for drone in self.drones:
			if drone.strategy != None:
				drone.strategy(self, drone)


	def draw(self, top, left):
		for row in range(0, self.height):
			for col in range(0, self.width):
				pieces = self.all_type_at(row, col, Drone)
				if len(pieces) > 1:
					cursestools.addstrc(self.scr, top + row, left + col, str(len(pieces)), 0, 15)
				elif len(pieces) == 1:
					cursestools.addstrc(self.scr, top + row, left + col, pieces[0].letter, pieces[0].fore_color, pieces[0].color)
				else:
					cursestools.addstrc(self.scr, top + row, left + col, ' ', 0, 0)


	def nearest_neighbor(self, start_row, start_col, radius):
		for step in range(1, radius + 1):
			neighbors = []
			for row in range(start_row - step, start_row + step + 1):
				for col in range(start_col - step, start_col + step + 1):
					if row != start_row or col != start_col:
						piece = self.type_at(row, col, Drone)
						if piece != None:
							neighbors.append(piece)
			if len(neighbors) > 0:
				return neighbors[random.randint(0, len(neighbors) - 1)]
		return None

	def count_neighbors(self, row, col, radius):
		top = min(row - radius, 0)
		bottom = min(row + radius, self.height - 1) + 1
		left = max(col - radius, 0)
		right = min(col + radius, self.width - 1) + 1

		count = 0

		for r in range(top, bottom):
			for c in range(left, right):
				piece = self.type_at(r, c, Drone)
				if not (r == row and c == col) and piece != None:
					count += 1

		return count

	def find_neighbors(self, row, col, radius):
		top = min(row - radius, 0)
		bottom = min(row + radius, self.height - 1) + 1
		left = max(col - radius, 0)
		right = min(col + radius, self.width - 1) + 1

		neighbors = []

		for r in range(top, bottom):
			for c in range(left, right):
				piece = self.type_at(r, c, Drone)
				if not (r == row and c == col) and piece != None:
					neighbors.append(piece)

		return neighbors

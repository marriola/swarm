import random

def strategy(matrix, drone):
	right = random.randint(0, 2) - 1
	down = random.randint(0, 2) - 1
	matrix.move(drone, down, right)

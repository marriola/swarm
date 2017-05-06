import strategies.random_walk as random_walk
import random

def direction(n):
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0


def strategy(radius, wander_threshhold):
    def avoid_strategy(matrix, drone):
        wander = random.randint(0, 100) <= wander_threshhold
        if wander:
            random_walk.strategy(matrix, drone)
            return

        nearest = matrix.nearest_neighbor(drone.row, drone.col, radius)
        if nearest != None:
            row, col = nearest.row, nearest.col
            down = row - drone.row
            right = col - drone.col

            downdir = direction(down) * -1
            rightdir = direction(right) * -1

            matrix.move(drone, downdir, rightdir)
        else:
            random_walk.strategy(matrix, drone)

    return avoid_strategy

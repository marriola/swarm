# Swarm Configuration

The configs directory contains a few sample configurations that can be loaded into swarm.py. Each contains three constants:

 * SEARCH_RADIUS
 * WANDER_THRESHHOLD
 * FLOCK_THRESHHOLD


## SEARCH_RADIUS

The radius that a drone searches for neighbors.


## WANDER_THRESHHOLD

Wander threshhold is the percent chance that a drone will random walk instead of moving purposefully.


## FLOCK_THRESHHOLD

Flock threshhold is the distance at which a drone is repulsed from its neighbors.
If this constant is an integer, one flock strategy will be generate with that flock threshhold. If it is an array, a flock strategy will be generated for each value.

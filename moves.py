# grid finder.csv
import numpy as np
from numpy import genfromtxt
map = np.flipud(genfromtxt('pacman_map.csv', delimiter=','))

def possible_moves(current_pos):
    current_pos = (current_pos[1]+1, current_pos[0]+1)
    if not(map[current_pos[0]][current_pos[1]]):
        return -1
    allowed = []
    if map[current_pos[0]][current_pos[1]+1]:
        allowed.append("R")
    if map[current_pos[0]][current_pos[1]-1]:
        allowed.append("L")
    if map[current_pos[0]+1][current_pos[1]]:
        allowed.append("U")
    if map[current_pos[0]-1][current_pos[1]]:
        allowed.append("D")
    return allowed

print(possible_moves([9,5]))

np.savetxt("foo.csv",map,delimiter = ',')

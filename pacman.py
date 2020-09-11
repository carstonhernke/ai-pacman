import logging
import os, sys
import gym
import numpy as np
import matplotlib.pyplot as plt
from gym.envs.classic_control import rendering
import time
import random
import matplotlib.pyplot as plt
from numpy import genfromtxt

def get_center(p):
    ycenter = np.amin(p[0])+((np.amax(p[0]) - np.amin(p[0]))//2)
    xcenter = np.amin(p[1])+((np.amax(p[1]) - np.amin(p[1]))//2)
    return (xcenter, ycenter)

def find_pacman(o,map):
    c = (210, 164, 74)
    indices = np.where(np.all(o == c, axis=-1))
    if (len(indices[0])==0):
        return - 1
    else:
        return new_loc(get_center(indices), map)

def find_g1(o,map):
    c = (200,72,72)
    indices = np.where(np.all(o == c, axis=-1))
    if (len(indices[0])==0):
        return - 1
    else:
        return new_loc(get_center(indices), map)

def find_g2(o,map):
    c = (84,184,153)
    indices = np.where(np.all(o == c, axis=-1))
    if (len(indices[0])==0):
        return - 1
    else:
        return new_loc(get_center(indices), map)

def find_g3(o,map):
    c = (198,89,179)
    indices = np.where(np.all(o == c, axis=-1))
    if (len(indices[0])==0):
        return - 1
    else:
        return new_loc(get_center(indices), map)

def find_g4(o,map):
    c = (180,122,48)
    indices = np.where(np.all(o == c, axis=-1))
    if (len(indices[0])==0):
        return - 1
    else:
        return new_loc(get_center(indices), map)

def get_score():
    return None

def plot_locations(loc):
    axes = plt.gca()
    axes.set_xlim([0,17])
    axes.set_ylim([0,14])

    x.append(loc[0])
    y.append(loc[1])
    plt.plot(x,y)

    plt.draw()
    plt.pause(0.0001)
    plt.clf()
    return None

def new_loc(old_coordinates, map):
    new_x = (old_coordinates[0]-6) // 8
    new_y = (170-old_coordinates[1]) // 12
    if map[new_x+1][new_y+1] == 0:
        if map[new_x+1][new_y] == 0:
            if map[new_x][new_y+1] == 0:
                print("yikes")
                return (new_x-1, new_y-1)
            else:
                return (new_x, new_y+1) # crude fix for a bug
        else:
            return (new_x+1, new_y) # crude fix for a bug
    else:
        return (new_x+1, new_y+1)

def get_possible_moves(current_pos,map):
    current_pos = (current_pos[1], current_pos[0])
    if not(map[current_pos[0]][current_pos[1]]):
        return -1
    allowed = []
    if map[current_pos[0]][current_pos[1]+1]:
        allowed.append("3")
    if map[current_pos[0]][current_pos[1]-1]:
        allowed.append("4")
    if map[current_pos[0]+1][current_pos[1]]:
        allowed.append("2")
    if map[current_pos[0]-1][current_pos[1]]:
        allowed.append("5")
    return allowed

def update_dot_locations(dot_locations):
    # scan for dots?
    return None;

def MCTS():
    for x in move_tree:
        None
        # run MCTS
            # how many dots?
            # are there ghosts?
        # after a cutoff, pick the move with the best score
    return None

class MoveTree:
    def __init__(self):
        self.left= False
        self.right = False
        self.up = False
        self.down = False

    def insert_left(self, child):
        self.left = child

    def insert_right(self, child):
        self.right = child

    def insert_up(self, child):
        self.up = child

    def insert_down(self, child):
        self.down = child

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_up(self):
        return self.up

    def get_down(self):
        return self.down



def make_tree(loc):
    t = MoveTree()
    m = get_possible_moves(loc)
    for i in m:
        if i == 3:
            new_loc = (loc[0],loc[1]+1)
            t.insert_right(new_loc)
        if i == 4:
            new_loc = (loc[0],loc[1]-1)
            t.insert_left(new_loc)
        if i == 2:
            new_loc = (loc[0]+1,loc[1])
            t.insert_up(new_loc)
        if i == 5:
            new_loc = (loc[0]-1,loc[1])
            t.insert_down(new_loc)
    return t

def output_obs_csv(o,c):
    np.savetxt("obs/r_"+str(c)+".csv", o[:,:,0], delimiter = ",")
    np.savetxt("obs/g_"+str(c)+".csv", o[:,:,1], delimiter = ",")
    np.savetxt("obs/b_"+str(c)+".csv", o[:,:,2], delimiter = ",")
    return None

def print_status(pacman_loc, g1_loc, g2_loc, g3_loc, g4_loc, possible_moves):
    print("Current location of Ms. Pacman:")
    print(pacman_loc)
    print("Current location of Ghost 1:")
    print(g1_loc)
    print("Current location of Ghost 2:")
    print(g2_loc)
    print("Current location of Ghost 3:")
    print(g3_loc)
    print("Current location of Ghost 4:")
    print(g4_loc)
    print("Possible Moves:")
    for i in possible_moves:
        if i == "3":
            print("Right")
        if i == "4":
            print("Left")
        if i == "2":
            print("Up")
        if i == "5":
            print("Down")
    print('\n')
    return None

def make_graph(map,orig_map):
    g = {}
    print(map.shape)
    for x in range(0,20):
        for y in range(0,15):
                #print("X="+str(x))
                #print("Y="+str(y))
                m = get_possible_moves((x,y),orig_map)
                if m == -1:
                    continue
                else:
                    neighbors = {}
                    for i in m:
                        if i == "3":
                            neighbors[str(x+1)+","+str(y)] = 1
                        if i == "4":
                            neighbors[str(x-1)+","+str(y)] = 1
                        if i == "2":
                            neighbors[str(x)+","+str(y+1)] = 1
                        if i == "5":
                            neighbors[str(x)+","+str(y-1)] = 1
                    g[str(x)+","+str(y)] = neighbors
    return g

def decode_node(node):
    loc = node.find(",")
    x = node[0:loc]
    y = node[loc+1:len(node)]
    return((x,y))

def decide_move(current_location, future_location):
    print(current_location)
    print(future_location)
    if int(current_location[0]) > int(future_location[0]):
        return 3
    if int(current_location[0]) < int(future_location[0]):
        return 4
    if int(current_location[1]) < int(future_location[1]):
        return 2
    if int(current_location[1]) > int(future_location[1]):
        return 5
    else:
        return -1

def update_map(map,g1,g2,g3,g4,dots):
    if g1 != -1:
        map[g1[0]][g1[1]] = 100
    if g2 != -1:
        map[g2[0]][g2[1]] = 100
    if g3 != -1:
        map[g3[0]][g3[1]] = 100
    if g4 != -1:
        map[g4[0]][g4[1]] = 100
    return map

# Here we make the r matrix for the basic map. Where an 
# agent can go from one cell to another as long as it isn't 1 and
# attached on the map

# imports
import numpy as np
from .states_and_actions import states
from .map import key
from .q_matrix import q_matrix

# print out the numpy array without it truncating
import sys
np.set_printoptions(threshold=sys.maxsize) # https://stackoverflow.com/questions/1987694/how-to-print-the-full-numpy-array-without-truncation

def r_matrix(map: np.array) -> np.array:
    """Here we make the r matrix for the basic map. Where an 
agent can go from one cell to another as long as it isn't 1 and
attached on the map"""
    # get the states list
    S = states(map)

    # set up the empty r matrix
    # rmat = np.zeros((len(S), len(actions))) * np.nan
    rmat = q_matrix(map) * np.nan

    height = len(map)
    width = len(map[0])

    # to simplify can only move up, down, left, right
    # rows are where the agent currently is
    # columns are where the agent is going to

    # from cell 10 the agent can move to cell 11, but all other routes are blocked
    # from cell 11 the agent can move to cell 10 and get the reward or go to cell 12

    rewardDict = key()

    for cell in S:
        # integer divide by 9 to get the y position, modulus to get the x
        y_pos = cell // height
        x_pos = cell % width
        # get the value of the cells around it
        if map[y_pos, x_pos] != 1:
            if y_pos > 0:
                # Check cell above
                above = map[y_pos - 1, x_pos]
                if above != 1:
                    rmat[cell, (y_pos - 1) * 9 + x_pos] = rewardDict[above]['reward']
            if y_pos < height - 1:
                # check cell below
                below = map[y_pos + 1, x_pos]
                if below != 1:
                    rmat[cell, (y_pos + 1) * 9 + x_pos] = rewardDict[below]['reward']
            
            if x_pos > 0:
                # check the cell to the left
                left = map[y_pos, x_pos - 1]
                if left != 1:
                    rmat[cell, y_pos * 9 + x_pos - 1] = rewardDict[left]['reward']
            if x_pos < width - 1:
                # check the cell to the right
                right = map[y_pos, x_pos + 1]
                if right != 1:
                    rmat[cell, y_pos * 9 + x_pos + 1] = rewardDict[right]['reward']
        # print(cell, y_pos, x_pos)#, rmat[cell])
    return rmat
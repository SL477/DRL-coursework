"""Here we setup the Q-matrix, which is just an array of zeros"""

# imports
import numpy as np
from .states_and_actions import states

def q_matrix(map: np.array) -> np.array:
    """Get the empty Q Matrix"""
    # get the states and actions list
    S = states(map)
    actions = states(map)

    # set up the empty r matrix
    return np.zeros((len(S), len(actions)))

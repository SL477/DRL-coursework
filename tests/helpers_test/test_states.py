from helpers.states_and_actions import states
import numpy as np

def test_states():
    assert states(np.zeros((4,5))) == [x for x in range(4*5)]
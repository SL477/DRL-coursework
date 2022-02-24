from helpers.map import basic_map
from helpers.random_start import random_start
from helpers.states_and_actions import states

def test_random_start():
    m = basic_map()
    s = random_start(m)
    assert s >= 0
    assert s < len(states(m))
    # check the value
    width = len(m[0])
    height = len(m)
    val = m[s // height, s % width]
    assert val != 1
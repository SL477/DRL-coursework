from helpers.r_matrix import r_matrix
from helpers.map import basic_map
from helpers.get_available_actions import get_available_actions

def test_get_available_actions():
    m = basic_map()
    r = r_matrix(m)
    assert len(get_available_actions(r, 10)) == 1

    assert len(get_available_actions(r, 11)) == 2


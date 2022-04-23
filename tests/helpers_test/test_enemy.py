from helpers.enemy import Enemy

def test_enemy():
    a = Enemy([1, 2, 3])
    assert a.positions == [1, 2, 3, 2]
    assert a.step() == 3
    assert a.step() == 2
    assert a.step() == 1
    assert a.step() == 2
"""Defines the enemy class"""

class Enemy():
    """An enemy, goes from state 0 -> 1 -> 2 -> 1 -> repeats"""
    def __init__(self, positions) -> None:
        # By copying state 1 (the mid point), we don't have to do any advanced logic 
        self.positions = positions + [positions[1]]
        self.current_position = 0
    
    def step(self):
        """Take the next step and return the position"""
        self.current_position += 1
        if self.current_position >= len(self.positions):
            self.current_position = 0
        return self.positions[self.current_position]
    
    def __repr__(self) -> str:
        # This is so the class prints out nicely
        return f'Enemy({self.positions[:-1]})'

if __name__ == '__main__':
    # manual testing
    a = Enemy([1, 2, 3])
    print(a.positions)
    print(a.step())
    print(a)
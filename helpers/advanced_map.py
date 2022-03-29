"""here we define the Advanced Map class"""

from typing import Tuple
from .map import adv_map
import numpy as np
from .enemy import Enemy

import matplotlib.pyplot as plt

class AdvancedMap():
    """Advanced map class. Holds an instance of the map. Animates the enemies. Handles actions"""
    def __init__(self, pos=None) -> None:
        self.map = adv_map()

        # find the enemies and their positions in the 3 time steps (looking for 7 & 8)
        self.enemies = []
        banned_positions = []
        # enemies who bob up and down
        for i in np.argwhere(self.map == 7.):
            epos = [(i[0] - 1, i[1]), (i[0], i[1]), (i[0] + 1, i[1])]
            banned_positions += epos
            self.enemies.append(Enemy(epos))
        
        # enemies who bob side to side
        for i in np.argwhere(self.map == 8.):
            epos = [(i[0], i[1] - 1), (i[0], i[1]), (i[0], i[1] + 1)]
            banned_positions += epos
            self.enemies.append(Enemy(epos))
        
        # agent's starting point
        # The agent cannot start where the enemies will be stepping
        allowed_positions = np.argwhere(self.map == 0.)
        # Remove the enemy positions
        allowed_positions = filter(lambda x: (x[1], x[0]) not in banned_positions, allowed_positions)

        allowed_positions = list(allowed_positions)
        #print(allowed_positions)
        if pos is None:
            # use randint, as choice only works on 1-d arrays. Use a tuple as it is smaller
            self.agent_pos = tuple(allowed_positions[np.random.randint(0, len(allowed_positions))])
            # flip round to x, y
            self.agent_pos = (self.agent_pos[1], self.agent_pos[0])
        else:
            self.agent_pos = pos

        # So that we can keep track of whether the agent stood on the floor or a door
        self.old_agent_value = self.map[self.agent_pos[1]][self.agent_pos[0]]

        self.map[self.agent_pos[1]][self.agent_pos[0]] = 5.

        # set other stats
        self.agent_health = 100
        
    def step(self, action):
        pass

    def display(self):
        """Show the map in a nice way"""
        # Some trial & error using https://numpy.org/doc/stable/reference/generated/numpy.array2string.html to get rid of the decimal
        print(np.array2string(self.map, formatter={'float_kind': lambda x: "%.0f" % x}))

    def displayImg(self):
        """Show the map as an image"""
        plt.imshow(self.map)
        plt.title("Advanced map")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
    
    def agents_view(self):
        """The agent can see in a 7 by 7 grid around itself. But cannot see through doors or walls (unless it is sitting on a door"""
        ret = np.zeros((7,7))
        # the agent is in the middle
        ret[3, 3] = 5.

        # start ray tracing around the agent. There is almost certainly a more efficient way of doing this
        # up
        """ for i in range(1, 4):
            val = self.map[self.agent_pos[1] - i][self.agent_pos[0]]
            ret[3 - i, 3] = val
            if val in [1, 2]:
                break
        # down
        for i in range(1, 4):
            val = self.map[self.agent_pos[1] + i][self.agent_pos[0]]
            ret[3 + i, 3] = val
            if val in [1, 2]:
                break
        # left
        for i in range(1, 4):
            val = self.map[self.agent_pos[1]][self.agent_pos[0] - i]
            ret[3, 3 - i] = val
            if val in [1, 2]:
                break
        # right
        for i in range(1, 4):
            val = self.map[self.agent_pos[1]][self.agent_pos[0] + i]
            ret[3, 3 + i] = val
            if val in [1, 2]:
                break """

        # primary diagonals and up/down/left/right
        for xmod, ymod in [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]:
            for i in range(1, 4):
                val = self.map[self.agent_pos[1] + (i * ymod)][self.agent_pos[0] + (i * xmod)]
                ret[3 + (i * ymod), 3 + (i * xmod)] = val
                if val in [1, 2]:
                    break
        # secondary diagonals (those not blocked by a wall on both closest compass directions)
        for block in [[(2, 1), (3, 1), (3, 2)], [(2, -1), (3, -1), (3, -2)], [(-2, 1), (-3, 1), (-3, 2)], [(-2, -1), (-3, -1), (-3, -2)]]: # the ones whose view is determined by the x-axis
            for col, row in block:
                # check that we aren't straying out of the boundary 
                if self.agent_pos[1] + row < len(self.map) and self.agent_pos[0] + col < len(self.map[0]):
                    val = self.map[self.agent_pos[1] + row][self.agent_pos[0] + col]
                    val_offset_1 = self.map[self.agent_pos[1] + row][self.agent_pos[0] + col - 1]
                    val_offset_2 = self.map[self.agent_pos[1] + row - 1][self.agent_pos[0] + col - 1]

                    
                    #print('val', val, self.agent_pos[0] + col - 1, self.agent_pos[1] + row)

                    if val_offset_1 in [1, 2] and val_offset_2 in [1, 2]:
                        break
                    ret[3 + row, 3 + col] = val

        
        #(1, 2), (1, 3), (2, 3)]: # north east missing regions
        for block in [[(1, 2), (1, 3), (2, 3)], [(1, -2), (1, -3), (2, -3)], [(-1, 2), (-1, 3), (-2, 3)], [(-1, -2), (-1, -3), (-2, -3)]]:
            for col, row in block:
                # check that we aren't straying out of the boundary 
                if self.agent_pos[1] + row < len(self.map) and self.agent_pos[0] + col < len(self.map[0]):
                    val = self.map[self.agent_pos[1] + row][self.agent_pos[0] + col]
                    val_offset_1 = self.map[self.agent_pos[1] + row - 1][self.agent_pos[0] + col]
                    val_offset_2 = self.map[self.agent_pos[1] + row + 1][self.agent_pos[0] + col + 1]

                    if val_offset_1 in [1, 2] and val_offset_2 in [1, 2]:
                        break
                    ret[3 + row, 3 + col] = val

        return ret
    
    def direction_to_objective(self):
        """Get the relative direction to the objective. check 3 the primary objective first and then 4 the secondary objective"""
        primary_obj = np.argwhere(self.map == 3)
        #return primary_obj[0], len(primary_obj)
        if len(primary_obj) > 0:
            primary_obj = primary_obj[0]
            return primary_obj[1] - self.agent_pos[0], primary_obj[0] - self.agent_pos[1]
        primary_obj = np.argwhere(self.map == 4)
        primary_obj = primary_obj[0]
        return primary_obj[1] - self.agent_pos[0], primary_obj[0] - self.agent_pos[1]



if __name__ == '__main__':
    # run as python3 -m helpers.advanced_map
    m = AdvancedMap(pos=(5, 24))
    #print(m.map)
    print(m.enemies)
    print(m.agent_pos)
    m.display()
    #m.displayImg()
    print(m.agents_view())
    print(m.direction_to_objective())
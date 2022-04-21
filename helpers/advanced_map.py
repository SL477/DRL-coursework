"""here we define the Advanced Map class"""

from .map import adv_map, key
import numpy as np
from .enemy import Enemy
from .get_available_actions import Action, adv_actions

import matplotlib.pyplot as plt

class AdvancedMap():
    """Advanced map class. Holds an instance of the map. Animates the enemies. Handles actions
    
    Methods:
    reset, reset the map to what it was before & return the observations

    step, send in an Action named tuple to perform the step. Animate the enemies and the agent and send back the reward and other useful info
    
    display, prints a pretty view of the map
    
    displayImg, calls a matplotlib image of the map

    agents_view, returns the immediate surroundings of the agent, ray-traced(ish) out from the agent
    
    direction_to_objective, returns the direction to where the next objective is
    """
    def __init__(self, pos=None) -> None:
        self.map = adv_map()

        # find the enemies and their positions in the 3 time steps (looking for 7 & 8)
        self.enemies = []

        # set other stats
        self.agent_health = 100

        # reset the environment to set it up
        self.reset(pos=pos)

        # set a limit
        self.limit = 200
    
    def reset(self, pos=None) -> dict:
        """the function to reset the map"""
        # as we have changed a load of the values set the map back to what it was
        self.map = adv_map()

        # find the enemies and their positions in the 3 time steps (looking for 7 & 8)
        self.enemies = []
        banned_positions = []
        # enemies who bob up and down
        for i in np.argwhere(self.map == 7.):
            # to be consistent flip the positions around so that all tuples are (x, y)
            epos = [(i[1], i[0] - 1), (i[1], i[0]), (i[1], i[0] + 1)]
            banned_positions += epos
            self.enemies.append(Enemy(epos))
        
        # enemies who bob side to side
        for i in np.argwhere(self.map == 8.):
            epos = [(i[1] - 1, i[0]), (i[1], i[0]), (i[1] + 1, i[0])]
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

        # set a limit
        self.limit = 200

        # return the observations
        return {
            'is_stop': False, 
            'immediate_reward': 0,
            'enemy_count': len(self.enemies), # enemy count
            'agent_view': self.agents_view(), # agent view
            'obj_direction':  self.direction_to_objective(), # direction to objective
            'agent_health': self.agent_health, # agent health
            }
        
    def step(self, action: Action) -> dict:
        """Need to animate the enemies. Perform the action. Return the compass to the objective, update reward, mini-map, etc"""
        # run actions first. If the shoot action has been performed will need to eliminate enemies first
        ret = {'is_stop': False, 'immediate_reward': -1}
        if action.shoot:
            # Shoot
            # Go through the locations of the enemies, if one is within 3 spaces of the agent then remove it from the array
            remove_enemies = []
            for idx, enemy in enumerate(self.enemies):
                # Get the x & y of the enemy
                if enemy.check_if_near_point(self.agent_pos[0], self.agent_pos[1]):
                    remove_enemies.append(idx)
            
            # pop the enemies from the list and update the map value to 0
            for enemy_idx in reversed(remove_enemies):
                remove_enemy = self.enemies.pop(enemy_idx)
                e_x, e_y = remove_enemy.positions[remove_enemy.current_position]
                self.map[e_y][e_x] = 0.0
        else:
            # check if the cell moving to is empty
            new_x, new_y = self.agent_pos
            new_x, new_y = new_x + action.x, new_y + action.y
            val_new_cell = self.map[new_y][new_x]

            val_key = key(advanced=True)
            if val_key[val_new_cell]['solid']:
                # If the new cell is solid then we cannot move there
                new_x, new_y = self.agent_pos
            else:
                # Move to the new position
                # update the map with the old value
                self.map[self.agent_pos[1]][self.agent_pos[0]] = self.old_agent_value
                # store the old value of the new cell
                self.old_agent_value = self.map[new_y][new_x]
                # show on the map we have moved
                self.map[new_y][new_x] = 5.
                # update the agent's position
                self.agent_pos = (new_x, new_y)

                # Sort out rewards
                rew = val_key[val_new_cell]['reward']
                if not np.isnan(rew):
                    ret['immediate_reward'] += rew
                if val_new_cell == 4: #val_key[val_new_cell]['reward'] == 30:
                    # remove the reward point from the map so that it cannot be claimed again
                    self.old_agent_value = 0.
                    # as this is the escape point flag that we should end the session
                    ret['is_stop'] = True
                elif val_new_cell == 3: # val_key[val_new_cell]['reward'] == 50:
                    # if we land on the primary objective then remove it from the map so we cannot claim it again
                    self.old_agent_value = 0.
        
        # enemy movement. Sort out damage to the agent here
        for e_idx in range(len(self.enemies)):
            # get current position
            e_x, e_y = self.enemies[e_idx].positions[self.enemies[e_idx].current_position]
            # get current place in list in case we need to rewind backwards if we hit the player
            e_current_position = self.enemies[e_idx].current_position
            # Take the step
            e_val = self.map[e_y][e_x]
            e_x1, e_y1 = self.enemies[e_idx].step()
            
            if (e_x1, e_y1) == self.agent_pos:
                # We have hit the player so take off the reward
                rew = key(advanced=True)[e_val]['reward']
                if not np.isnan(rew):
                    ret['immediate_reward'] += rew

                # rollback the enemy
                self.enemies[e_idx].current_position = e_current_position
            else:
                # display the enemy moving
                # print('new enemy pos', e_x1, e_y1, e_val, e_x, e_y)
                self.map[e_y1][e_x1] = e_val
                # Update where it was to be zero
                self.map[e_y][e_x] = 0.

        if ret['immediate_reward'] < 0:
            self.agent_health += ret['immediate_reward']
            if self.agent_health <= 0:
                ret['is_stop'] = True
        
        # sort out limit
        self.limit -= 1
        if self.limit < 0:
            ret['is_stop'] = True

        # enemy count
        ret['enemy_count'] = len(self.enemies)

        # agent view
        ret['agent_view'] = self.agents_view()

        # direction to objective
        ret['obj_direction'] = self.direction_to_objective()
        
        # agent health
        ret['agent_health'] = self.agent_health
        return ret

    def display(self) -> None:
        """Show the map in a nice way"""
        # Some trial & error using https://numpy.org/doc/stable/reference/generated/numpy.array2string.html to get rid of the decimal
        print(np.array2string(self.map, formatter={'float_kind': lambda x: "%.0f" % x}))

    def displayImg(self) -> None:
        """Show the map as an image"""
        plt.imshow(self.map)
        plt.title("Advanced map")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
    
    def agents_view(self) -> np.array:
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
                    # if the row is below need to alter if we're looking at the row above or below
                    if row < 0:
                        row_plus_minus = 1
                    else:
                        row_plus_minus = -1
                    # same with the columns
                    if col < 0:
                        col_plus_minus = 1
                    else:
                        col_plus_minus = -1
                    val_offset_1 = self.map[self.agent_pos[1] + row][self.agent_pos[0] + col + col_plus_minus]
                    val_offset_2 = self.map[self.agent_pos[1] + row + row_plus_minus][self.agent_pos[0] + col + col_plus_minus]

                    
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

                    # if the row is below need to alter if we're looking at the row above or below
                    if row < 0:
                        row_plus_minus = 1
                    else:
                        row_plus_minus = -1
                    # same with the columns
                    if col < 0:
                        col_plus_minus = 1
                    else:
                        col_plus_minus = -1
                    
                    #val_offset_1 = self.map[self.agent_pos[1] + row - 1][self.agent_pos[0] + col]
                    #val_offset_2 = self.map[self.agent_pos[1] + row + 1][self.agent_pos[0] + col + 1]
                    if self.agent_pos[1] + row - row_plus_minus < len(self.map):
                        val_offset_1 = self.map[self.agent_pos[1] + row - row_plus_minus][self.agent_pos[0] + col]
                    else:
                        val_offset_1 = 0.
                    if self.agent_pos[1] + row + row_plus_minus < len(self.map):
                        val_offset_2 = self.map[self.agent_pos[1] + row + row_plus_minus][self.agent_pos[0] + col + col_plus_minus]
                    else:
                        val_offset_2 = 0.

                    if val_offset_1 in [1, 2] and val_offset_2 in [1, 2]:
                        break
                    ret[3 + row, 3 + col] = val

        return ret
    
    def direction_to_objective(self) -> tuple:
        """Get the relative direction to the objective. check 3 the primary objective first and then 4 the secondary objective"""
        primary_obj = np.argwhere(self.map == 3)
        #return primary_obj[0], len(primary_obj)
        if len(primary_obj) > 0:
            primary_obj = primary_obj[0]
            return primary_obj[1] - self.agent_pos[0], primary_obj[0] - self.agent_pos[1]
        primary_obj = np.argwhere(self.map == 4)
        primary_obj = primary_obj[0]
        return primary_obj[1] - self.agent_pos[0], primary_obj[0] - self.agent_pos[1]
    
    def convert_observations(self, obs: dict): #-> tuple(np.array, int, bool):
        """Convert the observations from step's dictionary into an array of the agent's view, the reward for the round and whether or not to stop
        
        The dictionary contains:
    is_stop: a boolean, used internally to determine whether to stop the episode
    immediate_reward: the points we got in the last round
    enemy_count: how many active enemies there are
    agent_view: the 7x7 view of the surroundings (values between 0-8)
    obj_direction: the relative direction to the objective (0-max width, 0-max height)
    agent_health: the health of the agent, between 0-100"""

        # sort out the relative coordinates, so that the directions are divided by the size of the environment
        obj_direction = np.divide(np.array(list(obs['obj_direction'])), np.array([21., 29.])) # TODO dynamically get the size

        # normalise the view of the surroundings
        # use ravel to reshape into a 1 row list and normalise it
        agent_view = obs['agent_view'].ravel() / 8.

        # enemy_count
        enemy_count = np.array(obs['enemy_count'] / 3.) # TODO dynamically get the max number of enemies

        # agent_health
        agent_health = np.array(obs['agent_health'] / 100.)

        # concatenate into a single numpy array, 1 row, 2 + 49 + 1 + 1 = 53 columns between -1 & 1
        return np.concatenate([obj_direction, agent_view, [enemy_count], [agent_health]]), obs['immediate_reward'], obs['is_stop']

if __name__ == '__main__':
    # run as python3 -m helpers.advanced_map
    m = AdvancedMap(pos=(5, 8)) # 24
    #print(m.map)
    print(m.enemies)
    print(m.agent_pos)
    m.display()
    #m.displayImg()
    print(m.agents_view())
    print(m.direction_to_objective())

    # perform an action
    #print("---SHOOT---")
    #print(m.step(adv_actions()['shoot']))
    #print("---LEFT---")
    #print(m.step(adv_actions()['left']))
    print("---Up---")
    print(m.step(adv_actions()['up']))
    m.display()
    print("---Up---")
    print(m.step(adv_actions()['up']))
    m.display()
    print("---Up---")
    print(m.step(adv_actions()['up']))
    m.display()
    print("---Left---")
    print(m.step(adv_actions()['left']))
    m.display()

    # manual testing
    while True:
        # get the user's input
        inp = input("Press a direction or space: ")

        # test the input, map to actions and quit if no match
        if inp == "a":
            print('--LEFT--')
            print(m.step(adv_actions()['left']))
            m.display()
            print('Agent position:',m.agent_pos)
        elif inp == 'w':
            print('--UP--')
            print(m.step(adv_actions()['up']))
            m.display()
            print('Agent position:',m.agent_pos)
        elif inp == 's':
            print('--DOWN--')
            print(m.step(adv_actions()['down']))
            m.display()
            print('Agent position:',m.agent_pos)
        elif inp == 'd':
            print('--RIGHT--')
            print(m.step(adv_actions()['right']))
            m.display()
            print('Agent position:',m.agent_pos)
        elif inp == ' ':
            print("---SHOOT---")
            print(m.step(adv_actions()['shoot']))
            m.display()
            print('Agent position:',m.agent_pos)
        else:
            # Quit text which seemed like a good idea at the time
            print("Goodbye")
            break
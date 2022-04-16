# DRL-coursework

Deep Reinforcement Learning Coursework

## Basic task

### The story version

Fired from a Solar Federation Space Force Infiltrator, our intrepid Space Marine Commando robot exits its boarding pod in a random place in the Custodian warship. Its mission is to cripple the ship's reactor before its crew are revived from stasis by planting a timed explosive on it. Its survival is optional, after it has completed its mission the robot can escape back to where a shuttle has cut a hole into the ship to retrieve it. But if the robot is destroyed, well we can always build more robots.

### The code version

![Basic Map](img/basic_map.png)

Here we are using Q-learning to get an agent to solve the above map. The Light Green point is the ultimate goal and exit point. The dark green point is the point of highest reward, but can only be claimed once. The yellow points are traps which will cause damage. The blue points are doors which don't do anything. The light purple points are walls (for simplicity they are excluded from the below graph). The dark purple points are empty space which the agent can walk over.

![Basic Map Graph](img/basic_map_graph.png)

This graph shows which points on the map are available from the others.

## Advanced task

Here our agent lands on a bigger spaceship and has to take out the reactor and then escape, while dodging traps and enemies.

![Advanced Map](img/advanced_map.png)

### No improvements (basic DQN)

<video src="videos/NoImprovement.mp4" />

### DoubleQ

<video src="videos/DoubleQ.mp4" />

### Prioritised Replay

<video src="videos/PrioritisedReplay.mp4" />

### Both

<video src="videos/Both.mp4" />

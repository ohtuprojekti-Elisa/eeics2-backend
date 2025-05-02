# PlayerManager
## Role
In charge of receiving and setting player data. Also "Managing" the player objects.

### Game object fetching and updating
The PlayerManager script initializes the object pools for the players and has a list of gameobjects currently alive.
When the script receives player data it first creates the players by fetching a gameobject from the pool and puts it on a list.
Then it simply sets the values for the Player script in the gamobjects.

This is done for every player in the received data.

### Death handling
If a player is on gameobject list, but not on the "alive" list, meaning there is a gameobject stored in the list which is not receiving data at the moment, means that player has died.

The player manager handles this by setting the player objects state.

There is no handling for players leaving the game, they would likely just show up dead on the map.

### Team switching handling
This script does notice if the player switches teams and tries to switch the prefab used by the gameobject. The implementation is a bit buggy, with lasers not being attached to the new prefab.

# Player
## Role
In charge of the individual players state.

### Movement handling
Smoothly moves itself from previous position to new position set to it.

### Animations
The player scipt has animation related booleans given to it which it relegates to the animation controller.

### Directional movement
Does calculations to check which direction the player is moving in relation to where the player is aiming. This info is relegated to, and used by the animation controller.

### Player text
Handles modifying the text above the players head to correct values. (Team color, name and current health)

### Bleed effect
If the bleed effect is not commented, you should do so or remove it. It should be handled by decals coupled with an effect. This was used before anything like that was implemented.

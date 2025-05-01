# Current status

`void UpdateAnimation(...)``
- Updates all animation states based on the player's current state.

### Parameters:

| Parameter              | Type  | Description                        | Status          | Avatar Mask     |
|------------------------|-------|------------------------------------|-----------------|-----------------|
| `isDead`               | Bool  | Player is dead                     | ✅ Working      | Both            |
| `isJumping`            | Bool  | Player is jumping                  | ✅ Working      | LowerBody       |
| `isDucking`            | Bool  | Player is crouching                | ✅ Working      | LowerBody       |
| `isWalking`            | Bool  | Player is walking                  | ✅ Working      | LowerBody       |
| `isPistol`             | Bool  | Holding a pistol                   | ✅ Working      | UpperBody       |
| `isRifle`              | Bool  | Holding a rifle                    | ✅ Working      | UpperBody       |
| `isKnife`              | Bool  | Holding a knife                    | ✅ Working      | UpperBody       |
| `isWalkingForward`     | Bool  | Walking forward                    | ✅ Working      | LowerBody       |
| `isWalkingBackward`    | Bool  | Walking backward                   | ✅ Working      | LowerBody       |
| `isWalkingLeft`        | Bool  | Walking left                       | ✅ Working      | LowerBody       |
| `isWalkingRight`       | Bool  | Walking right                      | ✅ Working      | LowerBody       |
| `isRunningForward`     | Bool  | Running forward                    | ✅ Working      | LowerBody       |
| `isRunningBackward`    | Bool  | Running backward                   | ✅ Working      | LowerBody       |
| `isRunningLeft`        | Bool  | Running left                       | ✅ Working      | LowerBody       |
| `isRunningRight`       | Bool  | Running right                      | ✅ Working      | LowerBody       |
| `isMoving`             | Bool  | Any movement                       | ✅ Working      | LowerBody       |
| `isRunning`            | Bool  | Player is running                  | ✅ Working      | LowerBody       |
| `isSMG`                | Bool  | Holding a SMG                      | 🔄 Planned      | UpperBody       |
| `isShotgun`            | Bool  | Holding a shotgun                  | 🔄 Planned      | UpperBody       |
| `isSniper`             | Bool  | Holding a sniper                   | 🔄 Planned      | UpperBody       |
| `isHeavy`              | Bool  | Holding a heavy weapon             | 🔄 Planned      | UpperBody       |
| `isDuckingLeft`        | Bool  | Crouchwalking left                 | 🔄 Planned      | LowerBody       |
| `isDuckingRight`       | Bool  | Crouchwalking right                | 🔄 Planned      | LowerBody       |
| `isDuckingBackwards`   | Bool  | Crouchwalking backwards            | 🔄 Planned      | LowerBody       |
| `isStabbing`           | Bool  | Player stabbing                    | 🔄 Planned      | UpperBody       |
| `isDual`               | Bool  | Holding dual pistols               | 🚫🔄 Animation missing | UpperBody |
| `isPlanting`           | Bool  | Planting the bomb                  | ❌ Not working  | UpperBody       |
| `isDefusing`           | Bool  | Defusing the bomb                  | ❌ Not working  | UpperBody       |
| `isGrenade`            | Bool  | Holding a grenade                  | ❌ Not working  | UpperBody       |
| `isBomb`               | Bool  | Holding the bomb                   | ❌ Not working  | UpperBody       |

✅ = Working as planned
❌ = Broken (used to work)
🔄 = Planned, partial support exists
🚫 = Animation not found from CS2 files

**Note:** Diagonal movement animations exist in CS2 (e.g., NE, SW), so implementing them is possible.

Here is a list of weapons and their categories: [weapons.md](weapons.md)

## Private Coroutines
Used to delay the deactivation of animations for smoother transitions.

`IEnumerator StopMovingWithDelay()`
- Disables isMoving if the player has stopped moving after stopDelay.

`IEnumerator StopRunningWithDelay()`
- Disables isRunning after delay if the player is not running and has stopped.

`IEnumerator StopWalkingWithDelay()`
- Resets all walking directional states after delay if movement stops.

`IEnumerator StopRunningDirectionsWithDelay()`
- Resets all running directional states if no movement is detected after delay.

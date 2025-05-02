# Manager
## It's a singleton

"Singleton is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance."

https://refactoring.guru/design-patterns/singleton

## Yes but why
### Handy dandy place for often used things
You don't want to do the same thing over and over, for example:

Many things in this project need to be scaled with the 3D map. It would be nice if unity did this with its hierarchy ( because child objects move and scale with their parent objects ), but it's not that simple in this project.

We get coordinates from the parser for the players and need to place them on the map in a way that makes sense; correct positioning, rotation and scale.

So we have to calculate this for anything and everything that is in the 3D map (players, grenades, effects, decals, etc.).

The singleton checks for scale changes and has the magic code the last team wrote for scale and position calculations (not sure how it works, but it works), so you can simply have the singleton do it from anywhere in the codebase rather than writing it again and again.

Its also a good place to store values you need in many different places like lerpDuration and the map transform which were seperately apart of most scripts before.

## What it does

- Checks for scale changes
- Returns a correct position for objects when given xyz coordinates and a parent object
- Can return a boolean if a new round has started that frame. So if true, you know the previous round ended (useful for resetting things)
- Can return lerpDuration, a value used for the duration you lerp for ( smoothing from a to b ).
- Can return the map transform. The point was to not NEED the map anymore and instead use the singleton, but it's used like this somewhere in the code.

## How to use
For example, to get the lerpDuration:

![image](https://github.com/user-attachments/assets/a683089a-da4a-4755-828d-1d3c38558282)

You can do this anywhere in the code.

Heres the grenade position calculation:

![image](https://github.com/user-attachments/assets/0eb18f25-7633-450b-b5f3-8e23f6333a76)

So "Manager.Instance" followed by method from the manager.

## Introduced late
The singleton/manager is somewhat underutilized, as it was not always in use. Some parts of the code use it while others don't.

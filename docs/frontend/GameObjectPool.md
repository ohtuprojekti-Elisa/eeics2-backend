# GameObjectPool
## It's the object pool pattern

"Improve performance and memory use by reusing objects from a fixed pool instead of allocating and freeing them individually."

https://gameprogrammingpatterns.com/object-pool.html

## Why
Destroying and instantiating gameobjects creates unnecessary performance overhead.

## How it works

![image](https://github.com/user-attachments/assets/735393fe-0ca7-4358-b470-135064efb950)

The GameObjectPool has a gameobject, parent for the gameobject/s and a queue to store the gameobjects in.

When a pool is created it's given a gameobject, it's parent and an initial size for the pool. The pool is then filled with the given gameobject until given initial size.

Example from the PlayerManager script:

![image](https://github.com/user-attachments/assets/b1805cc6-a9b3-4a5f-855f-2a81a580c8fa)

![image](https://github.com/user-attachments/assets/7dc36909-9e3f-4d17-8d7e-de8da125bd54)

So 5 gameobjects for both teams with the parent object being whatever the PlayerManager script is attached to.

Instead of instantiating gameobjects, you get them from the pool:

![image](https://github.com/user-attachments/assets/21352924-1c46-47f5-8d4d-67839659a2c6)

Instead of destroying gameobjects you return them to the pool:

![image](https://github.com/user-attachments/assets/a0ea4dd9-9803-4d81-af49-1c58418e7ce7)

# About initial size

You want the initial size to be as close to the number of gameobjects you will ever need as possible, because when the pool is empty and you try to get a gameobject from it, a new one will be created.

However this way the pool will naturally have as many gameobjects as you need eventually, and new ones won't be created.

# Other methods

- public GameObject GetFromPoolWithInitialPosition(Vector3 position)

  Does what it says
- public System.Collections.IEnumerator ReturnAfterDelay(GameObject obj, float delay)

  Does what it says, but has to be called with StartCoroutine()
- private void AddObjectToPool()

  The GameObjectPool uses this to add to the queue when it's initializing or empty

# Introduced late

Object pooling might not be used everywhere sensibly.
Much of the code was written before object pooling, so it might not work as expected. For example when players change teams, it's buggy, because the lasers were written without pooling in mind.
Team switching might have other issues too, we didn't have time to test it much, seeing as it doesn't happen too often.

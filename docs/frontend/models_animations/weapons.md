# Weapons

1. Select the character prefab: `Animation/animations/Phoenix.prefab` or `Animation/animations/FBI/FBI.prefab`.

2. Create a prefab from the weapon if it doesn't already exist (makes it easier to copy the weapon to other characters):
  * Drag the weapon into the hierarchy, then drag it back into the "Projects" panel — this will create e.g. `deagle.prefab`.
  * Name the prefab according to the list below.

3. Move the weapon (prefab) into the character's `weaponHolder`.

  * Paste the following transform settings into the weapon (prefab). Depending on the weapon, you might need to fine-tune its position (the placement isn't always perfect).

Weapon in hand:
```bash
UnityEditor.TransformWorldPlacementJSON:{"position":{"x":0.005505432840436697,"y":0.010460630059242249,"z":-0.00005298554606270045},"rotation":{"x":-0.5549819469451904,"y":-0.0638723075389862,"z":-0.3035511374473572,"w":-0.7718632221221924},"scale":{"x":0.009999999776482582,"y":0.009999999776482582,"z":0.009999999776482582}}
```
* Select the weapon in the hierarchy. In the Inspector, click the three dots on the right side of the Transform component -> Paste -> World Transform.
* Check in the scene that the weapon is in the character's hand and correctly scaled.
* If you still see the previous weapon in the character's hand, you can hide it by clicking the weapon in the hierarchy and unchecking its checkbox in the Inspector.

4. In `Animation/prefab/` you will find `firePoint.prefab` and `MuzzleFlashPoint.prefab`. Move these into the weapon in the hierarchy.

5. Add the following components to the weapon (prefab): `Gun Script` and `Weapons`
  * In `Weapons`, select the category the weapon belongs to (important for correct animations to be applied!).

---

### Weapon List:

1. **AK-47 / Rifle | Phoenix/FBI |**
2. **AUG / Rifle | Phoenix/FBI |**
3. **AWP / Sniper | Phoenix/FBI |**
4. **PP-Bizon / SMG | Phoenix/FBI |**
5. **C4 / Bomb | Phoenix |**
6. **Desert Eagle / Pistol | Phoenix/FBI |**
7. Decoy Grenade / Grenade
8. Dual Berettas / Dual Pistols (Animation missing)
9. **FAMAS / Rifle | Phoenix/FBI |**
10. **Five-SeveN / Pistol | Phoenix/FBI |**
11. Flashbang / Grenade
12. **G3SG1 / Rifle | Phoenix/FBI |**
13. **Galil AR / Rifle | Phoenix/FBI |**
14. **Glock-18 / Pistol | Phoenix/FBI |**
15. HE Grenade / Grenade
16. **P2000 / Pistol | Phoenix/FBI |**
17. Incendiary Grenade / Grenade
18. **M249 / Heavy | Phoenix/FBI |**
19. **M4A4 / Rifle | Phoenix/FBI |**
20. **MAC-10 / SMG | Phoenix/FBI |**
21. **MAG-7 / Shotgun | Phoenix/FBI |**
22. Molotov / Grenade
23. **MP7 / SMG | Phoenix/FBI |**
24. **MP5-SD / SMG | Phoenix/FBI |**
25. **MP9 / SMG | Phoenix/FBI |**
26. **Negev / Heavy | Phoenix/FBI |**
27. **Nova / Shotgun | Phoenix/FBI |**
28. **P250 / Pistol | Phoenix/FBI |**
29. **P90 / SMG | Phoenix/FBI |**
30. **Sawed-Off / Shotgun | Phoenix/FBI |**
31. **SCAR-20 / Sniper | Phoenix/FBI |**
32. **SG 553 / Rifle | Phoenix/FBI |**
33. Smoke Grenade / Grenade
34. **SSG 08 / Sniper | Phoenix/FBI |**
35. **Zeus x27 / Pistol | Phoenix/FBI |**
36. **Tec-9 / Pistol | Phoenix/FBI |**
37. **UMP-45 / SMG | Phoenix/FBI |**
38. **XM1014 / Shotgun | Phoenix/FBI |**
39. **M4A1 / Rifle | Phoenix/FBI |**
40. **CZ75 Auto / Pistol | Phoenix/FBI |**
41. **USP-S / Pistol | Phoenix/FBI |**
42. **R8 Revolver / Pistol | Phoenix/FBI |**
43. Kevlar Vest / ---
44. Kevlar + Helmet / ---
45. **Defuse Kit / FBI |**
46. **Knife / Knife | Phoenix/FBI |**

**Bolded** weapons have been added to both characters.

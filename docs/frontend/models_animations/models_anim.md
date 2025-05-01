# Models and animations

- Characters, animations, and weapons are exported directly from CS2 using [Source2Viewer](https://valveresourceformat.github.io/)
  - ./Steam/steamapps/common/Counter-Strike Global Offensive/game/csgo/pak01_dir.vpk
    - characters/models
    - weapons/models

- Exported files are converted to .fbx format (Unity compatible) using [Blender](https://www.blender.org/)

# Export settings in Blender for .FBX format:
## For weapons:

- Path mode: **Copy + Embedded textures**
- Enable the following options:
  - [x] Selected Objects
  - Object Types:
    - [x] Armature
    - [x] Mesh
  - Apply Transform:
    - [x] Apply Scale
    - [x] Apply Rotation
    - [x] Apply Location
  - [x] Only Deform Bones
  - [x] Animation
  - [x] Key All Bones
  - [x] Force Start/End Keying

## For animations without mesh:

- Object Types:
  - [x] Armature
- Transform:
  - [x] Apply Scale
  - [x] Apply Rotation
  - [x] Apply Location
- [x] Only Deform Bones
- [x] Animation
- [x] Key All Bones
- [x] Force Start/End Keying
- Name the animation based on the model you want to inherit the mesh from: `inheritedmesh@animationname.fbx`
- In Unity, under the Model settings, enable **Preserve Hierarchy** for both the animation and the mesh

### Direction indicators related to movement animation:
- **n** = forward
- **s** = backward
- **w** = left
- **e** = right

# Current status of animations:

## Animations are set up so that leg movements use a separate Avatar Mask (**LowerBodyMask**).

**Character movement:**
- Walk: forward, backward, left, and right
- Run: forward, backward, left, and right
- Crouch: forward
- Jump: forward
- Idle

*Each of these has its own animation for every direction.*

## Upper body animations use a separate Avatar Mask (**UpperBodyMask**).

**Weapons**
- Each weapon type has been assigned its own category (`Weapons` script), which has been set for each weapon (makes it easier to add animations for different weapon types):
  - Knife
  - Pistols
  - Rifles (currently all other weapons use the rifle animation)
- Categories without animations assigned to characters:
  - SMG
  - Shotgun
  - Sniper
  - Heavy
  - Grenade
  - DualPistols (no animations found in CS2?)
  - Bomb (was working previously, but seems to have broken)

## Using both Avatar Masks:
- Death

# JSON specification

```json
{
    "tick": 43295,
    "round_time": 676.484349952,
    "round_start": false,
    "switch": false,
    "is_freeze": false,
    "is_halftime": false,
    "t": "HEROIC",
    "ct": "Nemiga Gaming",
    "t_wins": 5,
    "ct_wins": 1,
    "players": [
        {
            "sid": 76561198837117408,
            "name": "1eeR",
            "clan": "Nemiga Gaming",
            "team": "CT",
            "hp": 100,
            "money": 2200,
            "x": -263.2647705078125,
            "y": -2178.990478515625,
            "z": -171.13677978515625,
            "view_x": 58.327454,
            "view_y": 0.087890625,
            "actv_itm": "Five-SeveN",
            "items": ["Knife", "Five-SeveN"],
            "helmet": false,
            "armor": 100,
            "kit": false,
            "is_ducking": false,
            "is_walking": true,
            "is_standing": true,
            "is_air": false,
            "is_rld": false,
            "kills": 0,
            "deaths": 6,
            "assists": 1,
            "dmg": 101,
            "adr": 16.833333333333332,
            "is_planting": false,
            "is_defusing": false
        }
    ],
    "shooting": [76561198837117408],
    "kills": [
        {
            "killer": "tN1R",
            "victim": "khaN",
            "weapon": "AK-47",
            "is_hs": false,
            "penetrations": 0
        }
    ],
    "nades": [
        {
            "id": 7556250935960765521,
            "type": "Smoke Grenade",
            "x": -1165.15625,
            "y": -632.09375,
            "z": -165.96875,
            "team": "T"
        }
    ],
    "infernos": [
        {
            "id": 2093783464307243804,
            "fires":
                [
                    {
                        "x": -1037.0762939453125,
                        "y": -680.146484375,
                        "z": -261.96875
                    },
                    {
                        "x": -988.7138061523438,
                        "y": -629.1102294921875,
                        "z": -288
                    }
                ]
        }
    ],
    "nade_event": {
        "type": "HE Grenade",
        "x": 292.2667541503906,
        "y": -388.44927978515625,
        "z": -66.32966613769531
    },
    "bomb": {
        "carrier": "SunPayus",
        "x": 392.8011474609375,
        "y": 336.8455810546875,
        "z": -251.96875,
        "planted": false,
        "defused": false,
        "exploded": false,
        "planted_by": "",
        "defused_by": ""
    }
}
```
Parser library: https://github.com/markus-wa/demoinfocs-golang

A good reference project using demoinfocs-golang:
https://github.com/Linus4/csgoverview

## Data
The JSON data consists of individual server ticks in a list. 

**NOTE**: In Unity the coordinate values Y and Z are FLIPPED. (Easy to fix by flipping the values in the [parser](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/blob/main/backend/demodata_parser/go_src/demoparser.go))

## tick (list)

- **tick**: current in-game server tick
- **round_time**: *actually* the total time elapsed (seconds) since the start of the demo
- **round_start**: has round started during this tick
- **switch**: have teams switched
- **is_freeze**: is the buy phase active
- **is_halftime**: NEEDS TO BE REMOVED
- **t**: clan name playing as terrorists
- **ct**: clan name playing as counter terrorists
- **t_wins**: terrorist wins (will be swapped when teams are swapped)
- **ct_wins** counter terrorist wins (will be swapped when teams are swapped)

## players (list)

- **sid**: player steam id
- **name**: player steam name
- **clan**: player clan name
- **team**: current team side
- **xyz**: player's coordinates
- **view_x, view_y**: player's view direction
- **actv_itm**: currently active item (string)
- **items**: current items (list of strings)
- **helment**: does the player have a helmet
- **armor**: current armor rate
- **kit**: does the player have a defuse kit
- **is_ducking**: is the player currently crouching
- **is_walking**: NEEDS TO BE REMOVED
- **is_standing**: is the player standing
- **is_air**: is the player airborne
- **is_rld**: is the player reloading
- **kills**: total kills during match
- **deaths**: total deaths during match
- **assists**: total assists during match
- **dmg**: total damage during match
- **adr**: average damage per round
- **is_planting**: is the player planting the bomb
- **is_defusing**: is the player defusing the bomb

## shooting (list) (can be null)
The steam id of the player currently shooting

## kills (list) (can be null)

- **killer**: killer name
- **victim**: victim name
- **weapons**: weapon name
- **is_hs**: was the kill a headshot
- **penetrations**: number of penetrations through objects

## nades (list) (can be null)
Currently active grenades

- **id**: unique grenade id
- **type**: grenade type (string)
- **xyz**: grenade coordinates
- **team**: thrower team (T or CT)

## infernos (list) (can be null)
Infernos are the fire effects created by molotovs and incendiaries. New (individual) fires are created periodically as the fire effect spreads.

- **id**: unique inferno id
- **fires**: individual fires within an inferno
    - **xyz**: fire coordinates

## nade_event (can be null)
Signals a nade explosion (HE Grenades, Flashbangs, Smokes, Decoys but not molotovs/incendiaries)

- **type**: grenade/detonation type (same as nade type)
- **xyz**: grenade coordinates

## bomb
Bomb data

- **carrier**: name of the player carrying the bomb
- **xyz**: bomb coordinates
- **planted**: has the bomb been planted
- **defused**: has the bomb been defused
- **exploded**: has the bomb exploded
- **planted_by**: name of the player who planted the bomb (will be an empty string if bomb has not been planted)
- **defused_by**: name of the player who defused the bomb (will be an empty string if bomb has not been defused)


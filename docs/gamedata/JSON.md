# JSON-datan määrittely

```json
{
    "tick_rate": 64,
    "total_ticks": 181027,
    "map_name": "de_mirage",
    "ticks": [
                {
                "tick": 3700,
                "round_started": false,
                "t": "HEROIC",
                "ct": "Nemiga Gaming",
                "t_wins": 0,
                "ct_wins": 0,
                "players": [
                    {
                    "sid": 76561198178209109,
                    "name": "xfl0ud",
                    "clan": "HEROIC",
                    "team": "T",
                    "hp": 100,
                    "money": 150,
                    "x": -1969.03125,
                    "y": 450.0319519042969,
                    "z": -159.96875,
                    "view_x": -110.34256,
                    "view_y": 6.864044,
                    "actv_itm": "C4",
                    "items": [
                        "Knife",
                        "Glock-18",
                        "C4"
                    ],
                    "helmet": false,
                    "armor": 100,
                    "kit": false,
                    "is_ducking": true,
                    "is_walking": false,
                    "is_air": false,
                    "is_rld": false,
                    "kills": 0,
                    "deaths": 0,
                    "assists": 0,
                    "dmg": 0,
                    "adr": 0,
                    "is_planting": true,
                    "is_defusing": false
                    }
                ],
                "bomb": {
                    "carrier": "xfl0ud",
                    "x": -1969.03125,
                    "y": 450.0319519042969,
                    "z": -159.96875,
                    "bomb_planted": {
                    "planted": false,
                    "planter": ""
                    },
                    "bomb_defused": {
                    "defused": false,
                    "defuser": ""
                    },
                    "exploded": false
                },
                "kills": [
                    {
                    "killer": "tN1R",
                    "victim": "Xant3r",
                    "weapon": "Glock-18",
                    "is_headshot": true,
                    "penetrations": 0
                    }
                ],
                "nades": [
                    {
                    "type": "Smoke Grenade",
                    "x": -1022.90625,
                    "y": 189.5,
                    "z": -170.875,
                    "team": "T"
                    },
                    {
                    "type": "Smoke Grenade",
                    "x": -1908.875,
                    "y": -377.5,
                    "z": -165.96875,
                    "team": "T"
                    }
                ],
                "shooting": [
                    76561198872013168
                ],
                "smoke_events": [
                    {
                    "x": -1983.35791015625,
                    "y": 406.50048828125,
                    "z": -157.96875
                    }
                ],
                "infer_events": [
                    {
                    "x": -338.1795959472656,
                    "y": -1576.703125,
                    "z": -168
                        }
                    ],
                "decoy_events": null
                }
            ]
} 
```
## ticks
Sisältää listan tickeistä. Kukin tick sisältää sen aikana tapahtuneen pelidatan. 

**round_started**: Näyttää tarkalleen missä tickissä kierros alkoi.

## players
Lista pelaajista ja niiden datasta.

**is_ducking**: Onko pelaaja kyykyssä.\
**is_air**: Onko pelaaja ilmassa.\
**is_rld**: Lataako pelaaja asettaan.

## bomb
Pommin data.

**exploded**: "true" näyttää missä tickissä pommi räjähti, muulloin "false".

## kills
Näyttää tickin aikana tapahtuneen pelaajatapon.

## nades
Näyttää aktiiviset kranaatit.

## shooting
Näyttää tickin aikana ampuvat pelaajat (pelkkä steam id).

## smoke_events
Näyttää listan tickin aikana lauenneista savukranaateista (koordinaatit) (savun aika täytyy laskea Unityssa toistaiseksi).

## infer_events
Näyttää listan tickin aikana lauenneista tulikranaateista (koordinaatit) (tulen aika täytyy laskea Unityssa toistaiseksi).

## decoy_events
Näyttää listan tickin aikana lauenneista decoy-kranaateista (koordinaatit) (decoyn aika täytyy laskea Unityssa toistaiseksi).

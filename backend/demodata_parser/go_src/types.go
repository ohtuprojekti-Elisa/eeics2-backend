package main

type HeaderData struct {
	TickRate   float64 `json:"tickrate"`
	TotalTicks int     `json:"total_ticks"`
	MapName    string  `json:"map_name"`
}

type Player struct {
	SteamID     uint64   `json:"sid"`
	Name        string   `json:"name"`
	Clan        string   `json:"clan"`
	Team        string   `json:"team"`
	Health      int      `json:"hp"`
	Money       int      `json:"money"`
	X           float64  `json:"x"`
	Y           float64  `json:"y"`
	Z           float64  `json:"z"`
	ViewX       float32  `json:"view_x"`
	ViewY       float32  `json:"view_y"`
	ActvItm     string   `json:"actv_itm"`
	Items       []string `json:"items"`
	Helmet      bool     `json:"helmet"`
	Armor       int      `json:"armor"`
	Kit         bool     `json:"kit"`
	IsDucking   bool     `json:"is_ducking"`
	IsWalking   bool     `json:"is_walking"`
	IsStanding  bool     `json:"is_standing"`
	MadeFtstp   bool     `json:"made_ftstp"`
	IsAirborne  bool     `json:"is_air"`
	IsReloading bool     `json:"is_rld"`
	Kills       int      `json:"kills"`
	Deaths      int      `json:"deaths"`
	Assists     int      `json:"assists"`
	DMG         int      `json:"dmg"`
	ADR         float64  `json:"adr"`
	IsPlanting  bool     `json:"is_planting"`
	IsDefusing  bool     `json:"is_defusing"`
}

type Kill struct {
	Killer            string `json:"killer"`
	Victim            string `json:"victim"`
	Weapon            string `json:"weapon"`
	IsHeadshot        bool   `json:"is_hs"` // updated
	PenetratedObjects int    `json:"penetrations"`
}

type Nade struct {
	ID   int64   `json:"id"`
	Type string  `json:"type"`
	X    float64 `json:"x"`
	Y    float64 `json:"y"`
	Z    float64 `json:"z"`
	Team string  `json:"team"`
}

type Bomb struct {
	Carrier     string      `json:"carrier"`
	X           float64     `json:"x"`
	Y           float64     `json:"y"`
	Z           float64     `json:"z"`
	BombPlanted BombPlanted `json:"planted"` // updated
	BombDefused BombDefused `json:"defused"` // updated
	Exploded    bool        `json:"exploded"`
}

type BombPlanted struct {
	Planted bool   `json:"planted"`
	Planter string `json:"planter"`
}

type BombDefused struct {
	Defused bool   `json:"defused"`
	Defuser string `json:"defuser"`
}

type Header struct {
	DemoHeader DemoInfo `json:"demo_info"`
}

type Ticks struct {
	AllTicks []Tick `json:"ticks"`
}

type DemoInfo struct {
	TickRate   float64 `json:"tick_rate"`
	TotalTicks int     `json:"total_ticks"`
	MapName    string  `json:"map_name"`
}

type HeEvent struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type FlashEvent struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type FireEvent struct {
	ShooterID uint64 `json:"sid"`
}

type SmokeEvent struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type InfernoEvent struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type DecoyEvent struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type Tick struct {
	Tick          int            `json:"tick"`
	RoundStarted  bool           `json:"round_start"`
	TeamT         string         `json:"t"`
	TeamCT        string         `json:"ct"`
	TWins         int            `json:"t_wins"`
	CTWins        int            `json:"ct_wins"`
	Players       []Player       `json:"players"`
	Bomb          Bomb           `json:"bomb"`
	Kills         []Kill         `json:"kills"`
	Nades         []Nade         `json:"nades"`
	FireEvents    []uint64       `json:"shooting"`
	HeEvents      []HeEvent      `json:"he_events"`
	FlashEvents   []FlashEvent   `json:"flash_events"`
	SmokeEvents   []SmokeEvent   `json:"smoke_events"`
	InfernoEvents []InfernoEvent `json:"infer_events"`
	DecoyEvents   []DecoyEvent   `json:"decoy_events"`
}

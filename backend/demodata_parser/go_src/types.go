package main

type HeaderData struct {
	TickRate   float64 `json:"tickrate"`
	TotalTicks int     `json:"total_ticks"`
	MapName    string  `json:"map_name"`
	RoundTime  float64 `json:"round_time"`
	FreezeTime float64 `json:"freeze_time"`
	BombTime   float64 `json:"bomb_time"`
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

type Inferno struct {
	ID    int64  `json:"id"`
	Fires []Fire `json:"fires"`
}

type Fire struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

type Bomb struct {
	Carrier   string  `json:"carrier"`
	X         float64 `json:"x"`
	Y         float64 `json:"y"`
	Z         float64 `json:"z"`
	Planted   bool    `json:"planted"`
	Defused   bool    `json:"defused"`
	Exploded  bool    `json:"exploded"`
	PlantedBy string  `json:"planted_by"`
	DefusedBy string  `json:"defused_by"`
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

type NadeEvent struct {
	Type string  `json:"type"`
	X    float64 `json:"x"`
	Y    float64 `json:"y"`
	Z    float64 `json:"z"`
}

type Tick struct {
	Tick           int        `json:"tick"`
	RoundTime      float64    `json:"round_time"`
	RoundStarted   bool       `json:"round_start"`
	TeamSideSwitch bool       `json:"switch"`
	IsFreezeTime   bool       `json:"is_freeze"`
	IsHalfTime     bool       `json:"is_halftime"`
	TeamT          string     `json:"t"`
	TeamCT         string     `json:"ct"`
	TWins          int        `json:"t_wins"`
	CTWins         int        `json:"ct_wins"`
	Players        []Player   `json:"players"`
	ShootingEvents []uint64   `json:"shooting"`
	Kills          []Kill     `json:"kills"`
	Nades          []Nade     `json:"nades"`
	Infernos       []Inferno  `json:"infernos"`
	NadeEvent      *NadeEvent `json:"nade_event"`
	Bomb           Bomb       `json:"bomb"`
}

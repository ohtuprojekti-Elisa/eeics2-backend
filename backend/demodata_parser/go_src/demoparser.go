package main

/*
#include <stdlib.h>
#include <stdbool.h>
*/
import "C"

import (
	"encoding/json"
	"log"
	"os"

	demoinfocs "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs"
	common "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/common"
	events "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/events"
)

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

type DemoData struct {
	TickRate   float64 `json:"tick_rate"`
	TotalTicks int     `json:"total_ticks"`
	MapName    string  `json:"map_name"`
	Ticks      []Tick  `json:"ticks"`
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
	SmokeEvents   []SmokeEvent   `json:"smoke_events"`
	InfernoEvents []InfernoEvent `json:"infer_events"`
	DecoyEvents   []DecoyEvent   `json:"decoy_events"`
}

//export ParseDemo
func ParseDemo(filename *C.char) C.bool {
	demodataFileName := C.GoString(filename)
	jsonFileName := demodataFileName[:len(demodataFileName)-len(".dem")] + ".json"

	f, err := os.Open(demodataFileName)
	if err != nil {
		log.Panic("failed to open demo file: ", err)
		return C.bool(false)
	}
	defer f.Close()

	p := demoinfocs.NewParser(f)
	defer p.Close()

	var demodata DemoData
	var ticks []Tick
	var kills []Kill
	var roundStarted bool
	var bombPlanted BombPlanted
	var bombDefused BombDefused
	var fireEvents []uint64
	var smokeEvents []SmokeEvent
	var inferEvents []InfernoEvent
	var decoyEvents []DecoyEvent
	bombExploded := false

	//Player weapon fire
	p.RegisterEventHandler(func(e events.WeaponFire) {
		if e.Shooter != nil {
			fireEvents = append(fireEvents, e.Shooter.SteamID64)
		}
	})

	// Smokes
	p.RegisterEventHandler(func(e events.SmokeStart) {
		smokeEvents = append(smokeEvents, SmokeEvent{
			X: e.Position.X,
			Y: e.Position.Y,
			Z: e.Position.Z,
		})
	})

	// Infernos
	p.RegisterEventHandler(func(e events.InfernoStart) {
		for _, inferno := range e.Inferno.Fires().Active().List() {
			inferEvents = append(inferEvents, InfernoEvent{
				X: inferno.X,
				Y: inferno.Y,
				Z: inferno.Z,
			})
		}
	})

	// Decoys
	p.RegisterEventHandler(func(e events.DecoyStart) {
		decoyEvents = append(decoyEvents, DecoyEvent{
			X: e.Position.X,
			Y: e.Position.Y,
			Z: e.Position.Z,
		})
	})

	// Kill events
	p.RegisterEventHandler(func(e events.Kill) {
		kills = append(kills, Kill{
			Killer:            checkPlayerName(e.Killer),
			Victim:            checkPlayerName(e.Victim),
			Weapon:            e.Weapon.String(),
			IsHeadshot:        e.IsHeadshot,
			PenetratedObjects: e.PenetratedObjects,
		})
	})

	// Bomb planted
	p.RegisterEventHandler(func(e events.BombPlanted) {
		isPlanted := false
		planterName := ""

		if len(e.Player.Name) > 0 {
			isPlanted = true
			planterName = e.Player.Name
		}

		bombPlanted = BombPlanted{
			Planted: isPlanted,
			Planter: planterName,
		}
	})

	// Bomb defused
	p.RegisterEventHandler(func(e events.BombDefused) {
		isDefused := false
		defuserName := ""

		if len(e.Player.Name) > 0 {
			isDefused = true
			defuserName = e.Player.Name
		}

		bombDefused = BombDefused{
			Defused: isDefused,
			Defuser: defuserName,
		}
	})

	// Bomb explodes
	p.RegisterEventHandler(func(e events.BombExplode) {
		bombExploded = true
	})

	// Start of a new round
	// True: indicates which tick is the exact round starting tick
	// False: otherwise
	p.RegisterEventHandler(func(e events.RoundStart) {
		roundStarted = true

		// Reset bomb status
		bombPlanted = BombPlanted{
			Planted: false,
			Planter: "",
		}

		bombDefused = BombDefused{
			Defused: false,
			Defuser: "",
		}
	})

	// Tick data
	// TODO: Needs heavy refactoring
	p.RegisterEventHandler(func(e events.FrameDone) {
		var players []Player
		var nades []Nade

		// Players
		for _, player := range p.GameState().Participants().Playing() {
			if player.IsAlive() {
				pos := player.Position()

				players = append(players, Player{
					SteamID:     player.SteamID64,
					Name:        player.Name,
					Clan:        player.TeamState.ClanName(),
					Team:        teamToString(player.Team),
					Health:      player.Health(),
					Money:       player.Money(),
					X:           pos.X,
					Y:           pos.Y,
					Z:           pos.Z,
					ViewX:       player.ViewDirectionX(),
					ViewY:       player.ViewDirectionY(),
					ActvItm:     player.ActiveWeapon().String(),
					Items:       itemsToStr(player.Weapons()),
					Helmet:      player.HasHelmet(),
					Armor:       player.Armor(),
					Kit:         player.HasDefuseKit(),
					IsDucking:   player.IsDucking(),
					IsWalking:   player.IsWalking(),
					IsReloading: player.IsReloading,
					IsAirborne:  player.IsAirborne(),
					Kills:       player.Kills(),
					Deaths:      player.Deaths(),
					Assists:     player.Assists(),
					DMG:         player.TotalDamage(),
					ADR:         calculateADR(player.TotalDamage(), p.GameState().TotalRoundsPlayed()), // avg damage / round
					IsPlanting:  player.IsPlanting,
					IsDefusing:  player.IsDefusing,
				})
			}
		}

		// Grenades
		for _, nade := range p.GameState().GrenadeProjectiles() {
			nades = append(nades, Nade{
				Type: nade.WeaponInstance.Type.String(),
				X:    nade.Position().X,
				Y:    nade.Position().Y,
				Z:    nade.Position().Z,
				Team: teamToString(nade.Owner.Team),
			})
		}

		// Bomb
		bomb := p.GameState().Bomb()

		bombStruct := Bomb{
			Carrier:     checkPlayerName(bomb.Carrier),
			X:           bomb.Position().X,
			Y:           bomb.Position().Y,
			Z:           bomb.Position().Z,
			BombPlanted: bombPlanted,
			BombDefused: bombDefused,
			Exploded:    bombExploded,
		}

		// Tick
		ticks = append(ticks, Tick{
			Tick:          p.CurrentFrame(),
			RoundStarted:  roundStarted,
			TeamT:         p.GameState().TeamTerrorists().ClanName(),
			TeamCT:        p.GameState().TeamCounterTerrorists().ClanName(),
			TWins:         p.GameState().TeamTerrorists().Score(),
			CTWins:        p.GameState().TeamCounterTerrorists().Score(),
			Players:       players,
			Bomb:          bombStruct,
			FireEvents:    fireEvents,
			Kills:         kills,
			Nades:         nades,
			SmokeEvents:   smokeEvents,
			InfernoEvents: inferEvents,
			DecoyEvents:   decoyEvents,
		})

		// These values need to be reset to false/nil before the next tick
		roundStarted = false
		kills = nil
		fireEvents = nil
		smokeEvents = nil
		inferEvents = nil
		decoyEvents = nil
		bombExploded = false
	})

	// Parse demo to end
	err = p.ParseToEnd()
	if err != nil {
		log.Panic("Error parsing demo: ", err)
		return C.bool(false)
	}

	demodata.TickRate = p.TickRate()
	demodata.TotalTicks = p.Header().PlaybackFrames
	demodata.MapName = p.Header().MapName
	demodata.Ticks = ticks

	file, _ := os.OpenFile(jsonFileName, os.O_CREATE, os.ModePerm)
	defer file.Close()

	// Write to JSON file
	encoder := json.NewEncoder(file)
	encoder.Encode(demodata)

	// if err != nil {
	// 	fmt.Println("Error encoding JSON:", err)
	// 	return C.bool(false)
	// }

	// err = os.WriteFile(jsonFileName, jsonData, 0644)
	// if err != nil {
	// 	fmt.Println("Error writing JSON file:", err)
	// 	return C.bool(false)
	// }

	return C.bool(true)
}

// Converts common.Equipment to string
func itemsToStr(items []*common.Equipment) []string {
	var items_str []string

	for _, item := range items {
		items_str = append(items_str, item.String())
	}

	return items_str
}

// Checks whether player is nil or not
// If player is nil, the name will be an emptry string
func checkPlayerName(player *common.Player) string {
	playerName := ""

	if player != nil {
		playerName = player.Name
	}

	return playerName
}

// Teams are represented by integers from 0-3, so this converts them to their
// corresponding names
func teamToString(team common.Team) string {
	var teamString string

	switch team {
	case 0:
		teamString = "UA" //TeamUnassigned
	case 1:
		teamString = "S" //TeamSpectators
	case 2:
		teamString = "T" //TeamTerrorists
	case 3:
		teamString = "CT" //TeamCounterTerrorists
	}

	return teamString
}

func calculateADR(damage int, roundsPlayed int) float64 {
	if roundsPlayed == 0 {
		return float64(damage)
	}

	return float64(damage) / float64(roundsPlayed)
}

func main() {
	// This is required to compile the shared library
}

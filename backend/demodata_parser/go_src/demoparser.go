package main

/*
#include <stdlib.h>
#include <stdbool.h>
*/
import "C"

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	demoinfocs "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs"
	common "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/common"
	events "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/events"
)

// TODO needs more fields
type Player struct {
	SteamID     uint64  `json:"sid"`
	Name        string  `json:"name"`
	Health      int     `json:"hp"`
	X           float64 `json:"x"`
	Y           float64 `json:"y"`
	Z           float64 `json:"z"`
	ViewX       float32 `json:"view_x"`
	ViewY       float32 `json:"view_y"`
	IsDucking   bool    `json:"is_ducking"`
	IsWalking   bool    `json:"is_walking"`
	IsAirborne  bool    `json:"is_air"`
	IsDefusing  bool    `json:"is_def"`
	IsReloading bool    `json:"is_rld"`
	Kills       int     `json:"kills"`
	Deaths      int     `json:"deaths"`
	Assists     int     `json:"assists"`
	DMG         int     `json:"dmg"`
}

type Kill struct {
	Killer            string `json:"killer"`
	Victim            string `json:"victim"`
	Weapon            string `json:"weapon"`
	IsHeadshot        bool   `json:"is_headshot"`
	PenetratedObjects int    `json:"penetrations"`
}

type Nade struct {
	Type string      `json:"type"`
	X    float64     `json:"x"`
	Y    float64     `json:"y"`
	Z    float64     `json:"z"`
	Team common.Team `json:"team"`
}

type DemoData struct {
	TickRate   float64 `json:"tick_rate"`
	TotalTicks int     `json:"total_ticks"`
	MapName    string  `json:"map_name"`
	Ticks      []Tick  `json:"ticks"`
}

// TODO needs more data, such as smokes, molotovs, bomb, match state etc.
type Tick struct {
	Tick    int      `json:"tick"`
	Players []Player `json:"players"`
	Kills   []Kill   `json:"kills"`
	Nades   []Nade   `json:"nades"`
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

	// Kill events
	p.RegisterEventHandler(func(e events.Kill) {
		killerName := "Unknown"
		victimName := "Unknown"

		if e.Killer != nil {
			killerName = e.Killer.Name
		}
		if e.Victim != nil {
			victimName = e.Victim.Name
		}

		kills = append(kills, Kill{
			Killer:            killerName,
			Victim:            victimName,
			Weapon:            e.Weapon.String(),
			IsHeadshot:        e.IsHeadshot,
			PenetratedObjects: e.PenetratedObjects,
		})
	})

	// Tick data
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
					Health:      player.Health(),
					X:           pos.X,
					Y:           pos.Y,
					Z:           pos.Z,
					ViewX:       player.ViewDirectionX(),
					ViewY:       player.ViewDirectionY(),
					IsDucking:   player.IsDucking(),
					IsWalking:   player.IsWalking(),
					IsReloading: player.IsReloading,
					IsAirborne:  player.IsAirborne(),
					Kills:       player.Kills(),
					Deaths:      player.Deaths(),
					Assists:     player.Assists(),
					DMG:         player.TotalDamage(),
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
				Team: nade.Owner.Team,
			})
		}

		ticks = append(ticks, Tick{
			Tick:    p.CurrentFrame(),
			Players: players,
			Kills:   kills,
			Nades:   nades,
		})

		kills = nil
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

	// Write to JSON file
	jsonData, err := json.MarshalIndent(demodata, "", " ")
	if err != nil {
		fmt.Println("Error encoding JSON:", err)
		return C.bool(false)
	}

	err = os.WriteFile(jsonFileName, jsonData, 0644)
	if err != nil {
		fmt.Println("Error writing JSON file:", err)
		return C.bool(false)
	}

	return C.bool(true)
}

func main() {
	// This is required to compile the shared library
}

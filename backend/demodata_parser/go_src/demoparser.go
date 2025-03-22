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

//export ParseDemo
func ParseDemo(filename *C.char) C.bool {
	// Open CS2 demodata-file
	demodataFileName := C.GoString(filename)
	demodataFile, err := os.Open(demodataFileName)
	if err != nil {
		log.Panic("failed to open demo file: ", err)
		return C.bool(false)
	}
	defer demodataFile.Close()

	// JSON: Create new files (tics & config)
	// Ticks
	jsonFileNameTicks := demodataFileName[:len(demodataFileName)-len(".dem")] + ".json"
	jsonFileTicks, err := os.OpenFile(jsonFileNameTicks, os.O_CREATE|os.O_WRONLY, os.ModePerm)
	if err != nil {
		log.Panic("failed to open/create JSON file: ", err)
		return C.bool(false)
	}
	defer jsonFileTicks.Close()

	// Config
	jsonFileNameConfig := demodataFileName[:len(demodataFileName)-len(".dem")] + "_config.json"
	jsonFileConfig, err := os.OpenFile(jsonFileNameConfig, os.O_CREATE|os.O_WRONLY, os.ModePerm)
	if err != nil {
		log.Panic("failed to open/create JSON file: ", err)
		return C.bool(false)
	}
	defer jsonFileConfig.Close()

	// Create new parser
	parser := demoinfocs.NewParser(demodataFile)
	defer parser.Close()

	//Player weapon fire
	var fireEvents []uint64
	parser.RegisterEventHandler(func(e events.WeaponFire) {
		if e.Shooter != nil {
			fireEvents = append(fireEvents, e.Shooter.SteamID64)
		}
	})

	// Smokes
	var smokeEvents []SmokeEvent
	parser.RegisterEventHandler(func(e events.SmokeStart) {
		smokeEvents = append(smokeEvents, SmokeEvent{
			X: e.Position.X,
			Y: e.Position.Y,
			Z: e.Position.Z,
		})
	})

	// Infernos
	var inferEvents []InfernoEvent
	parser.RegisterEventHandler(func(e events.InfernoStart) {
		for _, inferno := range e.Inferno.Fires().Active().List() {
			inferEvents = append(inferEvents, InfernoEvent{
				X: inferno.X,
				Y: inferno.Y,
				Z: inferno.Z,
			})
		}
	})

	// Decoys
	var decoyEvents []DecoyEvent
	parser.RegisterEventHandler(func(e events.DecoyStart) {
		decoyEvents = append(decoyEvents, DecoyEvent{
			X: e.Position.X,
			Y: e.Position.Y,
			Z: e.Position.Z,
		})
	})

	// Kill events
	var kills []Kill
	parser.RegisterEventHandler(func(e events.Kill) {
		kills = append(kills, Kill{
			Killer:            checkPlayerName(e.Killer),
			Victim:            checkPlayerName(e.Victim),
			Weapon:            e.Weapon.String(),
			IsHeadshot:        e.IsHeadshot,
			PenetratedObjects: e.PenetratedObjects,
		})
	})

	// Bomb planted
	var bombPlanted BombPlanted
	parser.RegisterEventHandler(func(e events.BombPlanted) {
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
	var bombDefused BombDefused
	parser.RegisterEventHandler(func(e events.BombDefused) {
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

	// Bomb exploded
	var bombExploded bool
	parser.RegisterEventHandler(func(e events.BombExplode) {
		bombExploded = true
	})

	// Start of a new round
	var roundStarted bool
	parser.RegisterEventHandler(func(e events.RoundStart) {
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

	// JSON: Write the opening bracket and "ticks" array
	jsonFileTicks.WriteString("{\"ticks\": [\n")
	firstTick := true

	// CREATE $_TICKS.JSON
	parser.RegisterEventHandler(func(e events.FrameDone) {
		// JSON: write comma after every object, except before the first and after the last one
		if !firstTick {
			jsonFileTicks.WriteString(",\n")
		}

		// Players
		var players []Player
		for _, player := range parser.GameState().Participants().Playing() {
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
					// avg damage / round
					ADR:        calculateADR(player.TotalDamage(), parser.GameState().TotalRoundsPlayed()),
					IsPlanting: player.IsPlanting,
					IsDefusing: player.IsDefusing,
				})
			}
		}

		// Grenades
		var nades []Nade
		for _, nade := range parser.GameState().GrenadeProjectiles() {
			nades = append(nades, Nade{
				Type: nade.WeaponInstance.Type.String(),
				X:    nade.Position().X,
				Y:    nade.Position().Y,
				Z:    nade.Position().Z,
				Team: teamToString(nade.Owner.Team),
			})
		}

		// Bomb
		bomb := parser.GameState().Bomb()
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
		tick := Tick{
			Tick:          parser.CurrentFrame(),
			RoundStarted:  roundStarted,
			TeamT:         parser.GameState().TeamTerrorists().ClanName(),
			TeamCT:        parser.GameState().TeamCounterTerrorists().ClanName(),
			TWins:         parser.GameState().TeamTerrorists().Score(),
			CTWins:        parser.GameState().TeamCounterTerrorists().Score(),
			Players:       players,
			Bomb:          bombStruct,
			FireEvents:    fireEvents,
			Kills:         kills,
			Nades:         nades,
			SmokeEvents:   smokeEvents,
			InfernoEvents: inferEvents,
			DecoyEvents:   decoyEvents,
		}

		// JSON: Write the tick
		tickJSON, err := json.Marshal(tick)
		if err != nil {
			log.Panic("Error encoding tick to JSON: ", err)
		}
		jsonFileTicks.WriteString(string(tickJSON))

		// Reset before the next tick
		roundStarted = false
		kills = nil
		fireEvents = nil
		smokeEvents = nil
		inferEvents = nil
		decoyEvents = nil
		bombExploded = false
		firstTick = false
	})

	// Parse demo to end
	err = parser.ParseToEnd()
	if err != nil {
		log.Panic("Error parsing demo: ", err)
		return C.bool(false)
	}

	// JSON: Write the closing brackets
	jsonFileTicks.WriteString("\n]}")

	// CREATE $_CONFIG.JSON
	var headerData HeaderData
	headerData.TickRate = parser.TickRate()
	headerData.TotalTicks = parser.Header().PlaybackFrames
	headerData.MapName = parser.Header().MapName
	headerDataJSON, err := json.Marshal(headerData)
	if err != nil {
		log.Panic("Error encoding tick to JSON: ", err)
	}
	jsonFileConfig.WriteString(string(headerDataJSON))

	// Return status to EEICT (Python)
	return C.bool(true)
}

// Converts a list of items to string
func itemsToStr(items []*common.Equipment) []string {
	var items_str []string

	for _, item := range items {
		items_str = append(items_str, item.String())
	}

	return items_str
}

// Checks whether player is nil or not
func checkPlayerName(player *common.Player) string {
	if player == nil {
		return ""
	}

	return player.Name
}

// Teams are represented by integers from 0-3, so this converts them to their
// corresponding names
func teamToString(team common.Team) string {
	var teamString string

	switch team {
	case 0:
		teamString = "UA" //Unassigned
	case 1:
		teamString = "S" //Spectators
	case 2:
		teamString = "T" //Terrorists
	case 3:
		teamString = "CT" //Counter Terrorists
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

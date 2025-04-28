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

type MatchState struct {
	RoundStarted   bool
	Tick           Tick
	Bomb           Bomb
	Players        []Player
	Nades          []Nade
	FireEvents     []uint64
	NadeEvent      NadeEvent
	Infernos       []Inferno
	Kills          []Kill
	TeamSideSwitch bool
	FirstTick      bool
	LastTick       int
}

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
	jsonFileTicks, err := os.OpenFile(jsonFileNameTicks, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, os.ModePerm)
	if err != nil {
		log.Panic("failed to open/create JSON file: ", err)
		return C.bool(false)
	}
	defer jsonFileTicks.Close()

	// Config
	jsonFileNameConfig := demodataFileName[:len(demodataFileName)-len(".dem")] + "_config.json"
	jsonFileConfig, err := os.OpenFile(jsonFileNameConfig, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, os.ModePerm)
	if err != nil {
		log.Panic("failed to open/create JSON file: ", err)
		return C.bool(false)
	}
	defer jsonFileConfig.Close()

	// Create new parser
	parser := demoinfocs.NewParser(demodataFile)
	defer parser.Close()

	matchState := MatchState{}
	matchState.FirstTick = true
	registerEventHandlers(parser, &matchState, jsonFileTicks)

	// JSON: Write the opening bracket and "ticks" array
	jsonFileTicks.WriteString("{\"ticks\": [\n")

	// CREATE $_TICKS.JSON
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

	rules := parser.GameState().Rules()
	roundTime, _ := rules.RoundTime()
	freezeTime, _ := rules.FreezeTime()
	bombTime, _ := rules.BombTime()

	headerData.TickRate = parser.TickRate()
	headerData.TotalTicks = parser.Header().PlaybackFrames
	headerData.MapName = parser.Header().MapName
	headerData.RoundTime = roundTime.Seconds()
	headerData.FreezeTime = freezeTime.Seconds()
	headerData.BombTime = bombTime.Seconds()

	headerDataJSON, err := json.Marshal(headerData)

	if err != nil {
		log.Panic("Error encoding tick to JSON: ", err)
	}

	jsonFileConfig.WriteString(string(headerDataJSON))

	// Return status to EEICT (Python)
	return C.bool(true)
}

func registerEventHandlers(parser demoinfocs.Parser, ms *MatchState, jsonTicks *os.File) {
	// Player weapon fire
	parser.RegisterEventHandler(func(e events.WeaponFire) {
		if e.Shooter != nil {
			ms.FireEvents = append(ms.FireEvents, e.Shooter.SteamID64)
		}
	})

	parser.RegisterEventHandler(func(e events.HeExplode) {
		ms.NadeEvent = nadeEventHandler(e.GrenadeEvent)
	})

	parser.RegisterEventHandler(func(e events.FlashExplode) {
		ms.NadeEvent = nadeEventHandler(e.GrenadeEvent)
	})

	parser.RegisterEventHandler(func(e events.SmokeStart) {
		ms.NadeEvent = nadeEventHandler(e.GrenadeEvent)
	})

	parser.RegisterEventHandler(func(e events.DecoyStart) {
		ms.NadeEvent = nadeEventHandler(e.GrenadeEvent)
	})

	parser.RegisterEventHandler(func(e events.Kill) {
		ms.Kills = killEventHandler(e)
	})

	parser.RegisterEventHandler(func(e events.RoundStart) {
		ms.RoundStarted = true

		// Reset bomb status
		ms.Bomb = Bomb{}
	})

	parser.RegisterEventHandler(func(e events.BombPlanted) {
		ms.Bomb.Planted = true
		ms.Bomb.PlantedBy = checkPlayerName(e.Player)
	})

	parser.RegisterEventHandler(func(e events.BombDefused) {
		ms.Bomb.Defused = true
		ms.Bomb.DefusedBy = checkPlayerName(e.Player)
	})

	parser.RegisterEventHandler(func(e events.BombExplode) {
		ms.Bomb.Exploded = true
	})

	parser.RegisterEventHandler(func(e events.TeamSideSwitch) {
		ms.TeamSideSwitch = true
	})

	// After a frame is done, this handler gets updated.
	// Frames are NOT stored in JSON, but server ticks are.
	parser.RegisterEventHandler(func(e events.FrameDone) {
		if updateTick(parser, ms) {
			if !ms.FirstTick {
				jsonTicks.WriteString(",\n")
			}

			tickJSON, err := json.Marshal(ms.Tick)
			if err != nil {
				log.Panic("Error encoding tick to JSON: ", err)
			}
			jsonTicks.WriteString(string(tickJSON))

			ms.FirstTick = false
		}

		// Reset tick data before the next frame
		ms.RoundStarted = false
		ms.Players = nil
		ms.Nades = nil
		ms.Infernos = nil
		ms.Kills = nil
		ms.FireEvents = nil
		ms.NadeEvent = NadeEvent{}
	})
}

func getPlayersInCurrentFrame(parser demoinfocs.Parser) []Player {
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
				IsStanding:  player.IsStanding(),
				IsReloading: player.IsReloading,
				IsAirborne:  player.IsAirborne(),
				Kills:       player.Kills(),
				Deaths:      player.Deaths(),
				Assists:     player.Assists(),
				DMG:         player.TotalDamage(),
				ADR:         calculateADR(player.TotalDamage(), parser.GameState().TotalRoundsPlayed()),
				IsPlanting:  player.IsPlanting,
				IsDefusing:  player.IsDefusing,
			})
		}
	}

	return players
}

func getNadesInCurrentFrame(parser demoinfocs.Parser) []Nade {
	var nades []Nade
	for _, nade := range parser.GameState().GrenadeProjectiles() {
		nades = append(nades, Nade{
			ID:   nade.UniqueID(),
			Type: nade.WeaponInstance.Type.String(),
			X:    nade.Position().X,
			Y:    nade.Position().Y,
			Z:    nade.Position().Z,
			Team: teamToString(nade.Owner.Team),
		})
	}

	return nades
}

func getInfernosInCurrentFrame(parser demoinfocs.Parser) []Inferno {
	var infernos []Inferno

	for _, inferno := range parser.GameState().Infernos() {
		var fires []Fire
		id := 0

		for _, fire := range inferno.Fires().Active().List() {
			fires = append(fires, Fire{
				X: fire.X,
				Y: fire.Y,
				Z: fire.Z,
			})

			id++
		}

		infernos = append(infernos, Inferno{
			ID:    inferno.UniqueID(),
			Fires: fires,
		})
	}

	return infernos
}

// Updates matchState Tick if the next frame is a new server tick or contains an update.
func updateTick(parser demoinfocs.Parser, ms *MatchState) bool {
	currentTick := parser.GameState().IngameTick()
	matchStarted := parser.GameState().IsMatchStarted()

	// Check if the game tick has updated
	tickChanged := matchStarted && (currentTick != ms.LastTick ||
		ms.NadeEvent.Type != "" ||
		ms.FireEvents != nil ||
		ms.Kills != nil ||
		ms.RoundStarted)

	if tickChanged {
		// Players
		ms.Players = getPlayersInCurrentFrame(parser)

		// Nades
		ms.Nades = getNadesInCurrentFrame(parser)

		// Incendiaries/molotovs
		ms.Infernos = getInfernosInCurrentFrame(parser)

		// Bomb
		updateBomb(parser, ms)

		ms.Tick = Tick{
			Tick:           currentTick,
			RoundTime:      parser.CurrentTime().Seconds(),
			RoundStarted:   ms.RoundStarted,
			TeamSideSwitch: ms.TeamSideSwitch,
			IsFreezeTime:   parser.GameState().IsFreezetimePeriod(),
			TeamT:          parser.GameState().TeamTerrorists().ClanName(),
			TeamCT:         parser.GameState().TeamCounterTerrorists().ClanName(),
			TWins:          parser.GameState().TeamTerrorists().Score(),
			CTWins:         parser.GameState().TeamCounterTerrorists().Score(),
			Players:        ms.Players,
			ShootingEvents: ms.FireEvents,
			Kills:          ms.Kills,
			Nades:          ms.Nades,
			Infernos:       ms.Infernos,
			Bomb:           ms.Bomb,
		}

		if ms.NadeEvent.Type != "" {
			ms.Tick.NadeEvent = &ms.NadeEvent
		} else {
			ms.Tick.NadeEvent = nil
		}

		ms.LastTick = currentTick

		return true
	}

	return false
}

func updateBomb(parser demoinfocs.Parser, ms *MatchState) {
	bombData := parser.GameState().Bomb()

	ms.Bomb.Carrier = checkPlayerName(bombData.Carrier)
	ms.Bomb.X = bombData.Position().X
	ms.Bomb.Y = bombData.Position().Y
	ms.Bomb.Z = bombData.Position().Z
}

func nadeEventHandler(e events.GrenadeEvent) NadeEvent {
	return NadeEvent{
		Type: e.Base().GrenadeType.String(),
		X:    e.Base().Position.X,
		Y:    e.Base().Position.Y,
		Z:    e.Base().Position.Z,
	}
}

func killEventHandler(e events.Kill) []Kill {
	var kills []Kill
	kills = append(kills, Kill{
		Killer:            checkPlayerName(e.Killer),
		Victim:            checkPlayerName(e.Victim),
		Weapon:            e.Weapon.String(),
		IsHeadshot:        e.IsHeadshot,
		PenetratedObjects: e.PenetratedObjects,
	})

	return kills
}

// Converts a list of items to string
func itemsToStr(items []*common.Equipment) []string {
	var itemsStr []string

	for _, item := range items {
		itemsStr = append(itemsStr, item.String())
	}

	return itemsStr
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

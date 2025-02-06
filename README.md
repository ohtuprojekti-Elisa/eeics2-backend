# Elisa Esports - Immersive Coaching Tool

A prototype AR tool for Counter-Strike 2 coaching and refereeing, developed for Elisa Esports. This tool enables users to watch game broadcasts while accessing real-time game statistics, interacting with a 3D bird's-eye-view map, and utilizing various advanced features. This tool was developed as part of a Software Engineering Lab project for the Department of Computer Science at the University of Helsinki.

## Status
[![Push backend image to Quay.io](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-quay.yaml/badge.svg?branch=main)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-quay.yaml)

[![Sync and push backend to version.helsinki.fi](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml/badge.svg?branch=main)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml)

## Implementation
- Implemented for Meta Quest VR headsets (Android-based)
- Developed in Unity environment
- Deployed on OpenShift
- Backend code in Python, frontend code in C#
- PostgreSQL database

## Instructions
### Requirements
In order to use this app, you need to fullfill the following requirements:
* You have to have Unity installed. You can download Unity [here](https://unity.com/download).
* You have to have Counter-Strike 2 installed.
* You need to have access to the University of Helsinki's network. Find information on connecting using VPN [here](https://helpdesk.it.helsinki.fi/en/logging-and-connections/networks/connections-outside-university).

### Configuration for Counter-Strike 2
1. Navigate to your game's configuration (cfg) folder. Example - C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg
2. Add [this](counter_strike_2/gsi/gamestate_integration_example.cfg) configuration file to the cfg folder.

### Launching the app in Unity
1. Clone this repository to your local device.
2. Locate project in unityhub and download the correct unity editor build by clicking the project.
3. Open the cloned project in Unity.
4. (Optional) Make sure you are connected to the University of Helsinki's network. [Steps to Connect to OpenVPN](https://helpdesk.it.helsinki.fi/kirjautuminen-ja-yhteydet/verkkoyhteydet/yhteydet-yliopiston-ulkopuolelta)
5. (Optional) Join a game in CS2 as a **spectator** OR play a demo by using playdemo command in CS2 console and downloading the demo and putting it to Counter-Strike Global Offensive/game/csgo
6. Make sure the correct scene is selected. Go to File -> Open scene -> Scenes folder -> open Main Vr Scene.unity
7. Enter the play-mode in unity (optional: Activate the simulator to use vr controllers when testing with pc)
Note: Unity can be slow. Be patient and give it time.

## Documentation

### Architecture
- [Class diagram](https://github.com/NikiPOU/elisaohtuprojekti/blob/main/docs/class_diagram.md)
- [Architecture diagram and documentation](https://github.com/NikiPOU/elisaohtuprojekti/blob/main/docs/architecture.md)

### Practices
- [Definition of Done](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/blob/main/docs/definition%20of%20done.md)

### For those wanting to continue this project
- [Handover](https://github.com/NikiPOU/elisaohtuprojekti/blob/main/docs/handover.md)

## Backlog
- [Product backlog](https://github.com/orgs/ohtuprojekti-Elisa/projects/1)

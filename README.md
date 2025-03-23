# Elisa Esports - Immersive Coaching Tool

A prototype mixed reality (AR/VR) tool for Counter-Strike 2 coaching, developed for Elisa Esports. This tool enables users to watch playback of recorded demo while accessing its statistics, interacting with a 3D bird's-eye-view map and utilizing various advanced features. This tool was developed as part of a Software Engineering Lab project for the Department of Computer Science at the University of Helsinki.

## Status
[![Sync backend to version.helsinki.fi](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml/badge.svg?branch=main)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml)

[![Backend unit tests](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/test_backend.yml/badge.svg)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/test_backend.yml)

## Implementation
- Implemented for Meta Quest VR headsets (Android-based)
- Developed in Unity environment (C#)
- Backend code in Python and Go
- Deployed on OpenShift
- PostgreSQL database

## Instructions
### Requirements
In order to use this app, you need to fullfill the following requirements:
* You have to have Unity installed. You can download Unity [here](https://unity.com/download).
* You have to have Counter-Strike 2 installed.
* You need to have access to the University of Helsinki's network. Find information on connecting using VPN [here](https://helpdesk.it.helsinki.fi/en/logging-and-connections/networks/connections-outside-university).

### Launching the app in Unity
1. Clone this repository to your local device.
2. Locate project in unityhub and download the correct unity editor build by clicking the project.
3. Open the cloned project in Unity.
4. (Optional) Make sure you are connected to the University of Helsinki's network. [Steps to Connect to OpenVPN](https://helpdesk.it.helsinki.fi/kirjautuminen-ja-yhteydet/verkkoyhteydet/yhteydet-yliopiston-ulkopuolelta)
6. Make sure the correct scene is selected. Go to File -> Open scene -> Scenes folder -> open Main Vr Scene.unity
7. Enter the play-mode in unity (optional: Activate the simulator to use vr controllers when testing with pc)
Note: Unity can be slow. Be patient and give it time.

## Project documentation

### Process
- [Documentation repository (fi)](https://github.com/ohtuprojekti-Elisa/suunnitteludokumentaatio)

### Practices
- [Definition of Done](docs/definition%20of%20done.md)

### Backlog
- [Product backlog](https://github.com/orgs/ohtuprojekti-Elisa/projects/1)

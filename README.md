# Elisa Esports Immersive CS2

Prototype of a mixed reality (XR) application for innovatively reviewing Counter-Strike 2 (CS2) matches, developed for Elisa Esports. The Elisa Esports Immersive CS2 enables a new way to review game events in an immersive VR-environment, allowing for more detailed analyses of both team and individual player performances. This tool was developed as part of a Software Engineering Lab project for the Department of Computer Science at the University of Helsinki.
## Video demo

[![EEICS2 Demo](/docs/images/video_thumb.jpg)](https://www.youtube.com/watch?v=AEIXmy_g22s "Elisa Esports Immersive CS2")
## Status
[![Sync backend to version.helsinki.fi](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml/badge.svg?branch=main)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/push-to-version.helsinki.fi.yaml)

[![Backend unit tests](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/test_backend.yml/badge.svg)](https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/actions/workflows/test_backend.yml)

## Implementation

- Implemented for Meta Quest VR headsets
- Developed in Unity environment (C#)
- Backend code in Python and Go
- Deployed on OpenShift
## Instructions
### Prerequisites

In order to use this app, you need to fulfill the following requirements:
* At least have Python installed. Download Python [here](https://www.python.org/downloads/).
* You need demo files recorded in Counter-Strike 2 and from a Mirage map. Put those files in directory: `elisaohtuprojekti/backend/demofiles/`. If you don't have any, you can use the ones in `elisaohtuprojekti/backend/demofiles/test_demos/`.
* Select from 'easy' or 'hard' paths below.
### Easy: Launching the downloaded app (release)

1. Read [this document](docs/release_readme.md).
### Hard: Launching the cloned project in Unity

You can download Unity [here](https://unity.com/download).
1. Clone this repository to your local device.
2. Locate project in Unity Hub and download the correct Unity version (2022.3.45f1) by clicking the project.
3. Open the cloned project in Unity.
4. Start the backend process using [this guide](docs/backend/backend_user_guide.md#starting-the-backend-process)
5. Make sure the correct scene is selected by going to `File -> Open scene -> Scenes folder` and opening: `Main Vr Scene.unity`.
6. Enter the play-mode in Unity

Note: Especially the first start takes a while (25-25 minutes), because Unity creates the lightmap UV:s for map model. So be patient and give it time.
## Documentation

- Backend, Frontend and various docs
	- /[Docs](docs/)
- Handover
	- [Project handover](docs/project%20handover.md)
-  Practices
	- [Definition of Done](docs/definition%20of%20done.md)
-  Backlog
	- [Product backlog](https://github.com/orgs/ohtuprojekti-Elisa/projects/1)

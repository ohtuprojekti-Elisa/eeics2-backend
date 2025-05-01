# EEICS2 - Project handover

This document conducts a quick walkthrough of the Elisa Esports Immersive CS2 project.
## Backend

Backend consists of CS2 demo data parser and WebSocket server.
#### Technology stack

- Python
- Go
- C#
- Docker
#### Deployment guide

- [backend_user_guide](backend/backend_user_guide.md)
- [cs2-demodata_to_eeict](backend/cs2-demodata_to_eeict.md)
- [eeict-backend](backend/eeict-backend.md)
#### Other related documents / files

- [OpenShift configs](backend/openshift_configs/openshift_configs.md)
#### Researched and resolved problems

- [Unity Version Control](Unity%20Version%20Control.md)
- [json_vs_ijson](backend/json_vs_ijson.md)
#### Development ideas for backend
- Refactor code and write more in depth tests.
- Ablity to work in a live broadcast environment.
- New modes and ability to change between them: coaching and forensics.
- A web front to upload demo files for streaming (Tornado can create REST API).
- Containerize in Docker or Podman (Image with Python and Go required)
- Add a posibility to pause and resume the streaming from client. Usable with coaching or forensics mode.
- Optimize data transfer by using losless compression methods.
- Add new data points to parser side and find usage for them on client side.
- Mode to scheduling a stream start time by realtime clock or by delaying it n+1 minutes.

## Frontend

Frontend consists of virtual reality project.
#### Technology stack

- C#
- Unity
- SteamVR
#### Deployment guide

- [weapons](weapons.md)
- [models_animations](models_anim.md)
#### Other related documents / files
#### Researched and resolved problems
#### Development ideas for frontend

# Elisa Esports Immersive CS2

Instructions on how to install and use this release.

### Requirements

This is what you need for get things rolling.

 - A fairly modern computer with Windows 10 or 11.
 - Meta Quest 3 (other models might work too).
 - Meta Quest Link App.
   - https://www.meta.com/en-gb/help/quest/1517439565442928/

 - Contents of this downloaded release.
   - https://github.com/ohtuprojekti-Elisa/elisaohtuprojekti/releases

 - Python (version 3.12).
   - https://www.python.org/downloads/


### Setting up

Just with a few steps and you can start viewing CS2 demos!

 - Install and setup Meta Quest Link App.
 - Install Python 3.12.
 - In release folder, with PowerShell , navigate to `backend` folder.
 - Install Python virtual environment (venv) with command `python -m venv .venv`.
 - Activate the venv with `.venv\Scripts\activate.ps1`.
 - Install backends dependencies with the command:  `pip install -r requirements.txt`.
 - If everything goes without errors, setup is done!

### Starting server and client

- Place your CS2 demo file inside `./backend/demofiles/` folder.
- In release folder, with PowerShell , navigate to `backend` folder.
- Activate the venv with `.venv\Scripts\activate.ps1`
- Start the backend (venv activated) with  a command `python eeict.py -f yourdemofile.dem`
  - You can also view other options with `python eeict.py -h`.
- In `./ElisaSportsImmersive/` folder, start the client by double clicking 'Elisa Esports Immersive.exe'.
- Now you should see your demo file playing in the client!
- ...
- Enjoy!
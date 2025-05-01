# Creating a Demo in CS2

1. Launch CS2 and open the developer console by pressing the "§" key (in the main lobby).
   * If the console doesn't open -> Settings -> Game -> Enable Developer Console: "Yes"

2. In the CS2 console, type `tv_enable true` (do this in the lobby before joining a server).

3. Select for example: Play -> Practice -> Mirage -> Start

4. When the game starts, open the CS2 console and type `tv_record filename`.

5. To stop recording, type `tv_stoprecord` in the CS2 console.

6. The demo file can be found at: `./Steam/steamapps/common/Counter-Strike Global Offensive/game/csgo`

**NOTE:** You might need to re-enable `tv_enable true` every time you restart CS2.  
Automatic recording at game launch can sometimes cause issues, so it's better to avoid using it.

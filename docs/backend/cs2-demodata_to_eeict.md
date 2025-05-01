# CS2 demodatan siirto EEICT-sovellukseen (WIP)

Backendin sovellusarkkitehtuuri kuvattuna kehittäjän näkökulmasta.
## Arkkitehtuurikuvaus

```mermaid

%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%

flowchart TB

    dem@{ shape: doc, label: "$demodata.DEM"}
    dem --> parser

    direction TB
    orch("Orchestrator")
    orch -.-> parser
    orch -.-> server
    
    subgraph parser ["**Demodata parser**"]
        worker("Worker")
        worker <--"subprocess.run"--> B
        B("DemodataToJSON-parser (Demoinfocs-golang)")
    end

    parser --- json
    json@{ shape: doc, label: "$demodata.JSON"}
    json --> server

    subgraph server ["**Demodata Server**"]
        direction LR
        D("JSONchopper (ijson)") 
        D --> E
        E("Websocket-server (Tornado)")
    end
    
    server <--"Websocket"--> eeict
    eeict{{"EEICT (Unity/C#)"}}
    
```

## Komponenttien vastuut

#### Orchestrator
- Vastuu: demodatan siirtymisestä eri komponenttien välillä.
- Ohjelmointikieli: Python

### Demodata parser

Ottaa syötteenä Counter Strike 2:n tuottaman demodata tiedoston (\*.dem) ja tuottaa siitä EEICT-sovelluksen käyttöön soveltuvan JSON-tiedoston.
#### Worker
- Vastuu: demodatan siirtymisestä parserin läpi.
- Ohjelmointikieli: Python
#### DemodataToJSON-parser
- Vastuu: parsii CS2:n tuottaman demodatan JSON muotoon.
- Ohjelmointikieli: Go
- Hyödyntää kirjastoa: Demoinfocs-golang (https://github.com/markus-wa/demoinfocs-golang)
- Tallentaa parsitun JSON-datan saman nimiseen tiedostoon kuin lähdetiedosto.
- Mahdollisuus määrittää JSON-tiedostoon tulevien tapahtumien määrä/sekunti.
    - CS2 tukee enimmillään 64/128 tapahtumaa/sekunti, riippuen CS2-palvelimen asetuksista.
    - Kirjoittaa asetetun intervallin JSON-tiedostoon.

### Demodata Server

Ottaa syötteenä parserin tuottaman JSON-tiedoston ja lähettää sitä objekti kerrallaan websocket protokollaa hyödyntäen. Toimii myös itsenäisenä, kehittäjän koneella suoritettavana sovelluksena.
#### JSONchopper
- Vastuu: pilkkoo JSON-tiedoston yksittäisiksi objekteiksi EEICT-sovellukselle siirtoa varten.
- Ohjelmointikieli: Python
- Lukee parserilta saadun JSON-tiedoston muistiin.
- Siirtää JSON-tiedoston datan objekti kerrallaan, aiemmin määritetyllä tapahtumaa/sekunti intervallilla, eteenpäin seuraavalle komponentille.
- Hyödyntää kirjastoa: Ijson (https://pypi.org/project/ijson/)
#### Websocket-server
- Vastuu: muodostaa websocket protokollaa hyödyntäen yhteyden backendin ja EEICT-sovelluksen välille.
- Siirtää JSONchopperilta saatua dataa aiemmin määritetyllä tapahtumaa/sekunti intervallilla (esimerkiksi: 64 t/s = 15.625ms)
- Ohjelmointikieli: Python
- Hyödyntää kirjastoa: Tornado (https://www.tornadoweb.org/en/stable/)
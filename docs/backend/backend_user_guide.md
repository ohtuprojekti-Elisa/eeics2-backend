# EEICT - Backend User Guide

Instructions for settings up virtual environment, compiling binaries, starting up and using the backend for Elisa Esports Immersive Coaching Tool (EEICT).

## Compiling the demo data parser

The demo data parser, written in Go, must be compiled before use. Here are the instructions for Windows.

#### Windows

1. Download and install the latest version of Go (64-bit): [https://go.dev/doc/install](https://go.dev/doc/install)
    - *A restart or re-login might be needed to complete the setup.*
2. Download the latest version of the `mingw-w64` compiler: [https://github.com/niXman/mingw-builds-binaries/releases](https://github.com/niXman/mingw-builds-binaries/releases)
    1. Recommended: `x86_64-$SOMERELEASE-win32-seh-ucrt-rt_$SOMEVERSION.7z`
    2. Extract the downloaded archive and move the `mingw64` folder inside it, to a location of your choice.
    3. Add the newly created `mingw64/bin` folder path to your system's environment `PATH` variable.
        - Guide: [https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho)
        - *You might need to restart or re-login for the environment variable to take effect.*
    4. Test if GCC is working by running `gcc --version` in your terminal.
3. In your console, navigate to the parser folder `./backend/demodata_parser/`.
4. Compile the parser using the command `python build.py`.
5. Fingers crossed.
6. If the parser compiled successfully, you’ll find the `demoparser.so` file in the `./backend/demodata_parser/` directory.
#### Linux

1. TBA

2. source .venv/bin/activate


## Starting the backend process

How to "get the pipeline running."

#### Windows

1. Place your chosen demo file into the `./backend/demofiles/` folder.
2. Open Powershell or CMD.
3. Navigate to the `./backend/` directory.
4. Create a new Python Virtual Environment (venv) with the command:  `python -m venv .venv`
5. Activate the venv:
    - CMD: `.venv\Scripts\activate`
    - Powershell: `.venv\Scripts\activate.ps1`
        - *If successful, your prompt should show something like `(.venv) PS {directory}`*
6. Install backends dependencies with the command:  `pip install -r requirements.txt`
7. Finally, you can start the EEICT backend from the `./backend/` folder with:  
    `python eeict.py -f your_demo_file.dem`
8. Once the parse process is done and  the server is running and waiting for a new connection, you can connect using the EEICT application.

#### Linux

1. TBA

## Backend commands and examples

The backend takes any `.dem` file produced by CS2 as input (`$` = your file).

#### Help

Shows the most up-to-date list of available features:

```sh
python eeict.py -h
```

#### File

Feeds the specified CS2 demo file to the backend:

```sh
python eeict.py -f $
```

#### Loop

Loops the demo file continuously until the backend process is stopped:

```sh
python eeict.py -l -f $
```

#### Overwrite

Overwrites previously parsed `.json` files tied to the CS2 demo file name. This is necessary after compiling a new version of the parser. Using this option may also help fix backend issues during development.

```sh
python eeict.py -o -f $
```

## Nota bene!

To ensure everything runs smoothly on the backend, keep in mind that the demo data parser must be recompiled after every change made to it. There’s no need to delete the old `demoparser.so` file — the compiler will overwrite it. However, any `$.json` or `$_config.json` files generated using the old version of the parser, must be reparsed using the `-o` argument at starup. This is to ensure, that any changes made to the JSON output logic of the parser are reflected in them.

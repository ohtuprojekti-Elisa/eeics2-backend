import os
from dotenv import load_dotenv
import subprocess

# Load and set .env_build
load_dotenv(".env_build")

# Build demoparser
os.chdir("go_src")
subprocess.run(
    [
        "go",
        "build",
        "-o",
        "../demoparser.so",
        "-buildmode=c-shared",
        "demoparser.go",
    ],
    check=True,
)

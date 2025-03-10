import os
import subprocess

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
    env={**os.environ, "CGO_ENABLED": "1"},
)

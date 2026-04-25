#!/usr/bin/env python3
"""
components/polybar/shared/launch.py
Reinicia polybar en cada monitor conectado.
"""

import subprocess
import os
import time
from pathlib import Path


def _connected_monitors() -> list[str]:
    """Devuelve la lista de monitores activos según xrandr."""
    try:
        out = subprocess.check_output(["xrandr", "--query"], text=True)
        return [
            line.split()[0]
            for line in out.splitlines()
            if " connected" in line
        ]
    except FileNotFoundError:
        return []


def main():
    # Matar instancias previas
    subprocess.run(["killall", "-q", "polybar"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Esperar a que terminen
    while True:
        result = subprocess.run(
            ["pgrep", "-x", "polybar"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            break
        time.sleep(0.5)

    # Lanzar una instancia por monitor
    monitors = _connected_monitors()
    if not monitors:
        monitors = [""]   # sin xrandr: lanzar una instancia genérica

    env = os.environ.copy()
    for monitor in monitors:
        if monitor:
            env["MONITOR"] = monitor
        subprocess.Popen(
            ["polybar", "--reload", "main"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    main()

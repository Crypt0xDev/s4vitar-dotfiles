#!/usr/bin/env python3
"""
core/bspwm/scripts/autostart.py
Lanzado por bspwmrc al iniciar sesión. Arranca los daemons del entorno.
"""

import subprocess
import os
from pathlib import Path

HOME = Path.home()


def spawn(*cmd: str) -> None:
    """Lanza un proceso en segundo plano, sin bloquear."""
    subprocess.Popen(list(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    # Fondo de pantalla
    wallpaper = HOME / "Pictures" / "wallpapers" / "main.jpg"
    if wallpaper.exists():
        spawn("feh", "--bg-fill", str(wallpaper))

    # Compositor
    spawn("picom", "--experimental-backends")

    # Barra
    launch = HOME / ".config" / "polybar" / "launch.py"
    if launch.exists():
        spawn("python3", str(launch))

    # Notificaciones
    spawn("dunst")

    # Cursor
    spawn("xsetroot", "-cursor_name", "left_ptr")

    # Numlock
    spawn("numlockx", "on")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║       bspwm-dotfiles — Instalador principal          ║
║       Kali · Parrot · Arch  |  s4vitar style         ║
╚══════════════════════════════════════════════════════╝
Uso: sudo python3 install.py
"""

import os
import sys
import shutil
import importlib.util
from pathlib import Path

# ── Rutas base ───────────────────────────────────────────────
REPO_DIR     = Path(__file__).parent.resolve()
HOME         = Path.home()
CONFIG_DIR   = HOME / ".config"
FONTS_DIR    = HOME / ".local" / "share" / "fonts"
PICTURES_DIR = HOME / "Pictures" / "wallpapers"

sys.path.insert(0, str(REPO_DIR / "scripts"))
from utils import (
    info, ok, warn, die, header,
    print_banner, detect_distro, deploy_dir, run,
)

# ── Mapa distro → handler ────────────────────────────────────
DISTRO_MAP = {
    "arch":     REPO_DIR / "distros" / "arch"   / "handler.py",
    "manjaro":  REPO_DIR / "distros" / "arch"   / "handler.py",
    "kali":     REPO_DIR / "distros" / "debian" / "handler.py",
    "parrot":   REPO_DIR / "distros" / "debian" / "handler.py",
    "debian":   REPO_DIR / "distros" / "debian" / "handler.py",
    "ubuntu":   REPO_DIR / "distros" / "debian" / "handler.py",
}


def load_handler(distro: str):
    """Carga dinámicamente el módulo handler de la distro."""
    handler_path = DISTRO_MAP.get(distro)
    if not handler_path or not handler_path.exists():
        die(f"Distro '{distro}' no soportada o handler no encontrado.")
    spec = importlib.util.spec_from_file_location("handler", handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def step_core():
    """Despliega core/ → ~/.config/bspwm + ~/.config/sxhkd."""
    header("Aplicando configuración core")

    for app in ("bspwm", "sxhkd"):
        src = REPO_DIR / "core" / app
        dest = CONFIG_DIR / app
        deploy_dir(src, dest)
        ok(f"core/{app} → {dest}")

    # Permisos de ejecución
    bspwmrc = CONFIG_DIR / "bspwm" / "bspwmrc"
    if bspwmrc.exists():
        bspwmrc.chmod(0o755)
    for f in (CONFIG_DIR / "bspwm").rglob("*.sh"):
        f.chmod(0o755)


def step_components(distro: str):
    """Despliega components/: shared + override por distro."""
    header("Aplicando componentes")

    for component in ("polybar", "rofi"):
        shared   = REPO_DIR / "components" / component / "shared"
        override = REPO_DIR / "components" / component / distro
        dest     = CONFIG_DIR / component
        if shared.exists():
            deploy_dir(shared, dest)
        if override.exists():
            deploy_dir(override, dest)
        for f in dest.rglob("*.sh"):
            f.chmod(0o755)
        ok(f"{component} aplicado.")

    # Zsh va al HOME
    for subdir in ("shared", distro):
        zshrc = REPO_DIR / "components" / "zsh" / subdir / ".zshrc"
        if zshrc.exists():
            shutil.copy2(zshrc, HOME / ".zshrc")
    ok("zsh aplicado.")


def step_fonts():
    """Instala fuentes desde fonts/."""
    header("Instalando fuentes")
    src = REPO_DIR / "fonts"
    if not src.exists():
        warn("Carpeta fonts/ no encontrada, omitiendo.")
        return
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for f in src.rglob("*"):
        if f.is_file() and f.suffix in (".ttf", ".otf", ".woff", ".woff2"):
            shutil.copy2(f, FONTS_DIR / f.name)
    run(["fc-cache", "-fv"])
    ok("Fuentes instaladas.")


def step_wallpapers():
    """Copia wallpapers a ~/Pictures/wallpapers/."""
    header("Instalando wallpapers")
    src = REPO_DIR / "wallpapers"
    if not src.exists():
        warn("Carpeta wallpapers/ no encontrada, omitiendo.")
        return
    PICTURES_DIR.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, PICTURES_DIR / f.name)
    ok(f"Wallpapers → {PICTURES_DIR}")


def step_reload():
    """Recarga bspwm si está corriendo."""
    header("Recargando entorno")
    if run(["pgrep", "-x", "bspwm"], check=False):
        run(["bspc", "wm", "-r"])
        ok("bspwm recargado.")
    else:
        warn("bspwm no está corriendo. Inicia sesión para aplicar el entorno.")


# ── Punto de entrada ─────────────────────────────────────────
def main():
    print_banner()

    if os.geteuid() != 0:
        die("Ejecuta como root: sudo python3 install.py")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    distro = detect_distro()
    info(f"Distro detectada: {distro}")

    handler = load_handler(distro)

    # 1. Dependencias
    header("Instalando dependencias")
    handler.deps(REPO_DIR)

    # 2. Core
    step_core()

    # 3. Componentes
    step_components(distro)

    # 4. Post-instalación por distro
    header(f"Post-instalación ({distro})")
    handler.post(HOME)

    # 5. Fuentes
    step_fonts()

    # 6. Wallpapers
    step_wallpapers()

    # 7. Recargar
    step_reload()

    print(f"\n\033[1;32m╔════════════════════════════════════╗")
    print(f"║  Instalación completada con éxito  ║")
    print(f"╚════════════════════════════════════╝\033[0m")
    print(f"\n\033[0;33m➜  Cierra sesión y vuelve a entrar, o ejecuta: startx\033[0m\n")


if __name__ == "__main__":
    main()

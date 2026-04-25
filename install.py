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
    print_banner, deploy_dir, run,
)

# ── Mapa distro → handler ────────────────────────────────────
DISTRO_MAP = {
    "kali":   REPO_DIR / "distros" / "debian" / "handler.py",
    "parrot": REPO_DIR / "distros" / "debian" / "handler.py",
    "arch":   REPO_DIR / "distros" / "arch"   / "handler.py",
}

# Opciones que aparecen en el menú (las 3 soportadas)
MENU_OPTIONS = [
    ("kali",   "Kali Linux"),
    ("parrot", "Parrot OS"),
    ("arch",   "Arch Linux"),
]

# Distros actualmente disponibles
AVAILABLE = {"kali"}


def choose_distro() -> str:
    """Menú manual de selección de distro. Devuelve el identificador elegido."""
    CYAN   = "\033[0;36m"
    BOLD   = "\033[1m"
    YELLOW = "\033[0;33m"
    GRAY   = "\033[0;90m"
    RESET  = "\033[0m"

    print(f"\n{CYAN}{BOLD}══ Selección de sistema operativo ══{RESET}\n")

    for i, (key, label) in enumerate(MENU_OPTIONS, 1):
        if key in AVAILABLE:
            print(f"  {BOLD}{i}{RESET}) {label}")
        else:
            print(f"  {GRAY}{i}) {label}  [próximamente]{RESET}")

    print()
    while True:
        try:
            raw = input(f"{YELLOW}Elige una opción: {RESET}").strip()
            choice = int(raw)
            if 1 <= choice <= len(MENU_OPTIONS):
                key = MENU_OPTIONS[choice - 1][0]
                if key not in AVAILABLE:
                    print(f"  {YELLOW}Esa opción aún no está disponible.{RESET}")
                    continue
                return key
            print(f"  Opción inválida. Introduce un número entre 1 y {len(MENU_OPTIONS)}.")
        except ValueError:
            print(f"  Opción inválida. Introduce un número entre 1 y {len(MENU_OPTIONS)}.")
        except KeyboardInterrupt:
            print("\nInstalación cancelada.")
            raise SystemExit(0)


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
    """Despliega core/ → ~/.config/{bspwm,sxhkd,kitty,picom,rofi}."""
    header("Aplicando configuración core")

    for app in ("bspwm", "sxhkd", "kitty", "picom", "rofi"):
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
    for f in (CONFIG_DIR / "bspwm").rglob("*.py"):
        f.chmod(0o755)


def step_components(distro: str):
    """Despliega components/: polybar y zsh por distro."""
    header("Aplicando componentes")

    for component in ["polybar"]:
        src  = REPO_DIR / "components" / component / distro
        dest = CONFIG_DIR / component
        if not src.exists():
            warn(f"{component}/{distro}/ no encontrado, omitiendo.")
            continue
        deploy_dir(src, dest)
        for f in dest.rglob("*.sh"):
            f.chmod(0o755)
        for f in dest.rglob("*.py"):
            f.chmod(0o755)
        ok(f"{component} ({distro}) aplicado.")

    # Zsh va al HOME
    zshrc = REPO_DIR / "components" / "zsh" / distro / ".zshrc"
    if zshrc.exists():
        shutil.copy2(zshrc, HOME / ".zshrc")
        ok("zsh aplicado.")
    else:
        warn(f"zsh/{distro}/.zshrc no encontrado, omitiendo.")


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

    distro = choose_distro()
    info(f"Sistema seleccionado: {distro}")

    handler = load_handler(distro)

    # 1. Dependencias
    header("Instalando dependencias")
    handler.deps(REPO_DIR, distro)

    # 2. Core
    step_core()

    # 3. Componentes
    step_components(distro)

    # 4. Post-instalación por distro
    header(f"Post-instalación ({distro})")
    handler.post(HOME, distro)

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

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
# Cuando se ejecuta con sudo, usar el home del usuario real (SUDO_USER)
_sudo_user   = os.environ.get("SUDO_USER")
HOME         = Path(f"/home/{_sudo_user}") if _sudo_user else Path.home()
CONFIG_DIR   = HOME / ".config"
FONTS_DIR    = HOME / ".local" / "share" / "fonts"

sys.path.insert(0, str(REPO_DIR / "scripts"))
from utils import ( # type: ignore
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
    """Despliega core/ → ~/.config/{bspwm,sxhkd,kitty,picom,rofi,wallpapers,scripts}."""
    header("Aplicando configuración core")

    for app in ("bspwm", "sxhkd", "kitty", "picom", "rofi", "wallpaper", "scripts"):
        src  = REPO_DIR / "core" / app
        # wallpaper se despliega en ~/.config/wallpapers (plural)
        dest = CONFIG_DIR / ("wallpaper" if app == "wallpaper" else app)
        if not src.exists():
            warn(f"core/{app}/ no encontrado en el repositorio, omitiendo.")
            continue
        deploy_dir(src, dest)
        ok(f"core/{app} → {dest}")

    # Permisos de ejecución
    bspwmrc = CONFIG_DIR / "bspwm" / "bspwmrc"
    if bspwmrc.exists():
        bspwmrc.chmod(0o755)
    for pattern in ("*.sh", "*.py"):
        for f in (CONFIG_DIR / "bspwm").rglob(pattern):
            f.chmod(0o755)
    # Scripts sin extensión en bspwm/scripts/ (ej: bspwm_resize)
    for f in (CONFIG_DIR / "bspwm" / "scripts").rglob("*"):
        if f.is_file():
            f.chmod(0o755)

    # Permisos de ejecución para scripts globales (~/.config/scripts/)
    scripts_dir = CONFIG_DIR / "scripts"
    if scripts_dir.exists():
        for f in scripts_dir.iterdir():
            if f.is_file():
                f.chmod(0o755)
                ok(f"{f.name} → ~/.config/scripts/{f.name}")

    # Permisos de ejecución para wallpaper.sh
    script = CONFIG_DIR / "wallpaper" / "wallpaper.sh"
    if script.exists():
        script.chmod(0o755)

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

    # Despliega temas de polybar (globales para todas las distros)
    themes_src = REPO_DIR / "components" / "polybar" / "themes"
    themes_dest = CONFIG_DIR / "polybar" / "themes"
    if themes_src.exists():
        deploy_dir(themes_src, themes_dest)
        ok("Temas de polybar (globales) aplicados.")

    # Despliega colors_active.ini (nivel superior, global)
    colors_src = REPO_DIR / "components" / "polybar" / "colors_active.ini"
    colors_dest = CONFIG_DIR / "polybar" / "colors_active.ini"
    if colors_src.exists():
        shutil.copy2(colors_src, colors_dest)
        ok("colors_active.ini (tema por defecto) aplicado.")

    # Zsh va al HOME
    zshrc = REPO_DIR / "components" / "zsh" / distro / ".zshrc"
    if zshrc.exists():
        target_zshrc = HOME / ".zshrc"
        # Backup si ya existe y es distinto
        if target_zshrc.exists():
            from datetime import datetime
            backup = HOME / f".zshrc.backup-{datetime.now():%Y%m%d-%H%M%S}"
            shutil.copy2(target_zshrc, backup)
            ok(f"Backup creado: {backup.name}")
        shutil.copy2(zshrc, target_zshrc)
        ok("zsh aplicado.")
    else:
        warn(f"zsh/{distro}/.zshrc no encontrado, omitiendo.")


def step_fonts():
    """Instala fuentes desde fonts/ y components/polybar/kali/fonts/."""
    header("Instalando fuentes")
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    sources = [
        REPO_DIR / "fonts",
        REPO_DIR / "components" / "polybar" / "kali" / "fonts",
    ]
    installed = 0
    for src in sources:
        if not src.exists():
            continue
        for f in src.rglob("*"):
            if f.is_file() and f.suffix in (".ttf", ".otf", ".woff", ".woff2"):
                shutil.copy2(f, FONTS_DIR / f.name)
                installed += 1
    if installed == 0:
        warn("No se encontraron fuentes, omitiendo.")
        return
    run(["fc-cache", "-fv"])
    ok(f"Fuentes instaladas ({installed} archivos).")


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

    # 6. Recargar
    step_reload()

    print(f"\n\033[1;32m╔════════════════════════════════════╗")
    print(f"║  Instalación completada con éxito  ║")
    print(f"╚════════════════════════════════════╝\033[0m")
    print(f"\n\033[0;33m➜  Cierra sesión y vuelve a entrar, o ejecuta: startx\033[0m\n")


if __name__ == "__main__":
    main()

"""
Handler de instalación para distros basadas en Debian
(Kali Linux, Parrot OS, Debian, Ubuntu).

Expone dos funciones públicas:
  deps(repo_dir)  — instala apt packages y compila desde fuente
  post(home)      — instala Oh My Zsh, crea ~/.xinitrc
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
from utils import info, ok, warn, die, header, run, run_shell


# ── Paquetes a compilar desde fuente ─────────────────────────
SOURCE_REPOS = {
    "bspwm": {
        "url":        "https://github.com/baskerville/bspwm.git",
        "deps": [
            "libxcb1-dev", "libxcb-util0-dev", "libxcb-ewmh-dev",
            "libxcb-randr0-dev", "libxcb-icccm4-dev",
            "libxcb-keysyms1-dev", "libxcb-xinerama0-dev",
            "libxcb-shape0-dev", "libxcb-xfixes0-dev",
        ],
        "submodules": False,
        "build":      "make",
        "install":    ["make", "install"],
    },
    "sxhkd": {
        "url":        "https://github.com/baskerville/sxhkd.git",
        "deps": [
            "libxcb1-dev", "libxcb-keysyms1-dev", "libxcb-util0-dev",
            "libxcb-xtest0-dev", "libxcb-xkb-dev",
            "libxkbcommon-dev", "libxkbcommon-x11-dev", "libasound2-dev",
        ],
        "submodules": False,
        "build":      "make clean && make",
        "install":    ["make", "install"],
    },
    "picom": {
        "url":        "https://github.com/ibhagwan/picom.git",
        "deps": [
            "meson", "ninja-build", "cmake", "libxext-dev",
            "libxcb1-dev", "libxcb-damage0-dev", "libxcb-xfixes0-dev",
            "libxcb-shape0-dev", "libxcb-render-util0-dev", "libxcb-render0-dev",
            "libxcb-randr0-dev", "libxcb-composite0-dev", "libxcb-image0-dev",
            "libxcb-present-dev", "libxcb-xinerama0-dev", "libxcb-glx0-dev",
            "libpixman-1-dev", "libdbus-1-dev", "libconfig-dev",
            "libgl1-mesa-dev", "libpcre3-dev", "libev-dev", "uthash-dev",
            "libevdev-dev", "libx11-xcb-dev", "libepoxy-dev",
        ],
        "submodules": True,
        "build":      "meson setup --buildtype=release build && ninja -C build",
        "install":    ["ninja", "-C", "build", "install"],
    },
    "polybar": {
        "url":        "https://github.com/polybar/polybar.git",
        "deps": [
            "cmake", "build-essential", "libcairo2-dev",
            "libxcb1-dev", "libxcb-ewmh-dev", "libxcb-icccm4-dev",
            "libxcb-image0-dev", "libxcb-randr0-dev", "libxcb-util0-dev",
            "libxcb-xkb-dev", "libxcb-xrm-dev", "libxcb-composite0-dev",
            "libxcb-cursor-dev", "python3-xcbgen", "xcb-proto",
            "libasound2-dev", "libmpdclient-dev", "libiw-dev",
            "libcurl4-openssl-dev", "libpulse-dev",
        ],
        "submodules": True,
        "build":      (
            "cmake -DCMAKE_BUILD_TYPE=Release -S . -B build && "
            "cmake --build build --parallel $(nproc)"
        ),
        "install":    ["cmake", "--install", "build"],
    },
}

# Paquetes apt base + herramientas del entorno
APT_BASE = [
    "build-essential", "git", "pkg-config",
    "python3", "python3-pip",
]

APT_TOOLS = [
    "kitty", "feh", "rofi", "dunst",
    "xclip", "xdotool", "wmctrl", "lxappearance",
    "papirus-icon-theme", "ranger",
    "zsh", "flameshot", "numlockx",
    "imagemagick", "curl", "wget", "unzip",
    "fonts-hack-ttf", "scrot",
]


# ── Helpers internos ──────────────────────────────────────────
def _apt_install(packages: list[str]) -> None:
    unique = list(dict.fromkeys(packages))
    info(f"apt install: {len(unique)} paquetes...")
    run(["apt", "install", "-y"] + unique)


def _clone_and_build(name: str, spec: dict, build_dir: Path) -> None:
    dest = build_dir / name
    if dest.exists():
        warn(f"{name} ya clonado en {dest}, omitiendo clone.")
    else:
        info(f"Clonando {name}...")
        run(["git", "clone", spec["url"], str(dest)])

    if spec.get("submodules"):
        info(f"Inicializando submódulos de {name}...")
        run(["git", "submodule", "update", "--init", "--recursive"], cwd=dest)

    info(f"Compilando {name}...")
    run_shell(spec["build"], cwd=dest)

    info(f"Instalando {name}...")
    run(spec["install"], cwd=dest)
    ok(f"{name} instalado.")


def _read_packages(repo_dir: Path) -> list[str]:
    pkg_file = repo_dir / "distros" / "debian" / "packages.txt"
    if not pkg_file.exists():
        die(f"packages.txt no encontrado en {pkg_file}")
    return [
        line.strip()
        for line in pkg_file.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


# ── API pública ───────────────────────────────────────────────
def deps(repo_dir: Path) -> None:
    """Instala dependencias apt y compila bspwm/sxhkd/picom/polybar."""
    build_dir = Path.home() / "Downloads" / "bspwm-build"
    build_dir.mkdir(parents=True, exist_ok=True)

    header("Actualizando sistema (apt update)")
    run(["apt", "update"])

    header("Dependencias base")
    _apt_install(APT_BASE)

    # Paquetes del packages.txt (herramientas, fuentes, etc.)
    header("Paquetes del entorno")
    _apt_install(_read_packages(repo_dir))
    _apt_install(APT_TOOLS)

    # Compilar desde fuente
    for name, spec in SOURCE_REPOS.items():
        header(f"Compilando {name.upper()} desde fuente")
        _apt_install(spec["deps"])
        _clone_and_build(name, spec, build_dir)


def post(home: Path) -> None:
    """Acciones post-instalación para Debian/Kali/Parrot."""
    header("Post-instalación Debian/Kali/Parrot")

    # Oh My Zsh
    omz_dir = home / ".oh-my-zsh"
    if omz_dir.exists():
        warn("Oh My Zsh ya instalado, omitiendo.")
    else:
        info("Instalando Oh My Zsh...")
        run_shell(
            "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
            " | bash --unattended"
        )
        ok("Oh My Zsh instalado.")

    # .xinitrc
    xinitrc = home / ".xinitrc"
    if not xinitrc.exists():
        xinitrc.write_text("#!/bin/sh\nexec bspwm\n")
        xinitrc.chmod(0o755)
        ok(f"{xinitrc} creado.")
    else:
        warn(f"{xinitrc} ya existe, omitiendo.")

    ok("Post-instalación Debian completada.")

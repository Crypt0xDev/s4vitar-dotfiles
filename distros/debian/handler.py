"""
Handler de instalación para distros basadas en Debian
(Kali Linux, Parrot OS, Debian, Ubuntu).

Expone dos funciones públicas:
  deps(repo_dir)  — instala apt packages y compila desde fuente
  post(home)      — instala Powerlevel10k, crea ~/.xinitrc
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
from utils import info, ok, warn, die, header, run, run_shell # type: ignore


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
            "libgl-dev", "libpcre2-dev", "libev-dev", "uthash-dev",
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
            "libasound2-dev", "libmpdclient-dev",
            "libcurl4-openssl-dev", "libpulse-dev",
        ],
        "submodules": True,
        "build":      (
            "cmake -DCMAKE_BUILD_TYPE=Release -DWITH_LIBIW=OFF -S . -B build && "
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
    "scrot",
]

# Nerd Fonts necesarias para polybar (iconos)
NERD_FONTS = [
    ("Hack",   "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.zip"),
    ("FiraCode", "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip"),
]


def _install_nerd_fonts() -> None:
    """Descarga e instala Hack Nerd Font y FiraCode Nerd Font."""
    import shutil
    import zipfile
    fonts_dir = Path.home() / ".local" / "share" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    tmp = Path("/tmp/nerd-fonts")
    tmp.mkdir(exist_ok=True)

    for name, url in NERD_FONTS:
        zip_path = tmp / f"{name}.zip"
        info(f"Descargando {name} Nerd Font...")
        if not run(["curl", "-fsSL", "-o", str(zip_path), url]):
            warn(f"No se pudo descargar {name} Nerd Font.")
            continue
        with zipfile.ZipFile(zip_path, "r") as z:
            for member in z.namelist():
                if member.endswith(".ttf") and "Windows" not in member:
                    z.extract(member, fonts_dir)
                    # mover al raíz de fonts_dir si quedó en subcarpeta
                    extracted = fonts_dir / member
                    if extracted.parent != fonts_dir:
                        extracted.rename(fonts_dir / extracted.name)
        ok(f"{name} Nerd Font instalada.")

    run(["fc-cache", "-fv"])


# ── Helpers internos ─────────────────────────────────────────
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


def _read_packages(repo_dir: Path, distro: str) -> list[str]:
    """
    Carga packages.txt (base) + packages-{distro}.txt (específico).
    Las listas se fusionan eliminando duplicados.
    """
    debian_dir = repo_dir / "distros" / "debian"

    def _load(path: Path) -> list[str]:
        if not path.exists():
            return []
        return [
            line.strip()
            for line in path.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        ]

    base = _load(debian_dir / "packages.txt")
    if not base:
        die(f"packages.txt no encontrado en {debian_dir}")

    specific_file = debian_dir / f"packages-{distro}.txt"
    specific = _load(specific_file)
    if specific:
        info(f"Cargando paquetes específicos de {distro} ({specific_file.name})")
    else:
        warn(f"No hay packages-{distro}.txt, usando solo base.")

    # Fusionar manteniendo orden y sin duplicados
    seen = set()
    result = []
    for pkg in base + specific:
        if pkg not in seen:
            seen.add(pkg)
            result.append(pkg)
    return result


# ── API pública ───────────────────────────────────────────────
def deps(repo_dir: Path, distro: str = "debian") -> None:
    """Instala dependencias apt y compila bspwm/sxhkd/picom/polybar."""
    build_dir = Path("/tmp/bspwm-build")
    build_dir.mkdir(parents=True, exist_ok=True)

    header("Actualizando sistema (apt update)")
    run(["apt", "update"])

    header("Dependencias base")
    _apt_install(APT_BASE)

    # Paquetes del packages.txt + packages-{distro}.txt
    header(f"Paquetes del entorno ({distro})")
    _apt_install(_read_packages(repo_dir, distro))
    _apt_install(APT_TOOLS)

    # Nerd Fonts (Hack + FiraCode) para polybar
    header("Instalando Nerd Fonts")
    _install_nerd_fonts()

    # Compilar desde fuente
    for name, spec in SOURCE_REPOS.items():
        header(f"Compilando {name.upper()} desde fuente")
        _apt_install(spec["deps"])
        _clone_and_build(name, spec, build_dir)


def post(home: Path, distro: str = "debian") -> None:
    """Acciones post-instalación para Debian/Kali/Parrot."""
    header("Post-instalación Debian/Kali/Parrot")

    # Powerlevel10k
    p10k_dir = home / "powerlevel10k"
    if p10k_dir.exists():
        warn("Powerlevel10k ya instalado, omitiendo.")
    else:
        info("Instalando Powerlevel10k...")
        run(["git", "clone", "--depth=1",
             "https://github.com/romkatv/powerlevel10k.git",
             str(p10k_dir)])
        ok("Powerlevel10k instalado.")
    # Nota: el .zshrc del repo ya contiene la lógica para cargar p10k
    # condicionalmente según ~/.p10k_theme, no añadimos source duplicado.

    # .xinitrc
    xinitrc = home / ".xinitrc"
    if not xinitrc.exists():
        xinitrc.write_text("#!/bin/sh\nexec bspwm\n")
        xinitrc.chmod(0o755)
        ok(f"{xinitrc} creado.")
    else:
        warn(f"{xinitrc} ya existe, omitiendo.")

    ok("Post-instalación Debian completada.")

"""
Handler de instalación para Arch Linux (y derivados: Manjaro, EndeavourOS…).
Expone dos funciones públicas:
  deps(repo_dir)  — instala paquetes y picom-ibhagwan desde AUR
  post(home)      — crea ~/.xinitrc si no existe
"""

from pathlib import Path
import sys

# Utils del repo
sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
from utils import info, ok, warn, die, header, run, run_shell


# ── Dependencias de compilación de picom ibhagwan ────────────
PICOM_AUR_PKG = "picom-ibhagwan-git"


def _read_packages(repo_dir: Path) -> list[str]:
    """Lee distros/arch/packages.txt y devuelve la lista de paquetes."""
    pkg_file = repo_dir / "distros" / "arch" / "packages.txt"
    if not pkg_file.exists():
        die(f"packages.txt no encontrado en {pkg_file}")
    pkgs = [
        line.strip()
        for line in pkg_file.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    return pkgs


def _has_yay() -> bool:
    return run(["which", "yay"], check=False)


def _install_yay() -> bool:
    """Instala yay desde el repositorio oficial."""
    info("Instalando yay (AUR helper)...")
    tmp = Path("/tmp/yay-bin")
    if not run(["git", "clone", "https://aur.archlinux.org/yay-bin.git", str(tmp)]):
        return False
    return run_shell("makepkg -si --noconfirm", cwd=tmp)


# ── API pública ───────────────────────────────────────────────
def deps(repo_dir: Path) -> None:
    """Instala todos los paquetes necesarios para Arch."""
    header("Actualizando sistema (pacman -Syu)")
    run(["pacman", "-Syu", "--noconfirm"])

    packages = _read_packages(repo_dir)
    info(f"Instalando {len(packages)} paquetes via pacman...")
    run(["pacman", "-S", "--noconfirm", "--needed"] + packages)
    ok("Paquetes base instalados.")

    # picom ibhagwan desde AUR
    header("Instalando picom (ibhagwan fork) desde AUR")
    if not _has_yay():
        warn("yay no encontrado. Intentando instalar...")
        if not _install_yay():
            warn("No se pudo instalar yay. Usando picom estándar de los repositorios.")
            run(["pacman", "-S", "--noconfirm", "--needed", "picom"])
            return

    if run(["yay", "-S", "--noconfirm", "--needed", PICOM_AUR_PKG], check=False):
        ok(f"{PICOM_AUR_PKG} instalado.")
    else:
        warn("Falló la instalación del fork AUR. Usando picom estándar.")
        run(["pacman", "-S", "--noconfirm", "--needed", "picom"])


def post(home: Path) -> None:
    """Acciones post-instalación para Arch."""
    header("Post-instalación Arch")

    xinitrc = home / ".xinitrc"
    if not xinitrc.exists():
        xinitrc.write_text("#!/bin/sh\nexec bspwm\n")
        xinitrc.chmod(0o755)
        ok(f"{xinitrc} creado.")
    else:
        warn(f"{xinitrc} ya existe, omitiendo.")

    ok("Post-instalación Arch completada.")

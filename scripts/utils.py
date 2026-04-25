"""
Utilidades compartidas para el instalador bspwm-dotfiles.
"""

import os
import shutil
import subprocess
from pathlib import Path

# ── Colores ANSI ─────────────────────────────────────────────
RED    = "\033[0;31m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE   = "\033[0;34m"
CYAN   = "\033[0;36m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ── Logging ──────────────────────────────────────────────────
def info(msg: str):
    print(f"{BLUE}[*]{RESET} {msg}")


def ok(msg: str):
    print(f"{GREEN}[✔]{RESET} {msg}")


def warn(msg: str):
    print(f"{YELLOW}[!]{RESET} {msg}")


def die(msg: str):
    print(f"{RED}[✘]{RESET} {msg}")
    raise SystemExit(1)


def header(msg: str):
    print(f"\n{CYAN}{BOLD}══ {msg} ══{RESET}")


def print_banner():
    banner = f"""
{CYAN}{BOLD}
 ██████╗ ███████╗██████╗ ██╗    ██╗███╗   ███╗
 ██╔══██╗██╔════╝██╔══██╗██║    ██║████╗ ████║
 ██████╔╝███████╗██████╔╝██║ █╗ ██║██╔████╔██║
 ██╔══██╗╚════██║██╔═══╝ ██║███╗██║██║╚██╔╝██║
 ██████╔╝███████║██║     ╚███╔███╔╝██║ ╚═╝ ██║
 ╚═════╝ ╚══════╝╚═╝      ╚══╝╚══╝ ╚═╝     ╚═╝
         s4vitar style  ·  Arch · Kali · Parrot
{RESET}"""
    print(banner)


# ── Ejecución de comandos ────────────────────────────────────
def run(cmd: list, cwd: Path = None, shell: bool = False, check: bool = True) -> bool:
    """
    Ejecuta un comando. Devuelve True si tuvo éxito.
    Si check=False no lanza excepción aunque falle.
    """
    try:
        subprocess.run(
            cmd,
            shell=shell,
            cwd=str(cwd) if cwd else None,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        if check:
            print(f"{RED}[✘]{RESET} Comando fallido: {e.cmd}")
            if e.stderr:
                print(f"  {RED}{e.stderr[:400].strip()}{RESET}")
        return False


def run_shell(cmd: str, cwd: Path = None) -> bool:
    """Ejecuta un comando de shell (con &&, pipes, etc.)."""
    return run(cmd, cwd=cwd, shell=True)


# ── Detección de distro ──────────────────────────────────────
def detect_distro() -> str:
    """
    Lee /etc/os-release y devuelve un identificador normalizado:
    'arch' | 'kali' | 'parrot' | 'debian' | 'ubuntu' | distro-id desconocida.
    Usa ID_LIKE como fallback si ID no está en el mapa.
    """
    os_release = Path("/etc/os-release")
    if not os_release.exists():
        die("/etc/os-release no encontrado. ¿Estás en Linux?")

    values: dict[str, str] = {}
    with os_release.open() as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                values[key.strip()] = val.strip().strip('"')

    distro_id   = values.get("ID", "").lower()
    id_like     = values.get("ID_LIKE", "").lower()

    KNOWN = {"arch", "manjaro", "kali", "parrot", "debian", "ubuntu"}

    if distro_id in KNOWN:
        return distro_id

    # fallback: primer token de ID_LIKE que reconozcamos
    for token in id_like.split():
        if token in KNOWN:
            return token

    return distro_id or "unknown"


# ── Despliegue de configuraciones ────────────────────────────
def deploy_dir(src: Path, dest: Path) -> None:
    """
    Copia recursivamente src/ → dest/.
    Crea dest si no existe. Sobreescribe archivos existentes.
    """
    if not src.exists():
        warn(f"Fuente no encontrada, omitiendo: {src}")
        return

    dest.mkdir(parents=True, exist_ok=True)

    for item in src.rglob("*"):
        if item.is_file():
            rel    = item.relative_to(src)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)

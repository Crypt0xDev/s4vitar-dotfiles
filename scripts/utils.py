"""
Utilidades compartidas para el instalador
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
         s4vitar  ·  Arch · Kali · Parrot
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

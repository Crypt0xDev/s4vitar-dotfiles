#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════╗
# ║   wallpaper.sh — Aplica el wallpaper actual          ║
# ║   Uso: wallpaper.sh [archivo]                        ║
# ║   Sin argumento: usa s4vitar.png por defecto         ║
# ╚══════════════════════════════════════════════════════╝

WP_DIR="${HOME}/.config/wallpaper"
WALLPAPER="${1:-${WP_DIR}/s4vitar.png}"

# Si pasaron solo un nombre, buscarlo en WP_DIR
if [ ! -f "$WALLPAPER" ] && [ -f "${WP_DIR}/${1}" ]; then
    WALLPAPER="${WP_DIR}/${1}"
fi

if [ ! -f "$WALLPAPER" ]; then
    echo "[!] Wallpaper no encontrado: $WALLPAPER"
    exit 1
fi

if ! command -v feh >/dev/null 2>&1; then
    echo "[!] feh no está instalado"
    exit 1
fi

feh --bg-fill "$WALLPAPER"

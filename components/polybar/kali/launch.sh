#!/usr/bin/env sh

## Uso: launch.sh [s4vitar|htb|purple]
##
##   s4vitar  → S4vitar (tema por defecto)
##   htb      → Hack The Box
##   purple   → Kali Purpure

CONFIG_DIR="${HOME}/.config/polybar"
ROFI_THEMES_DIR="$CONFIG_DIR/scripts/themes"
THEME="${1:-s4vitar}"

# Selecciona el tema de colores y escribe el acento para los scripts
case "$THEME" in
    htb)
        cp -f "$CONFIG_DIR/themes/htb/colors.ini"     "$CONFIG_DIR/colors_active.ini"
        echo "#9FEF00" > "$CONFIG_DIR/theme_accent"
        echo "htb" > "${HOME}/.p10k_theme"
        ;;
    purple)
        cp -f "$CONFIG_DIR/themes/purple/colors.ini"  "$CONFIG_DIR/colors_active.ini"
        echo "#A855F7" > "$CONFIG_DIR/theme_accent"
        echo "purple" > "${HOME}/.p10k_theme"
        ;;
    *)
        cp -f "$CONFIG_DIR/themes/s4vitar/colors.ini" "$CONFIG_DIR/colors_active.ini"
        echo "#FEC006" > "$CONFIG_DIR/theme_accent"
        echo "s4vitar" > "${HOME}/.p10k_theme"
        ;;
esac

# ═══════════════════════════════════════════════════════════════
#  Generar colors.rasi de Rofi desde los colores de Polybar
# ═══════════════════════════════════════════════════════════════
BG=$(grep "^bg" "$CONFIG_DIR/colors_active.ini" | awk '{print $3}')
FG=$(grep "^fg" "$CONFIG_DIR/colors_active.ini" | awk '{print $3}')
AC=$(grep "^ac" "$CONFIG_DIR/colors_active.ini" | awk '{print $3}')
DIM=$(grep "^dim" "$CONFIG_DIR/colors_active.ini" | awk '{print $3}')
RED=$(grep "^red" "$CONFIG_DIR/colors_active.ini" | awk '{print $3}')

cat > "$ROFI_THEMES_DIR/colors.rasi" << EOF
/* ════════════════════════════════════════════
   Tema ACTIVO de Rofi
   Generado automáticamente desde: polybar/themes/$THEME/colors.ini
   ════════════════════════════════════════════ */

* {
    background:     ${BG}ff;
    background-alt: #1a1a1aff;
    foreground:     ${FG}ff;
    border:         ${AC}ff;
    selected:       ${AC}ff;
    urgent:         ${RED}ff;
    logo:           ${AC}ff;
    on:             ${AC}ff;
    off:            ${DIM}ff;
}
EOF

# ═══════════════════════════════════════════════════════════════
#  Sincronizar colores de borde de bspwm con el tema activo
# ═══════════════════════════════════════════════════════════════
bspc config focused_border_color  "${AC}"
bspc config normal_border_color   "${DIM}"
bspc config active_border_color   "${DIM}"
bspc config presel_feedback_color "${AC}"

# Permisos de ejecución en scripts
chmod +x "$CONFIG_DIR"/scripts/*.sh 2>/dev/null
chmod +x "$CONFIG_DIR"/scripts/bin/*.sh 2>/dev/null

# Termina instancias anteriores
killall -q polybar
while pgrep -x polybar >/dev/null; do sleep 1; done

# Lanza las 7 barras pill-shaped
polybar logo       -c "$CONFIG_DIR/current.ini" &
polybar date       -c "$CONFIG_DIR/current.ini" &
polybar network    -c "$CONFIG_DIR/current.ini" &
polybar vpn        -c "$CONFIG_DIR/current.ini" &
polybar workspaces -c "$CONFIG_DIR/current.ini" &
polybar target     -c "$CONFIG_DIR/current.ini" &
polybar sysmenu    -c "$CONFIG_DIR/current.ini" &

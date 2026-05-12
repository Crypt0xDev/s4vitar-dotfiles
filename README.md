<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=28&pause=1000&color=BD93F9&center=true&vCenter=true&width=600&lines=s4vitar%20dotfiles;bspwm+%7C+Dracula+%7C+Pentesting" alt="s4vitar%20dotfiles" />

<br/>

[![OS](https://img.shields.io/badge/Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org)
[![OS](https://img.shields.io/badge/Parrot%20OS-00ADEF?style=for-the-badge&logo=linux&logoColor=white)](https://parrotsec.org)
[![OS](https://img.shields.io/badge/Arch%20Linux-1793D1?style=for-the-badge&logo=archlinux&logoColor=white)](https://archlinux.org)

[![WM](https://img.shields.io/badge/bspwm-282a36?style=for-the-badge&logoColor=bd93f9)](https://github.com/baskerville/bspwm)
[![Python](https://img.shields.io/badge/Python_3.10+-bd93f9?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Theme](https://img.shields.io/badge/Dracula-ff79c6?style=for-the-badge)](https://draculatheme.com)
[![License](https://img.shields.io/badge/MIT-44475a?style=for-the-badge)](LICENSE)

<br/>

> Entorno de pentesting completo basado en la configuración de **[s4vitar](https://github.com/s4vitar)**
> Un solo comando — selección de distro — compilación desde fuente

</div>

## Preview

> Añade aquí un screenshot o GIF del entorno una vez instalado.
> Recomendado: `scrot ~/screenshot.png` o `flameshot gui`

## Prerrequisitos

Ejecuta el comando de tu distro **antes de clonar**:

**Kali Linux / Parrot OS**
```bash
sudo apt update && sudo apt install -y python3 git curl make gcc build-essential xorg
```

**Arch Linux**
```bash
sudo pacman -Syu --noconfirm python git curl base-devel xorg
```

> **Kali en modo Live:** los cambios no persisten al reiniciar. Usa una instalación completa en disco.


## Instalación

Una vez cumplidos los prerrequisitos:

```bash
git clone --depth 1 https://github.com/Crypt0xDev/s4vitar-dotfiles.git
cd s4vitar-dotfiles
sudo python3 install.py
```

### Flujo del instalador

```
[1] Selección manual de distro
[2] Verificación de prerrequisitos
[3] Instala dependencias  ──  apt / pacman
[4] Compila desde fuente  ──  bspwm · sxhkd · picom (ibhagwan) · polybar
[5] Despliega core/       ──  ~/.config/{bspwm, sxhkd, kitty, picom, rofi}
[6] Despliega components/ ──  polybar · zsh  (específico por distro)
[7] Post-instalación      ──  Powerlevel10k · .xinitrc
[8] Fuentes + wallpapers
[9] Recarga bspwm
```

## Arquitectura

```
s4vitar-dotfiles/
├── install.py                        # Orquestador: menú distro → preflight → instalación
├── scripts/
│   └── utils.py                      # Logging · run() · deploy_dir()
│
├── core/                             # Configuración idéntica en todas las distros
│   ├── bspwm/                        # Gestor de ventanas
│   ├── sxhkd/                        # Atajos de teclado y shorkuts
│   ├── kitty/                        # Terminal + 3 temas (s4vitar, htb, purple)
│   │   └── themes/                   # s4vitar (default), htb, purple
│   ├── picom/                        # Trasparencias y efectos
│   ├── rofi/                         # Lanzador + 3 temas (s4vitar, htb, purple)
│   │   └── themes/                   # s4vitar (default), htb, purple
│   └── scripts/                      # launch_theme.sh (orquestador global)
│
├── components/                       # Configuración específica por distro
│   ├── polybar/
│   │   ├── themes/                   # ★ TEMAS GLOBALES (3 temas: s4vitar, htb, purple)
│   │   │   ├── s4vitar/
│   │   │   │   └── colors.ini        # Ámbar #FEC006
│   │   │   ├── htb/
│   │   │   │   └── colors.ini        # Verde #9FEF00
│   │   │   └── purple/
│   │   │       └── colors.ini        # Violeta #A855F7
│   │   ├── colors_active.ini         # ★ Tema activo (copiado de themes/)
│   │   ├── kali/                     # Kali Linux (6 barras pill)
│   │   │   └── unified.ini
│   │   ├── parrot/                   # Parrot OS (barra única)
│   │   │   └── config.ini
│   │   └── arch/                     # Arch Linux (barra única)
│   │       └── config.ini
│   └── zsh/
│       ├── kali/                     # Paths Kali alias + 3 configs p10k (s4vitar, htb, purple)
│       ├── parrot/                   # Paths Parrot alias, etc.
│       └── arch/                     # Paths Arch alias, etc.
│
├── distros/
│   ├── arch/
│   │   ├── handler.py                # pacman + yay + picom-ibhagwan-git (AUR)
│   │   └── packages.txt
│   └── debian/                       # Kali · Parrot
│       ├── handler.py                # Compilación desde fuente: bspwm·sxhkd·picom·polybar
│       ├── packages.txt              # Paquetes base comunes
│       ├── packages-kali.txt         # Paquetes exclusivos de Kali
│       └── packages-parrot.txt       # Paquetes exclusivos de Parrot
│
├── docs/
│   └── manual.md                     # Guía de compilación manual paso a paso
├── wallpapers/                       # → ~/Pictures/wallpapers/
└── fonts/                            # → ~/.local/share/fonts/
```

## Keybindings

| Atajo | Acción |
|:------|:-------|
| `Super + Enter` | Terminal — kitty |
| `Super + D` | Lanzador — rofi |
| `Super + Shift + T` | **Selector de temas** — menú visual |
| `Super + W` | Cerrar ventana |
| `Super + F` | Pantalla completa |
| `Super + S` | Modo flotante |
| `Super + H/J/K/L` | Navegar ventanas |
| `Super + 1–0` | Cambiar escritorio |
| `Super + Shift + 1–0` | Mover ventana al escritorio |
| `Super + Alt + R` | Recargar bspwm |
| `Print` | Captura de pantalla |

## Temas

### 🎨 Selector visual (recomendado)
Presiona `Super + Shift + T` para abrir el menú de temas. Selecciona uno y todo cambia:

```
🟡 s4vitar — Ámbar clásico • #FEC006
🟢 htb — Verde neón HTB • #9FEF00
🟣 purple — Violeta cyberpunk • #A855F7
```

### ⌨️ Cambio por comando (alternativo)
```bash
theme s4vitar   # Ámbar (default) — fondo muy oscuro #0a0a0a
theme htb       # Verde HTB — negro puro #050505
theme purple    # Violeta — púrpura oscuro #0d0515
```

El tema persiste entre sesiones. Ver detalles completos en [THEMES.md](THEMES.md).


## Disclaimer

> Este entorno está diseñado exclusivamente para **seguridad ofensiva en entornos controlados y autorizados** (CTFs, laboratorios, máquinas propias).
>
> El uso de estas herramientas contra sistemas sin autorización expresa es **ilegal**. El autor no se hace responsable del mal uso de este software.
>
> **Usa este entorno de forma ética y responsable.**

<div align="center">

Configuración original de **[s4vitar](https://github.com/s4vitar)** — empaquetada por **[Crypt0xDev](https://github.com/Crypt0xDev)**

</div>

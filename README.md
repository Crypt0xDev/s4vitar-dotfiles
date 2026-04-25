<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=28&pause=1000&color=BD93F9&center=true&vCenter=true&width=600&lines=s4vitar-dotfiles;bspwm+%7C+Dracula+%7C+Pentesting" alt="s4vitar-dotfiles" />

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
> Un solo comando — detección automática de distro — compilación desde fuente

</div>

---

## Instalación

```bash
git clone --depth 1 https://github.com/Crypt0xDev/s4vitar-dotfiles.git
cd s4vitar-dotfiles
sudo python3 install.py
```

### Flujo del instalador

```
[1] Detecta distro (/etc/os-release)
[2] Instala dependencias  ──  apt / pacman
[3] Compila desde fuente  ──  bspwm · sxhkd · picom (ibhagwan) · polybar
[4] Despliega core/       ──  ~/.config/bspwm  +  ~/.config/sxhkd
[5] Despliega components/ ──  polybar · rofi · zsh
[6] Post-instalación      ──  Oh My Zsh · .xinitrc
[7] Fuentes + wallpapers
[8] Recarga bspwm
```

---

## Arquitectura

```
s4vitar-dotfiles/
├── install.py                        # Orquestador principal
│
├── core/                             # Config base — todas las distros
│   ├── bspwm/
│   │   ├── bspwmrc
│   │   └── scripts/autostart.py
│   └── sxhkd/sxhkdrc
│
├── components/                       # Módulos independientes
│   ├── polybar/shared/               # config.ini · launch.py
│   ├── rofi/shared/config.rasi
│   └── zsh/shared/.zshrc
│
├── distros/
│   ├── arch/
│   │   ├── handler.py                # pacman + AUR (picom-ibhagwan-git)
│   │   └── packages.txt
│   └── debian/                       # Kali · Parrot
│       ├── handler.py                # compilación desde fuente
│       └── packages.txt
│
├── scripts/utils.py                  # run · detect_distro · deploy_dir
├── wallpapers/
└── fonts/
```

---

## Keybindings

| Atajo | Acción |
|:------|:-------|
| `Super + Enter` | Terminal — kitty |
| `Super + D` | Lanzador — rofi |
| `Super + W` | Cerrar ventana |
| `Super + F` | Pantalla completa |
| `Super + S` | Modo flotante |
| `Super + H/J/K/L` | Navegar ventanas |
| `Super + 1–0` | Cambiar escritorio |
| `Super + Shift + 1–0` | Mover ventana al escritorio |
| `Super + Alt + R` | Recargar bspwm |
| `Print` | Captura de pantalla |

---

## Stack

| Componente | Herramienta |
|:-----------|:------------|
| Window Manager | bspwm + sxhkd |
| Terminal | kitty |
| Compositor | picom — ibhagwan fork |
| Barra de estado | polybar |
| Lanzador | rofi |
| Notificaciones | dunst |
| File manager | ranger |
| Tema | Dracula |

---

<div align="center">

Configuración original de **[s4vitar](https://github.com/s4vitar)** — empaquetada por **[Crypt0xDev](https://github.com/Crypt0xDev)**

</div>

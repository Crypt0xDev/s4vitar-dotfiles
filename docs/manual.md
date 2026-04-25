# Bspwm #

sudo apt update

1. Dependencias
sudo apt install -y \
build-essential git pkg-config \
libxcb1-dev libxcb-util0-dev libxcb-ewmh-dev \
libxcb-randr0-dev libxcb-icccm4-dev \
libxcb-keysyms1-dev libxcb-xinerama0-dev \
libxcb-shape0-dev libxcb-xfixes0-dev

2. Clonar repo
cd ~/Descargas
git clone https://github.com/baskerville/bspwm.git
cd bspwm

3. Compilar
make

4. Instalar
sudo make install

# Sxhkd #

sudo apt update

1. Dependencias
sudo apt install -y \
build-essential git pkg-config \
libxcb1-dev libxcb-keysyms1-dev libxcb-util0-dev \
libxcb-xtest0-dev libxcb-xkb-dev \
libxkbcommon-dev libxkbcommon-x11-dev \
libasound2-dev

2. Clonar repo
cd ~/Descargas
git clone https://github.com/baskerville/sxhkd.git
cd sxhkd

3. Compilar
make clean
make

4. Instalar
sudo make install

# Picón #

sudo apt update

1. Dependencias
sudo apt install -y \
git meson ninja-build pkg-config cmake \
libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev \
libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev \
libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev \
libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev \
libpixman-1-dev libdbus-1-dev libconfig-dev \
libgl1-mesa-dev libpcre3-dev libev-dev uthash-dev \
libevdev-dev libx11-xcb-dev \
libepoxy-dev

2. Clonar repo
cd ~/Descargas
git clone https://github.com/ibhagwan/picom.git
cd picom

3. Submódulos
git submodule update --init --recursive

4. Compilar
meson setup --buildtype=release build
ninja -C build

5. Instalar
sudo ninja -C build install

# Polybar

# Otro

sudo app install Kitty feh

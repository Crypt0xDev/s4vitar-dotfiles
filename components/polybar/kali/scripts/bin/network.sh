#!/bin/sh

ACCENT=$(cat ~/.config/polybar/theme_accent 2>/dev/null || echo "#FEC006")

# Comprueba eth0
ETH_IP=$(/usr/sbin/ifconfig eth0 2>/dev/null | grep "inet " | awk '{print $2}')
if [ -n "$ETH_IP" ]; then
    echo "%{F${ACCENT}}%{T3}󰈀%{T-} $ETH_IP%{F-}"   # 󰈀 nf-md-ethernet
    exit 0
fi

# Comprueba wlan0
WIFI_IP=$(/usr/sbin/ifconfig wlan0 2>/dev/null | grep "inet " | awk '{print $2}')
if [ -n "$WIFI_IP" ]; then
    SSID=$(iwgetid -r 2>/dev/null || echo "WiFi")
    echo "%{F${ACCENT}}%{T3}%{T-} $WIFI_IP ($SSID)%{F-}"   #  nf-md-wifi
    exit 0
fi

# Sin conexión
echo "%{F${ACCENT}}%{T3}%{T-} Disconnected%{F-}"   #  nf-md-wifi_off

#!/bin/sh

ACCENT=$(cat ~/.config/polybar/theme_accent 2>/dev/null || echo "#FEC006")
IFACE=$(/usr/sbin/ifconfig | grep tun0 | awk '{print $1}' | tr -d ':')

if [ "$IFACE" = "tun0" ]; then
	echo "%{F${ACCENT}} %{F#ffffff}$(/usr/sbin/ifconfig tun0 | grep "inet " | awk '{print $2}')%{u-}"
else
	echo "%{F${ACCENT}}%{u-} Disconnected"
fi

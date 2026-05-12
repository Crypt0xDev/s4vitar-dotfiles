#!/bin/sh

ACCENT=$(cat ~/.config/polybar/theme_accent 2>/dev/null || echo "#FEC006")
ip_target=$(cat ~/.config/polybar/scripts/bin/target 2>/dev/null | awk '{print $1}')
name_target=$(cat ~/.config/polybar/scripts/bin/target 2>/dev/null | awk '{print $2}')

if [ "$ip_target" ] && [ "$name_target" ]; then
	echo "%{F${ACCENT}}什%{F#ffffff} $ip_target - $name_target"
elif [ -n "$ip_target" ]; then
	echo "%{F${ACCENT}}什%{F#ffffff} $ip_target"
else
	echo "%{F${ACCENT}}ﲅ %{u-}%{F#ffffff} No target"
fi

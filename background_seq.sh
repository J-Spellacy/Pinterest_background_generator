#!/bin/bash

# this is to be used in your waybar config under a custom/wallpaper module which on-click changes between the generated sequence of wallpapers

# List of wallpapers (must also edit your .config/hypr/hyprpaper.conf to match with the preload command)
# this will likely be edited once I can work out how to preload all files in a certain directory or with a certain naming pattern so that you can generate different cluster numbers without editing code
wallpapers=(
    "/home/jude/Documents/python_stuff/collage_0.png"
    "/home/jude/Documents/python_stuff/collage_1.png"
    "/home/jude/Documents/python_stuff/collage_2.png"
    "/home/jude/Documents/python_stuff/collage_3.png"
    "/home/jude/Documents/python_stuff/collage_4.png"
    "/home/jude/Documents/python_stuff/collage_5.png"
)

# File to store current index
state_file="/tmp/current_wallpaper_index"

# runs through the sequence of wallpapers
# Read index (default 0)
if [[ -f "$state_file" ]]; then
    idx=$(<"$state_file")
else
    idx=0
fi

# Advance index
idx=$(( (idx + 1) % ${#wallpapers[@]} ))

# Save new index
echo "$idx" > "$state_file"

# final command to waybar
# Set wallpaper
hyprctl hyprpaper wallpaper ", ${wallpapers[$idx]}"
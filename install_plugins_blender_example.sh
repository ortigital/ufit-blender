#!/bin/bash

# Path to the Blender installation folder
BLENDER_PATH="/home/sover/Desktop/blender/blender-3.5.1-linux-x64"

# Path to the local addon folder
ADDON_SOURCE="ufit"  # Local path to the addon folder

# Path to the destination addon folder inside Blender
ADDON_DEST="$BLENDER_PATH/3.5/scripts/addons/ufit"

# Remove the existing addon folder and its contents if it exists
if [ -d "$ADDON_DEST" ]; then
    rm -rf "$ADDON_DEST"  # Recursively remove the addon folder
fi

# Create the addon folder again
mkdir -p "$ADDON_DEST"  # Create the folder, including parent directories if necessary

# Copy the contents of the local addon folder to the destination
cp -R "$ADDON_SOURCE"/. "$ADDON_DEST"  # Copy all files and subdirectories from the source to the destination

# Rename the __init_plugins__.py file to __init__.py if it exists
if [ -f "$ADDON_DEST/__init_plugins__.py" ]; then
    mv "$ADDON_DEST/__init_plugins__.py" "$ADDON_DEST/__init__.py"  # Rename the file
fi

# Terminate any running Blender processes
pkill -f blender  # Forcefully terminate Blender processes

# Start Blender
"$BLENDER_PATH/blender" &  # Launch Blender in the background

exit 0  # Exit the script with a success status
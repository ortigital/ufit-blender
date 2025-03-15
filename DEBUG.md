# Debug Setup Instructions

This guide explains how to set up debugging for the UFit Blender addon.

## Prerequisites

- Visual Studio Code
- Blender 3.5+
- Anaconda/Miniconda

## Installation Steps

### 1. Configure Environment

#### 1. Create `.env` file in project root with required variables:
```
BLENDER_EXECUTABLE_PATH=/home/username/Downloads/blender-3.5.1-linux-x64/blender
BLENDER_ADDONS_PATH=/home/username/.config/blender/3.5/scripts/addons
ANACONDA_PATH=/home/username/anaconda3/
CONDA_ENV_NAME=ufit
```

    cp .example.env .env

#### 2. Create `.vscode/launch.json` from template:
   - Copy `launch.example.json` to `launch.json`
   - Replace `<BLENDER_ADDONS_PATH>` with your actual Blender addons path

#### 3. Install Python dependencies:
```bash
conda activate your_env_name
pip install -r requirements.txt
```
Make sure `debugpy` is installed successfully - it's crucial for debugging.

### 2. Install Blender Debugger Addon

#### 1. Download the VSCode debugger addon for Blender:
   - Go to https://github.com/AlansCodeLog/blender-debugger-for-vscode
   - Click the green "Code" button
   - Select "Download ZIP"
#### 2. In Blender:
   - Go to Edit > Preferences > Add-ons
   - Click "Install"
   - Navigate to downloaded ZIP file and install it
   - Enable the addon by checking its checkbox

### 3. Launch Blender with Debug Environment

For Linux:
```bash
./install_plugin_launch_blender.sh
```

For Windows:
```batch
install_plugin_launch_blender.bat
```

This script will:
- Activate the conda environment
- Install the plugin in Blender addons directory
- Launch Blender with proper environment settings

### 4. Start Debugging

#### 1. In Blender:
   - Press F3
   - Search for "Debug"
   - Click "Debug: Start Debug Server for VS Code"

#### 2. In VS Code:
   - Set breakpoints in your code
   - Go to Run and Debug (Ctrl+Shift+D)
   - Select "Python Debugger: Remote Attach"
   - Click Start Debugging (F5)

You should now be able to debug your addon with breakpoints, variable inspection, and other debugging features.

## Troubleshooting

- If breakpoints are not hitting, check that paths in `launch.json` match your actual addon installation path
- In VS Code settings (Ctrl+,), verify:
    - Set `debug.allowBreakpointsEverywhere` to `true` to allow breakpoints in any file
    - Set `debug.showInlineBreakpointCandidates` to `true` to see where breakpoints can be placed
- Ensure Blender is running with `--python-use-system-env` flag (this is handled by the launch scripts)
- Verify the debugger server is running in Blender (check console output)
- Make sure all required environment variables are set correctly in `.env`
- Confirm that `debugpy` is installed in your conda environment
- In Blender, make sure `Preferences > Interface > Developer Extras` is enabled

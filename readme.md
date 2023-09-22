A tool for automatic fishing in Destiny 2.
Inspired by [D2SemiAutoFisher](https://github.com/Chadhendrixs/D2SemiAutoFisher).

# Features

- Predefined configurations for 1980x1080 screen resolutions,
  English and Russian localizations with `E` as interaction button.
- An opportunity to add configuration for your own resolution, localization and interaction key.
- Customizable fish limit to prevent fish left on the surface from disappearing.
- Anti-AFK system to prevent being kicked from the game during long fishing sessions.
  The system continues to run even if the player stops fishing or dies.

# Installation

## As an executable program

**Important**: This tool does not have any malware or spyware.
The executable is created via [PyInstaller](https://github.com/pyinstaller/pyinstaller);
it can add code and libraries for which I am not responsible.

[<b>VirusTotal score</b>](https://www.virustotal.com/gui/file/1dc8c0244d370a301eb0393858156fc704939a7c9f19ee9119384ef74c564d3d)

1. Open
   [the latest release](https://github.com/Prometheus3375/destiny2-auto-fishing/releases/latest).
2. Download `destiny2autofishing.zip` from Assets.
3. Unpack this archive to any empty directory.

## As a Python module

1. Install [Python 3.11.4](https://www.python.org/downloads/release/python-3114/)
   or higher version of Python 3.11.
2. Open PowerShell.
3. Run `pip install -U https://github.com/Prometheus3375/destiny2-auto-fishing/archive/latest.zip`
   to install the latest version of the script.

# Usage

## Running the tool

While the tool is running you can freely change keyboard layout,
but you are forced to use English (USA) before its start.

### As an executable program

1. Open directory where you have unpacked the archive, in Explorer.
2. Click on the address bar, erase everything there, type `powershell` and press Enter.
    - Alternatively, you can click `File -> Run Windows PowerShell -> Run Windows PowerShell`.
3. Switch your keyboard layout to English (USA).
4. Run `.\destiny2autofishing.exe 'path-to-configuration-file'` to start the script
   using configuration from a file located at `path-to-configuration-file`.
    - There are some predefined configurations located inside `config` directory.
    - For more information and parameters run `.\destiny2autofishing.exe --help`.

### As a Python module

1. Open PowerShell.
2. Switch your keyboard layout to English (USA).
3. Start the script:
    - Run `python -m destiny2autofishing -p 1920x1080-E-english` to start the script
      using predefined configuration for screen with resolution 1920x1080
      and Destiny 2 with `E` as interaction key and English localization.
        - Run `python -m destiny2autofishing --help` to view
          all available predefined configurations.
        - If you have not found your resolution/key/localization in the list of available,
          refer to section `Making custom configuration file` below.
    - Run `python -m destiny2autofishing -c 'path-to-configuration-file'` to start the script
      using configuration from a file located at `path-to-configuration-file`.

### Tips

#### PowerShell

- Use ⬆ and ⬇ keys to search for history of commands.
- If you have copied a command, you can paste it in single click of right mouse button.
- Press `Ctrl+C` to terminate any executing command.

#### Explorer

- Hold Shift and press right mouse button on a file/directory and select `Copy as path`
  to copy absolute path to this file/directory.

## Termination

The tool can be terminated by pressing `Enter` after it is fully started.

## Making custom configuration file

[//]: # (Specify full URL, so that views on other platforms will contain valid URL)

A usual case for creating a custom configuration file is the absense of predefined configuration
for your screen resolution, interaction key or localization.
Complete guidelines for creating a custom configuration file are written
[here](https://github.com/Prometheus3375/destiny2-auto-fishing/blob/main/resources/config-guide.md).

## Anti-AFK system

This system performs anti-AFK actions almost every 2 minutes,
each time after casting the fishing rod. A cast has long animation;
therefore, anti-AFK actions do not interrupt fish catching and other actions made by the script.

If for some reason the fishing rod was not cast by the script for 2.5 minutes,
then the system starts to perform anti-AFK actions every 2 minutes, without
waiting for rod casts, until the script makes a cast or the script is terminated.

**Note**: the script cannot resume fishing, this must be done manually.
Anti-AFK cannot track whether fishing is manually resumed, and after manual resuming
it will continue to consider that the rod was cast a long time ago
performing anti-AFK action according to the schedule.
Restart the script to prevent fish catch failure due to the system.

The current anti-AFK actions are the following:

1. Press `F1`.
2. Wait 1 second.
3. Press `D`.
4. Wait 1 second.
5. Press `F1`.

To check if these actions indeed prevent kicking to orbit,
I made a small script to perform these actions every minute,
loaded into EDZ and left the script and the game running while I was sleeping.
After I woke up, my character was still in EDZ.
Later, I got the same results with the whole fishing script on Nessus with the period in 2 minutes.

# Development

## Project initialization

1. Install [Python 3.11.4](https://www.python.org/downloads/release/python-3114/)
   or higher version of Python 3.11.
2. Clone this project.
3. Open terminal and change current working directory to the root of this repository.
4. Initialize virtual environment inside `.venv` directory and activate it according to the
   [tutorial](https://docs.python.org/3/library/venv.html).
5. Run `python -m pip install -U pip setuptools wheel build pyinstaller==5.13.0`
   to install building tools.
6. Run `python -m pip install -r requirements.txt` to install dependencies.

## Releasing new version

1. Increase version in `destiny2autofishing/__init__.py`
   according to the [specification](https://peps.python.org/pep-0440/) and commit changes.
2. List all changes made in `changelog.md` and commit changes.
3. Run `build.ps1` file.
4. Create new release attaching `.whl` and `.zip` files created inside `.dist` directory.

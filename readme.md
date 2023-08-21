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

1. Install [Python 3.11.4](https://www.python.org/downloads/release/python-3114/)
   or higher version of Python 3.11.
2. Open PowerShell.
3. Run `pip install -U https://github.com/Prometheus3375/destiny2-auto-fishing/archive/latest.zip`
   to install the latest version of the script.

# Usage

## Running the tool

1. Open PowerShell.
2. Switch your keyboard layout to English (USA).
3. Start the script:
    - Run `python -m destiny2autofishing -p 1920x1080-E-english` to start the script
      using predefined configuration for screen with resolution 1920x1080
      and Destiny 2 with `E` as interaction key and English localization.
      - Run `python -m destiny2autofishing --help` to view available predefined configurations.
    - Run `python -m destiny2autofishing -c 'path-to-configuration-file'` to start the script
      using configuration from a file located at `path-to-configuration-file`.

The script can be terminated by pressing Enter after it is fully started.
While script is running you can freely change keyboard layout,
but you are forced to use English (USA) before its start.

For more information and parameters run `python -m destiny2autofishing --help`.
This command can be run without installed dependencies.

Tips for PowerShell:

- Use ⬆ and ⬇ keys to search for history of commands.
- If you have copied a command, you can paste it in single click of right mouse button.
- Press `Ctrl+C` to terminate an executing command.

## Making custom configuration file

[//]: # (Specify full URL, so that views on other platforms will contain valid URL)
Refer to
[config-guide.md](https://github.com/Prometheus3375/destiny2-auto-fishing/blob/main/resources/config-guide.md)
for guidelines.

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
4. Initialize virtual environment and activate it according to the
   [tutorial](https://docs.python.org/3/library/venv.html).
5. Run `python -m pip install -U pip setuptools wheel build` to install building tools.
6. Run `python -m pip install -r requirements.txt` to install dependencies.

## Releasing new version

1. Increase version according to [specification](https://peps.python.org/pep-0440/)
   in `destiny2autofishing/__init__.py` and commit changes.
2. List all changes made in `changelog.md` and commit changes.
3. Run `python -m build`.
4. Delete tag `latest` on remote.
5. Add tag with new version and tag `latest` on the very last commit.
6. Push to remote.
7. Create new release attaching `.whl` file created inside directory `dist`.

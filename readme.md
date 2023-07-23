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
2. [Download](https://github.com/Prometheus3375/destiny2-auto-fishing/archive/refs/heads/main.zip)
   ZIP archive of the project.
3. Extract this archive to any empty directory.
4. Open this directory in Explorer, type `powershell` in address line and press Enter.
5. (Optional) Initialize and activate virtual environment.
    - Run `python -m venv .venv` to initialize.
    - Run `.\.venv\Scripts\Activate.ps1` to activate.
6. Run `python -m pip install -U pip setuptools wheel` to update building tools.
7. Run `python -m pip install -r requirements.txt` to install dependencies.

# Usage

## Running the tool

1. Open project directory in Explorer, type `powershell` in address line and press Enter.
2. If there is a virtual environment (installation step 5), activate it.
3. Switch your keyboard layout to English (USA).
4. Run `python -m destiny2autofishing 1920 1080 english E` to start the script
   for screen with resolution 1920x1080 and Destiny 2
   with English localization and `E` as interaction key.

The script can be terminated by pressing Enter after it is fully started.
While script is running you can freely change keyboard layout,
but you are forced to use English (USA) before its start.

For more information and parameters run `python -m destiny2autofishing --help`.
This command can be run without installed dependencies.

Some tips in working with PowerShell:

- Use ⬆ and ⬇ keys to search for history of commands.
- If you have copied a command, you can paste it in single click of right mouse button.
- Press `Ctrl+C` to terminate an executing command.

## Adding unsupported resolutions, localizations and keys

**Note**: it is possible to add mouse buttons, but directly supported buttons are
`left`, `middle` and `right`. For other buttons there is a workaround described
in the section below.

1. Start fishing manually and make a screenshot when `Perfect catch` interaction is clearly visible.
2. Crop the screenshot to capture key image.
3. Add your localization if it is not present.
    - Recall starting X and Y that were used for bounding box during cropping.
    - Open `predefined/image/localizations.py` in Notepad or any other text editor.
    - Add this code with corresponded values placed. Angle braces (`<>`) must be omitted.
      ```
      <localization>_<screen width>x<screen height> = Localization(bbox_x0=<X>, bbox_y0=<Y>)
      ```
      Usually localizations share `bbox_y0` withing the same screen resolution.
4. Record a video where you catch a fish. There should be at least 2 seconds before catch and
   2 seconds after.
5. Extract several frames when `Perfect catch` interaction is clearly visible as well as some
   frames before and after.
6. Crop extracted frames at the same place as in the screenshot.
   I suggest to use [XnView MP](https://www.xnview.com/en/xnviewmp/) for this.
7. Add your key if it is not present.
    - Run `python -m destiny2autofishing.methods.image "path/to/cropped/screenshot" -d "path/to/directory/with/other/images"`
      where the first path is the path to the cropped screenshot and
      the second one is the path to the directory with all key images you created at step 6.
        - Run `python -m destiny2autofishing.methods.image --help` to view available options.
    - You will see several `tolerance` values in the output. Pick the most appropriate one.
      A value of 85 is usually sufficient.
    - Open `predefined/image/keys.py` in Notepad or any other text editor.
    - Add this code with corresponded values placed. Angle braces (`<>`) must be omitted.
      ```
      <key name>_<screen width>x<screen height> = Key('<key name in lower case>', '<path to clearest key image>', tolerance=<tolerance>)
      ```
      If the key is a mouse button, use this code.
      ```
      <key name>_<screen width>x<screen height> = Key('<key name in lower case>', '<path to clearest key image>', tolerance=<tolerance>, is_mouse_button=True)
      ```
8. Run `python -m destiny2autofishing --help`. If you see your localization and key
   in the list of supported, then you have done everything correctly.

If you find difficult to add your own resolution, localization or key, then create an issue in
[issue tracker](https://github.com/Prometheus3375/destiny2-auto-fishing/issues)
with attached screenshot and video from steps 1 and 4.

### Workaround for unsupported mouse buttons

- Complete all steps from the guide above.
- In Destiny 2 settings set an *alternative button* for interaction command
  to any keyboard letter.
- Open `predefined/image/keys.py` in Notepad or any other text editor and
  locate previously added mouse button.
- Edit its code to the following. Angle braces (`<>`) must be omitted.
  ```
  <mouse button name>_<keyboard letter>_<screen width>x<screen height> = Key('<keyboard letter in lower case>', '<path to clearest mouse button image>', tolerance=<tolerance>)
  ```

Since mouse button is the primary way to interact,
the game shows its image when interaction is available.
Thus, its image must be used by the script. But this button cannot be pressed by the script
because of library limitations; therefore, you need to set an alternative key in
game settings and specify this key instead of mouse button.

## Anti-AFK system

This system performs anti-AFK actions almost every 2 minutes,
each time after casting the fishing rod.
Casting the rod has long animation;
therefore, anti-AFK actions do not interrupt fish catching or anything else.

If for some reason the fishing rod was not cast for 1 minute
then the system starts to perform anti-AFK actions every 2 minutes
without additional conditions until fishing is resumed or the script is terminated.

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
5. Press `ESC`.

To check if these actions indeed prevent kicking to orbit,
I made a small script to perform these actions every minute,
loaded into EDZ and left the script and the game running while I was sleeping.
After I woke up, my character was still in EDZ.

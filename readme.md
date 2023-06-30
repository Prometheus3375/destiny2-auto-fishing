Inspired by [D2SemiAutoFisher](https://github.com/Chadhendrixs/D2SemiAutoFisher).

# Installation

1. Install [Python 3.11.4](https://www.python.org/downloads/release/python-3114/)
   or higher version of Python 3.11.
2. [Download](https://github.com/Prometheus3375/destiny2-auto-fishing/archive/refs/heads/main.zip)
   ZIP archive of the project.
3. Extract this zip in any empty directory.
4. Open this directory in Explorer, type `powershell` in address line and press Enter.
5. (Optional) Initialize and activate virtual environment.
    - Run `python -m venv .venv` to initialize.
    - Run `.\.venv\Scripts\Activate.ps1` to activate.
6. Run `python -m pip install -U pip setuptools wheel` to update building tools.
7. Run `python -m pip install -r requirements.txt` to install dependencies.

# Usage

## Running a script

1. Open project directory in Explorer, type `powershell` in address line and press Enter.
2. If there is a virtual environment (installation step 5), activate it.
3. Run `python main.py 1920 1080 english E` to start the script
   for screen with resolution 1920x1080 and Destiny 2
   with English localization and `E` as interaction key.

For more information and parameters run `python main.py --help`.
This command can be run without installed dependencies.

## Adding unsupported resolutions, localizations and keys

**Note**: mouse buttons cannot be added currently, but this can be changed via request in
[issue tracker](https://github.com/Prometheus3375/destiny2-auto-fishing/issues).
PyAutoGUI supports limited amount of mouse buttons.

1. Record a video where you catch a fish. There should be at least 2 seconds before catch and
   2 seconds after.
2. Extract several frames when `Perfect catch` interaction is clearly visible as well as some
   frames before and after.
3. Crop these frames at the same place to capture key image and save separately.
   I suggest to use [XnView MP](https://www.xnview.com/en/xnviewmp/) for this.
4. Add your localization if it is not present.
    1. Recall starting X and Y that were used for bounding box during cropping.
    2. Open `predefined/image/localizations.py` in Notepad or any other text editor.
    3. Add this code with corresponded values placed. Angle braces (`<>`) must be omitted.
       ```
       <localization>_<screen width>x<screen height> = Localization(bbox_x0=<X>, bbox_y0=<Y>)
       ```
       Usually localizations share `bbox_y0` withing the same screen resolution.
5. Add your key if it is not present.
    1. Run `python -m methods.image "path\to\image"` where `"path\to\image"`
       is path to the clearest key image.
    2. You will see `x_averages` and `y_averages` in the output.
    3. Run `python -m methods.image "path\to\image" "path\to\other\image"`
       where the first path is from step 5.1
       and the second one is for any other key image made at step 3.
    4. Each run will produce suggested tolerance value. Pick the highest one.
       A value of 50 is usually sufficient.
    5. Open `predefined/image/keys.py` in Notepad or any other text editor.
    6. Add this code with corresponded values placed. Angle braces (`<>`) must be omitted.
       ```
       <key name>_<screen width>x<screen height> = Key(
           '<key name in lower case>',
           x_averages=<x_averages>,
           y_averages=<y_averages>,
           tolerance=<tolerance>,
           )
       ```
6. Run `python main.py --help`. If you see your localization and key in the list of supported,
   then you have done everything correctly.

This guide is outdated, a new one will be written soon.

# Creating configuration file

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

## Workaround for unsupported mouse buttons

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

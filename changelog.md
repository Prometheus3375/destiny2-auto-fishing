# Changelog

## 1.1.1

### Changes

- Now **all** path parameters must have either an absolute path
  or a path relative to the directory where a configuration file is stored.
  - Previously, this was true only for parameter `key_image_path` in section `fishing-method.image`.
  - Generated configuration files now specify this rule in the header.
- Descriptions of path parameters for debug directories
  now include that if passed paths do not exist they are created automatically.

## 1.1.0

### Features

- Added executable edition.

### Bug fixes

- Now log files from fishing methods have `.txt` extension.
- Fixed uncaught `EOFError` in `fisher.py`.

### Development

- Various improvements to documentation and typing.
- Updated import statements.
- Updated build configuration and tools.

## 1.0.0

Initial release.

### Features

- Working fishing loop.
- Anti-AFK system.
- Predefined configurations for 1920x1080 screen resolutions.

<<<<<<< HEAD
# Keylogger Project

> **Important:** This project records keyboard and mouse activity. Do not run or distribute it without explicit permission from the device owner. Unauthorized use may be illegal and unethical.

## Overview

`logger.py` is a Windows-targeted input logger that captures keyboard presses and mouse clicks. It stores log entries in a text file under the current Windows user's Local AppData folder by default.

The project also includes a PyInstaller spec file (`logger.spec`) for building a standalone executable.

## Requirements

- Windows OS
- Python 3.8+ installed
- `pynput` library
- `tkinter` available (usually included with Python on Windows)
- `pyinstaller` if you want to build an `.exe`

## Install dependencies

Open PowerShell in this folder and run:

```powershell
python -m pip install --upgrade pip
python -m pip install pynput pyinstaller
```

If `tkinter` is missing, install a Python distribution that includes it.

## Run from source

To run directly from Python:

```powershell
python logger.py
```

### What happens when you run it

- The script hides its window and begins listening for keyboard and mouse events.
- It buffers log data in memory and writes to disk every 30 seconds.
- The default log file is created in `%LOCALAPPDATA%` with a name like `log_2026-07-16_12-34-56.txt`.

## Build a standalone executable

Use PyInstaller and the existing spec file:

```powershell
pyinstaller logger.spec
```

After building, the executable will be placed under the `dist\logger` folder.

### Run the built executable

From PowerShell:

```powershell
cd dist\logger
logger.exe
```

## Log file path

By default, the logger writes to `%LOCALAPPDATA%\log_<timestamp>.txt`.

If the GUI is visible and you use the `Browse Folder` button, you can choose a custom output location.

## Windows startup behavior

When the project is built into an executable, `logger.exe` attempts to copy itself to the current user Startup folder as `WinHostServices.exe`.

This behavior is only active when the code is running as a frozen executable.

## Notes

- This logger is designed for use on a machine you own or manage.
- Do not use this on other people’s systems without express consent.
- If you want to stop logging, close the process or kill the `logger.py`/`logger.exe` instance.

## Troubleshooting

- If `python` is not recognized, install Python and add it to your PATH.
- If `pynput` fails to import, verify the package is installed in the same Python environment used to run the script.
- If the executable does not start, check `dist\logger\logger.exe` and run it from a command prompt for error output.
=======
# Key-Logger
I have developed a key logger that save the record of everykey you have presses on keyboard even passwords, each and everything.
>>>>>>> 3aaf650d20c1627c09813a41bb8eebb82b19cbbd

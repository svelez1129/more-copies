# DualCopy

A lightweight, zero-configuration secondary clipboard utility for Windows.

DualCopy runs silently in the background, giving you an extra clipboard slot without modifying native shortcuts, requiring administrator rights, or altering the Windows registry.

---

## Features

- **Dual Clipboard Slots:** Standard `Ctrl+C` / `Ctrl+V` remain untouched; secondary slot runs on `Ctrl+Shift+C` / `Ctrl+Shift+V`.
- **Minimal Footprint:** Headless execution consuming under 2 MB RAM with no system tray icon or taskbar window.
- **Zero-Setup Startup:** Double-click to start. Automatically configures auto-launch on system startup.
- **Clean Self-Uninstall:** Double-clicking the app while running opens a native prompt to completely remove startup scripts, terminate execution, and delete the file.

---

## Keybindings

| Command | Shortcut | Description |
| :--- | :--- | :--- |
| **Slot 1 Copy** | `Ctrl` + `C` | Native Windows copy |
| **Slot 1 Paste** | `Ctrl` + `V` | Native Windows paste |
| **Slot 2 Copy** | `Ctrl` + `Shift` + `C` | Copy text to secondary clipboard slot |
| **Slot 2 Paste** | `Ctrl` + `Shift` + `V` | Paste text from secondary clipboard slot |
| **Pause / Resume** | `Ctrl` + `Alt` + `P` | Toggle secondary shortcuts on/off |

---

## Installation & Setup

1. Download **`DualCopy.exe`** from [Releases](../../releases) (or from the latest GitHub Action artifact).
2. Move `DualCopy.exe` to any folder on your machine.
3. Double-click `DualCopy.exe` to launch.

DualCopy will immediately run in the background and configure automatic boot on system startup.

---

## Uninstallation

1. Double-click `DualCopy.exe` while it is already running.
2. Click **Yes** on the confirmation prompt.

DualCopy will remove its startup launcher, terminate its background process, and delete its executable from your system.

---

## License

MIT

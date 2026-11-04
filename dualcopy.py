import ctypes
import os
import subprocess
import sys
import time
from pathlib import Path

import keyboard
import pyperclip

MUTEX_NAME = "Global\\DualCopy_SingleInstance_Mutex"


class DualCopyState:
    """Manages internal state for the secondary clipboard and pause toggle."""

    def __init__(self):
        self.secondary_clipboard: str = ""
        self.is_paused: bool = False

    def toggle_pause(self) -> bool:
        self.is_paused = not self.is_paused
        return self.is_paused

    def set_secondary(self, text: str) -> None:
        self.secondary_clipboard = text

    def get_secondary(self) -> str:
        return self.secondary_clipboard


def get_startup_path() -> Path:
    """Resolves the Windows Startup folder path for the current user."""
    appdata = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
        / "DualCopy.bat"
    )


def is_already_running() -> tuple[bool, object]:
    """Uses a Win32 Mutex to verify if another DualCopy instance is active."""
    if not hasattr(ctypes, "windll"):
        return False, None

    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    ERROR_ALREADY_EXISTS = 183
    return (kernel32.GetLastError() == ERROR_ALREADY_EXISTS), mutex


def ensure_startup_entry() -> None:
    """Creates a background launcher script in the Windows Startup folder if absent."""
    startup_file = get_startup_path()
    if not startup_file.exists():
        target = Path(sys.argv[0]).resolve()
        if target.suffix == ".py":
            cmd = f'@echo off\nstart "" pythonw "{target}"\n'
        else:
            cmd = f'@echo off\nstart "" "{target}"\n'
        startup_file.write_text(cmd)


def uninstall_self() -> None:
    """Removes startup hooks, schedules self-deletion, and exits process."""
    startup_file = get_startup_path()
    if startup_file.exists():
        try:
            startup_file.unlink()
        except OSError:
            pass

    current_file = Path(sys.argv[0]).resolve()
    del_cmd = f'timeout /t 1 /nobreak > NUL & del /f /q "{current_file}"'
    subprocess.Popen(
        f'cmd.exe /c "{del_cmd}"',
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    sys.exit(0)


def prompt_uninstall() -> None:
    """Triggers native Win32 dialog when user launches a duplicate instance."""
    MB_YESNO = 0x00000004
    IDYES = 6
    response = ctypes.windll.user32.MessageBoxW(
        0,
        "DualCopy is currently running.\n\nWould you like to uninstall it?",
        "DualCopy",
        MB_YESNO,
    )
    if response == IDYES:
        uninstall_self()


class DualCopyApp:
    def __init__(self):
        self.state = DualCopyState()

    def copy_secondary(self) -> None:
        if self.state.is_paused:
            return
        keyboard.send("ctrl+c")
        time.sleep(0.05)
        self.state.set_secondary(pyperclip.paste())

    def paste_secondary(self) -> None:
        if self.state.is_paused:
            return
        content = self.state.get_secondary()
        if not content:
            return
        primary_backup = pyperclip.paste()
        pyperclip.copy(content)
        keyboard.send("ctrl+v")
        time.sleep(0.05)
        pyperclip.copy(primary_backup)

    def toggle_pause(self) -> None:
        self.state.toggle_pause()

    def run(self) -> None:
        ensure_startup_entry()
        keyboard.add_hotkey("ctrl+shift+c", self.copy_secondary, suppress=False)
        keyboard.add_hotkey("ctrl+shift+v", self.paste_secondary, suppress=False)
        keyboard.add_hotkey("ctrl+alt+p", self.toggle_pause, suppress=False)
        keyboard.wait()


if __name__ == "__main__":
    already_running, _ = is_already_running()
    if already_running:
        prompt_uninstall()
        sys.exit(0)

    app = DualCopyApp()
    app.run()
import os
import sys
from pathlib import Path
from dualcopy import DualCopyState, get_startup_path, is_already_running, DualCopyApp
from unittest.mock import MagicMock, patch


def test_initial_state():
    state = DualCopyState()
    assert state.secondary_clipboard == ""
    assert not state.is_paused


def test_toggle_pause():
    state = DualCopyState()
    assert state.toggle_pause() is True
    assert state.is_paused is True
    assert state.toggle_pause() is False
    assert state.is_paused is False


def test_secondary_clipboard_storage():
    state = DualCopyState()
    state.set_secondary("test snippet")
    assert state.get_secondary() == "test snippet"


def test_startup_path_resolution():
    path = get_startup_path()
    assert isinstance(path, Path)
    assert "Startup" in str(path)
    assert path.name == "DualCopy.bat"


def test_single_instance_mutex():
    running_1, mutex_1 = is_already_running()
    running_2, mutex_2 = is_already_running()

    if sys.platform == "win32":
        assert running_2 is True
    else:
        assert running_1 is False
        assert running_2 is False


def test_copy_secondary_active_and_paused():
    app = DualCopyApp()

    with patch("keyboard.send") as mock_send, patch(
        "pyperclip.paste", return_value="copied_text"
    ):
        # 1. Active copy should capture text into slot 2
        app.copy_secondary()
        mock_send.assert_called_once_with("ctrl+c")
        assert app.state.get_secondary() == "copied_text"

        # 2. Paused copy should be ignored completely
        mock_send.reset_mock()
        app.toggle_pause()
        app.copy_secondary()
        mock_send.assert_not_called()


def test_paste_secondary_logic():
    app = DualCopyApp()
    app.state.set_secondary("secondary_text")

    with patch("keyboard.send") as mock_send, patch(
        "pyperclip.paste", return_value="original_clipboard"
    ), patch("pyperclip.copy") as mock_copy:

        # Pasting should swap secondary in, trigger Ctrl+V, then restore original clipboard
        app.paste_secondary()

        mock_copy.assert_any_call("secondary_text")
        mock_send.assert_called_once_with("ctrl+v")
        mock_copy.assert_any_call("original_clipboard")
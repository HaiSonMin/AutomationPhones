"""
Input Handler for remote mouse and keyboard control.

Handles mouse and keyboard events received from viewers
and translates them to local system inputs.
"""

import logging
from typing import Optional, Tuple, Set

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

logger = logging.getLogger(__name__)


# Key mapping from web key names to pynput keys
KEY_MAP = {
    "Enter": Key.enter,
    "Escape": Key.esc,
    "Backspace": Key.backspace,
    "Tab": Key.tab,
    "Space": Key.space,
    "ArrowUp": Key.up,
    "ArrowDown": Key.down,
    "ArrowLeft": Key.left,
    "ArrowRight": Key.right,
    "Home": Key.home,
    "End": Key.end,
    "PageUp": Key.page_up,
    "PageDown": Key.page_down,
    "Insert": Key.insert,
    "Delete": Key.delete,
    "F1": Key.f1,
    "F2": Key.f2,
    "F3": Key.f3,
    "F4": Key.f4,
    "F5": Key.f5,
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "F11": Key.f11,
    "F12": Key.f12,
    "Control": Key.ctrl,
    "Shift": Key.shift,
    "Alt": Key.alt,
    "Meta": Key.cmd,
    "CapsLock": Key.caps_lock,
    "NumLock": Key.num_lock,
    "ScrollLock": Key.scroll_lock,
    "PrintScreen": Key.print_screen,
    "Pause": Key.pause,
}

# Mouse button mapping
MOUSE_BUTTON_MAP = {
    0: Button.left,
    1: Button.middle,
    2: Button.right,
}


class InputHandler:
    """
    Handles remote input events.

    Translates mouse and keyboard events from the web client
    into local system actions using pynput.
    """

    def __init__(
        self,
        screen_size: Tuple[int, int],
        stream_size: Optional[Tuple[int, int]] = None,
        enabled: bool = True,
    ):
        """
        Initialize input handler.

        Args:
            screen_size: Actual screen resolution (width, height)
            stream_size: Stream resolution for coordinate scaling
            enabled: Whether input handling is enabled
        """
        self._screen_width, self._screen_height = screen_size
        self._stream_width = stream_size[0] if stream_size else screen_size[0]
        self._stream_height = stream_size[1] if stream_size else screen_size[1]
        self._enabled = enabled

        self._mouse = MouseController()
        self._keyboard = KeyboardController()
        self._pressed_keys: Set[str] = set()

        logger.info(
            f"Input handler initialized: screen={screen_size}, "
            f"stream={stream_size}, enabled={enabled}"
        )

    def set_stream_size(self, width: int, height: int) -> None:
        """Update stream size for coordinate scaling."""
        self._stream_width = width
        self._stream_height = height

    def _scale_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        """
        Scale coordinates from stream space to screen space.

        Args:
            x: X coordinate in stream space (0-1 or pixel)
            y: Y coordinate in stream space (0-1 or pixel)

        Returns:
            Scaled (x, y) in screen pixels
        """
        # If coordinates are normalized (0-1 range)
        if 0 <= x <= 1 and 0 <= y <= 1:
            scaled_x = int(x * self._screen_width)
            scaled_y = int(y * self._screen_height)
        else:
            # Scale from stream resolution to screen resolution
            scale_x = self._screen_width / self._stream_width
            scale_y = self._screen_height / self._stream_height
            scaled_x = int(x * scale_x)
            scaled_y = int(y * scale_y)

        return (scaled_x, scaled_y)

    def handle_mouse_event(
        self,
        event_type: str,
        x: float,
        y: float,
        button: int = 0,
        delta_x: float = 0,
        delta_y: float = 0,
    ) -> None:
        """
        Handle a mouse event.

        Args:
            event_type: Event type (mousemove, mousedown, mouseup, click, wheel)
            x: X coordinate
            y: Y coordinate
            button: Mouse button (0=left, 1=middle, 2=right)
            delta_x: Scroll delta X (for wheel events)
            delta_y: Scroll delta Y (for wheel events)
        """
        if not self._enabled:
            return

        try:
            scaled_x, scaled_y = self._scale_coordinates(x, y)
            mouse_button = MOUSE_BUTTON_MAP.get(button, Button.left)

            if event_type == "mousemove":
                self._mouse.position = (scaled_x, scaled_y)

            elif event_type == "mousedown":
                self._mouse.position = (scaled_x, scaled_y)
                self._mouse.press(mouse_button)

            elif event_type == "mouseup":
                self._mouse.position = (scaled_x, scaled_y)
                self._mouse.release(mouse_button)

            elif event_type == "click":
                self._mouse.position = (scaled_x, scaled_y)
                self._mouse.click(mouse_button)

            elif event_type == "dblclick":
                self._mouse.position = (scaled_x, scaled_y)
                self._mouse.click(mouse_button, 2)

            elif event_type == "wheel":
                self._mouse.position = (scaled_x, scaled_y)
                # Scroll direction: negative = up, positive = down
                scroll_x = int(delta_x) if delta_x else 0
                scroll_y = int(-delta_y / 100) if delta_y else 0
                self._mouse.scroll(scroll_x, scroll_y)

            elif event_type == "contextmenu":
                self._mouse.position = (scaled_x, scaled_y)
                self._mouse.click(Button.right)

        except Exception as e:
            logger.error(f"Error handling mouse event: {e}")

    def handle_keyboard_event(
        self,
        event_type: str,
        key: str,
        code: str,
        modifiers: Optional[list] = None,
    ) -> None:
        """
        Handle a keyboard event.

        Args:
            event_type: Event type (keydown, keyup)
            key: Key value (e.g., 'a', 'Enter')
            code: Key code (e.g., 'KeyA', 'Enter')
            modifiers: List of modifier keys (ctrl, shift, alt, meta)
        """
        if not self._enabled:
            return

        try:
            # Map special keys
            if key in KEY_MAP:
                pynput_key = KEY_MAP[key]
            elif len(key) == 1:
                pynput_key = key
            else:
                # Try to parse from code
                if code.startswith("Key"):
                    pynput_key = code[3:].lower()
                elif code.startswith("Digit"):
                    pynput_key = code[5:]
                else:
                    logger.warning(f"Unknown key: {key} (code: {code})")
                    return

            if event_type == "keydown":
                self._keyboard.press(pynput_key)
                self._pressed_keys.add(key)

            elif event_type == "keyup":
                self._keyboard.release(pynput_key)
                self._pressed_keys.discard(key)

        except Exception as e:
            logger.error(f"Error handling keyboard event: {e}")

    def release_all_keys(self) -> None:
        """Release all currently pressed keys."""
        for key in list(self._pressed_keys):
            try:
                if key in KEY_MAP:
                    self._keyboard.release(KEY_MAP[key])
                elif len(key) == 1:
                    self._keyboard.release(key)
            except Exception:
                pass
        self._pressed_keys.clear()

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable input handling."""
        self._enabled = enabled
        if not enabled:
            self.release_all_keys()
        logger.info(f"Input handling {'enabled' if enabled else 'disabled'}")

    @property
    def enabled(self) -> bool:
        """Check if input handling is enabled."""
        return self._enabled

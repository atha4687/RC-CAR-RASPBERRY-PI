import sys
import termios
import tty
import select


def setup_keyboard():
    """Put terminal into cbreak mode for single-key reading."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return fd, old_settings


def restore_keyboard(fd, old_settings):
    """Restore normal terminal settings."""
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_key(timeout=0.05):
    """
    Non-blocking single key read.
    Returns key (str) if pressed, else None.
    """
    dr, _, _ = select.select([sys.stdin], [], [], timeout)
    if dr:
        return sys.stdin.read(1)
    return None


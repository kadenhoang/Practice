"""
Human-intuitive CLI UI helpers: clear sections, friendly messages, consistent prompts.
Uses ANSI colors when the terminal supports them (Windows 10+ and most terminals).
"""
import sys

# Enable ANSI colors on Windows when colorama is available
try:
    import colorama
    colorama.init()
except ImportError:
    pass

# ANSI codes (empty string if not supported)
try:
    _SUPPORT_COLOR = sys.stdout.isatty()
except Exception:
    _SUPPORT_COLOR = False

RESET = "\033[0m" if _SUPPORT_COLOR else ""
BOLD = "\033[1m" if _SUPPORT_COLOR else ""
DIM = "\033[2m" if _SUPPORT_COLOR else ""
GREEN = "\033[32m" if _SUPPORT_COLOR else ""
RED = "\033[31m" if _SUPPORT_COLOR else ""
YELLOW = "\033[33m" if _SUPPORT_COLOR else ""
CYAN = "\033[36m" if _SUPPORT_COLOR else ""

LINE_CHAR = "─"
LINE_WIDTH = 50


def _line(char=LINE_CHAR, width=LINE_WIDTH):
    return char * width


def clear_section():
    """Print blank lines to separate sections."""
    print()


def title(text, width=LINE_WIDTH):
    """Print a clear section title with lines above and below."""
    clear_section()
    line = _line(width=width)
    # Center the text in the line
    padding = max(0, width - len(text) - 2)
    left = padding // 2
    right = padding - left
    middle = f" {text} " if text else ""
    print(line)
    print(middle.center(width) if not middle.strip() else LINE_CHAR * left + middle + LINE_CHAR * right)
    print(line)
    print()


def section(text):
    """Shorter section header (e.g. for sub-steps)."""
    print()
    print(f"  {text}")
    print(f"  {_line(width=min(LINE_WIDTH, len(text) + 4))}")
    print()


def success(msg):
    """Print a success message."""
    print(f"  {GREEN}✓{RESET} {msg}")
    print()


def error(msg):
    """Print an error message."""
    print(f"  {RED}✗{RESET} {msg}")
    print()


def info(msg):
    """Print an info/hint message (dimmed)."""
    print(f"  {DIM}{msg}{RESET}")
    print()


def prompt(text, hint=None):
    """Return user input with a consistent prompt style. Optional hint shown below."""
    if hint:
        info(hint)
    return input(f"  {CYAN}→{RESET} {text}").strip()


def prompt_password(text):
    """Password prompt (no echo on input - we still use input() for simplicity)."""
    import getpass
    try:
        return getpass.getpass(f"  {CYAN}→{RESET} {text}")
    except Exception:
        return input(f"  {CYAN}→{RESET} {text}")


def menu(options, title_text="Choose an option", hint=None):
    """
    Display a numbered menu and return the user's choice (string).
    options: list of strings, e.g. ["Add Teacher", "Add Student", ...]
    """
    print()
    for i, opt in enumerate(options, 1):
        print(f"  {BOLD}{i}.{RESET} {opt}")
    print()
    if hint:
        info(hint)
    return prompt(f"{title_text} (1–{len(options)}): ")


def wait_to_continue(msg="Press Enter to return to the menu."):
    """Pause so the user can read the result before continuing."""
    input(f"  {DIM}{msg}{RESET}")


def card_title(text):
    """Print a small card-style title (for displaying one record)."""
    print()
    print(f"  {BOLD}{text}{RESET}")
    print(f"  {LINE_CHAR * (len(text) + 4)}")


def card_line(label, value):
    """Print one line of a card (label: value)."""
    print(f"    {label}: {value}")


def welcome_banner(app_name="Student & Teacher Info"):
    """Print a welcome banner at app start."""
    clear_section()
    width = max(LINE_WIDTH, len(app_name) + 6)
    print(_line("═", width))
    print()
    print(f"  {BOLD}{app_name}{RESET}".center(width + 4))
    print()
    print(_line("═", width))
    print()
    info("Please sign in or create an account to continue.")


def goodbye_banner():
    """Print a friendly goodbye."""
    clear_section()
    print(f"  {GREEN}Thanks for using the app. See you next time!{RESET}")
    print()

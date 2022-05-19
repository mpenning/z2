from __future__ import annotations
import termios
import fcntl
import sys

from loguru import logger

# Source:
#     https://stackoverflow.com/a/287944/667301
@logger.catch(default=True, onerror=lambda _: sys.exit(1))
class Color(object):
    """
    Select Graphic Rendition (SGR) color codes...
    https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
    """

    # Sources
    #   -> https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    #   -> https://xdevs.com/guide/color_serial/
    #   -> https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    #   -> https://wiki.bash-hackers.org/scripting/terminalcodes
    FG_BLACK = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_YELLOW = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"
    # ORANGE & PURPLE below uses 256-color (8-bit) codes
    #
    #     RGB ORANGE: 255, 165, 0
    FG_ORANGE = "\033[38;2;255;165;0m"
    #                 ^^ (38 is Foreground, 48 is Background)
    #
    #     RGB PURPLE: 230, 230, 250
    FG_PURPLE = "\033[38;2;230;230;250m"
    #                 ^^ (38 is Foreground, 48 is Background)

    BG_BLACK = "\033[0;40m"
    BG_RED = "\033[0;41m"
    BG_GREEN = "\033[0;42m"
    BG_YELLOW = "\033[0;43m"
    BG_BLUE = "\033[0;44m"
    BG_MAGENTA = "\033[0;45m"
    BG_CYAN = "\033[0;46m"
    BG_WHITE = "\033[0;47m"
    BG_ORANGE = "\033[48;2;255;165;0m"
    BG_PURPLE = "\033[48;2;230;230;250m"

    BRIGHT_RED = "\u001b[31;1m"
    BRIGHT_GREEN = "\u001b[32;1m"
    BRIGHT_YELLOW = "\u001b[33;1m"
    BRIGHT_BLUE = "\u001b[34;1m"
    BRIGHT_MAGENTA = "\u001b[35;1m"
    BRIGHT_CYAN = "\u001b[36;1m"
    BRIGHT_WHITE = "\u001b[37;1m"
    BRIGHT_BLACK = "\u001b[30;1m"

    # Output format codes
    #
    # https://stackoverflow.com/a/53826230/667301
    #
    BOLD = "\033[1m"
    DIM = "\033[2m"
    STANDOUT = "\033[3m"
    UNDERLINE = "\033[4m"
    # FYI... PuTTY requires special config to display BLINK text codes...
    #     After many experiments, I can't make PuTTY reliably blink
    #     text using "\033[5m"
    BLINK_SLOW = "\033[5m"
    BLINK_FAST = "\033[6m"
    INVERSE = "\033[7m"

    # Situational color names...
    HEADER = "\033[95m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"

    # End the colors...
    ENDC = "\033[0m"

#     Ref -> https://stackoverflow.com/a/7259460/667301
def getchar(prompt_text="", allowed_chars=None):
    """
    Read a single character from the user

    Parameters
    ----------
    - `prompt_text` can be a message before reading user input
    - `allowed_chars` can be a `set({})` of allowed characters
    """
    assert isinstance(prompt_text, str)
    fd_stdin = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd_stdin)
    newattr = termios.tcgetattr(fd_stdin)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd_stdin, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd_stdin, fcntl.F_GETFL)
    fcntl.fcntl(fd_stdin, fcntl.F_SETFL, oldflags)

    # print("something", end="") end param ensures there's no automatic newline
    #     Ref -> https://stackoverflow.com/a/493399/667301
    # Sometimes you need flush() to make the print() render
    if isinstance(prompt_text, str) and (prompt_text != ""):
        print(prompt_text, end="")
        sys.stdout.flush()

    try:
        while True:
            try:
                single_char = sys.stdin.read(1)
                # Check whether the char is in `allowed_chars`...
                if isinstance(allowed_chars, set):
                    if (single_char in allowed_chars):
                        break

                # break, if allowed_chars is not a `set({})`...
                elif not isinstance(allowed_chars, set):
                    break
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd_stdin, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd_stdin, fcntl.F_SETFL, oldflags)

    if isinstance(prompt_text, str) and (prompt_text != ""):
        print("")   # Move the cursor back to the far-left of terminal...
        sys.stdout.flush()

    return single_char


C = Color()

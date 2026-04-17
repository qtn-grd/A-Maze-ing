import sys
import time
from colors import CYAN, RESET


def fake_loading_bar(duration: int = 3, label: str = "Loading") -> None:
    """
    Display a simulated loading bar in the terminal.

    This function renders a progress bar that fills over a specified
    duration, updating in place using standard output. It is purely
    cosmetic and does not reflect actual processing.

    Args:
        duration (int, optional): Total duration of the loading animation
            in seconds. Defaults to 3.
        label (str, optional): Text label displayed before the loading bar.
            Defaults to "Loading".

    Returns:
        None
    """

    size = 40
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        progress = elapsed / duration
        if progress > 1:
            progress = 1
        i = int(progress * size)
        percent = int(progress * 100)
        bar = "#" * i + "-" * (size - i)
        if percent > 99:
            break
        sys.stdout.write(f"\r{label} : [{CYAN}{bar}{RESET}] {percent}%")
        sys.stdout.flush()

        if progress >= 1:
            break
        time.sleep(0.05)

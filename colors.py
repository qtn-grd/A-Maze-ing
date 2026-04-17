RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
RESET = "\033[0m"
BLACK = "\033[30m"


def print_rainbow_text(text: str) -> str:
    """
    Apply a rainbow color effect to a given text string.

    Each character of the input text is assigned a color from a predefined
    sequence of ANSI color codes, cycling through the list to create a
    rainbow-like effect.

    Args:
        text (str): The input string to be colorized.

    Returns:
        str: The colorized string with ANSI escape codes applied,
            ending with a reset code.
    """

    colors = [
        "\033[31m",
        "\033[33m",
        "\033[32m",
        "\033[36m",
        "\033[34m",
        "\033[35m",
    ]
    colored_text = ""

    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        colored_text += f"{color}{char}"

    return colored_text + RESET


def print_rainbow_art(art_string: str) -> str:
    """
    Apply a rainbow color effect to ASCII art text.

    Each character in the input string is assigned a color from a predefined
    palette, cycling through colors horizontally for each line.

    Args:
        art_string (str): Multiline string representing ASCII art.

    Returns:
        str: Colorized ASCII art string with ANSI escape codes applied.
    """

    colors = [
        "\033[31m",
        "\033[91m",
        "\033[33m",
        "\033[93m",
        "\033[32m",
        "\033[92m",
        "\033[36m",
        "\033[96m",
        "\033[34m",
        "\033[94m",
        "\033[35m",
        "\033[95m",
    ]

    lines = art_string.strip("\n").split("\n")
    colored_art = ""

    for line in lines:
        for x, char in enumerate(line):
            color = colors[x % len(colors)]
            colored_art += f"{color}{char}"
        colored_art += "\n"

    return colored_art + "\033[0m"


def handle_color() -> str:
    """
    Prompt the user to select a display color mode.

    Provides a menu for choosing between predefined display styles
    or accessing a hidden menu with additional color options.

    Returns:
        str: ANSI color code corresponding to the selected display mode.
    """

    print()

    while True:
        print(f"{print_rainbow_text('Please select a version')}\n")

        choice = input(print_rainbow_text(
            "1: Normal version\n"
            "2: Refined version\n"
            "(...)\n\n")
        )

        if choice == "1":
            print()
            return RESET

        elif choice == "2":
            print()
            return BLACK

        elif choice == "3":
            print()
            print(f"{print_rainbow_text('You found a secret menu!')}")
            while True:
                secret = input(
                    f"\n{print_rainbow_text('Choose your color:')}\n\n"
                    f"{RED}1: Red{RESET}\n"
                    f"{YELLOW}2: Yellow{RESET}\n"
                    f"{GREEN}3: Green{RESET}\n"
                    f"{CYAN}4: Cyan{RESET}\n"
                    f"{PURPLE}5: Purple{RESET}\n\n"
                )

                if secret == "1":
                    return RED
                elif secret == "2":
                    return YELLOW
                elif secret == "3":
                    return GREEN
                elif secret == "4":
                    return CYAN
                elif secret == "5":
                    return PURPLE
                else:
                    print()
                    print("Bad answer please try again")

        else:
            print()
            print("Bad answer, please try again")

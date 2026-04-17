import sys
from typing import Any
from colors import (
    RED,
    RESET,
    print_rainbow_text,
    print_rainbow_art,
    handle_color
)
from loading import fake_loading_bar
from parsing import (
    recup_config_lines,
    validate_and_convert,
    choose,
    input_user,
)
from maze_generator import MazeGenerator


def run_maze_sequence(valid_dict: dict[str, Any], color: str) -> bool:
    """
    Generate, solve, and display a maze based on validated configuration.

    This function orchestrates the full lifecycle of a maze:
    - Instantiates a MazeGenerator with provided configuration
    - Generates the maze structure
    - Exports the maze to a file
    - Computes the solution path using BFS
    - Handles user interaction for displaying, regenerating, or exiting

    Args:
        valid_dict (dict[str, Any]):
        Validated configuration dictionary containing maze parameters
        (WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, optional SEED).
        color (str):
        ANSI color code used for rendering the maze in the terminal.

    Returns:
        bool: False if the user chooses to exit or reset to main menu,
            otherwise continues execution through recursive calls.
    """

    maze = MazeGenerator(
        valid_dict["WIDTH"],
        valid_dict["HEIGHT"],
        valid_dict["ENTRY"],
        valid_dict["EXIT"],
        valid_dict["OUTPUT_FILE"],
        valid_dict["PERFECT"],
        seed=valid_dict.get("SEED")
    )

    try:
        maze.generate_maze_dfs()
    except ValueError as error:
        print()
        print(error)
        print("Please change your configuration to avoid any conflict")
        sys.exit()

    maze.export_file()

    path = maze.find_exit()

    while True:
        print("\nMaze unsolved\n")
        while True:
            maze.display_maze(None, color)

            print()
            choice = choose()
            if choice == "1":
                break
            if choice == "2":
                return run_maze_sequence(valid_dict, color)
            if choice == "3":
                color = handle_color()
                continue
            if choice == "4":
                return False

        print("\nMaze solved\n")
        maze.display_maze(path, color)

        while True:
            print(print_rainbow_text("\n1: Hide solution\n"
                                     "2: Generate new maze\n"
                                     "3: Change color\n"
                                     "4: Reset\n"
                                     "5: Quit\n"))
            unsolve = input()
            if unsolve == "1":
                break
            if unsolve == "2":
                return run_maze_sequence(valid_dict, color)
            if unsolve == "3":
                color = handle_color()
                maze.display_maze(path, color)
                continue
            if unsolve == "4":
                return False
            if unsolve == "5":
                exit = input(print_rainbow_text(
                    "\nReally Exit ? (yes or no):\n\n")).lower().strip()
                if exit in ["yes", "y"]:
                    print()
                    print("Exiting...")
                    print()
                    print("See you soon !")
                    sys.exit()
                if exit in ["no", "n"]:
                    continue
            print("Bad answer please try again")
            print()

        if unsolve == "1":
            continue

        if input_user() is True:
            return False
        return False


def main() -> None:
    """
    Entry point of the A-Maze-Ing program.

    This function:
    - Validates command-line arguments
    - Displays a loading sequence
    - Parses and validates the configuration file
    - Initializes the main user interface loop
    - Handles user input for maze generation, color selection, and exit
    - Gracefully handles interruptions (Ctrl+C, EOF)

    The program runs in a loop until the user explicitly exits.
    """

    if len(sys.argv) != 2:
        print(f"{RED}Error invalid arguments or missing configuration"
              f" file{RESET}\nProgram executed in default mode\n")

    while True:
        print()
        print("Loading our amazing project....\n")
        fake_loading_bar(3, "Loading...")
        print("\n")
        print(f"{RED}FAIL !\n")
        print(f"{RESET}--> Back to basic mode\n\n")

        try:
            initial_dict = recup_config_lines()
            valid_dict = validate_and_convert(initial_dict)

            color = RESET

            print("=" * 54)
            print("Welcome to the ultimate version of A-Maze-Ing project!")
            print("=" * 54)

            while True:
                first_menu = input(
                    f"\n{color}Selection:{RESET}\n\n"
                    "1: Generate a new Maze\n"
                    "2: Redefine color\n"
                    "3: Active special effects\n"
                    "4: Quit\n\n"
                )
                if first_menu == "1":
                    if run_maze_sequence(valid_dict, color) is False:
                        break

                elif first_menu == "2":
                    color = handle_color()

                elif first_menu == "3":
                    print()
                    print("Coming soon... "
                          "(under developpement with 42next!)")

                elif first_menu == "4":
                    exit = input("\nReally Exit ? (yes or no):\n\n")
                    if exit in ["yes", "y"]:
                        print()
                        print("Exiting...")
                        print()
                        print("See you soon !")
                        sys.exit()
                    if exit in ["no", "n"]:
                        continue

                else:
                    print()
                    print("Unrecognized option...")
                    print()
                    print("Please try again!")
                    print()

        except (KeyboardInterrupt, EOFError):
            message = r"""
     _________________________________________________________
    /                                                          \
    |    ___  _   _    __  __ _     _     ____  ___  ____  _   |
    |   / _ \| | | |  |  \/  | \   / |   / ___|/ _ \|  _ \| |  |
    |  | | | | |_| |  | |\/| |\ \ / /   | |  _| | | | | | | |  |
    |  | |_| |  _  |  | |  | | \ V /    | |_| | |_| | |_| |_|  |
    |   \___/|_| |_|  |_|  |_|  |_|      \____|\___/|____/(_)  |
    |                                                          |
    |                                                          |
    |                YOU'VE KILLED A-MAZE-ING !                |
    \__________________________________________________________/
    """
            print()
            print(f"{print_rainbow_art(message)}")
            sys.exit(0)


if __name__ == "__main__":
    main()

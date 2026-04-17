import sys
from colors import print_rainbow_text, RED, RESET
from typing import Any


def recup_config_lines() -> dict[str, str]:
    """
    Read and parse the configuration file into a dictionary.

    The function retrieves the configuration file name from command-line
    arguments if provided, otherwise defaults to "default.txt". It reads
    the file line by line, ignoring comments and empty lines, and extracts
    key-value pairs separated by '='.

    Basic validation is performed:
    - Ensures each line contains a '='
    - Ensures keys and values are not empty
    - Prevents duplicate keys

    On error (file not found, permission issues, invalid format),
    the program exits with an error message.

    Returns:
        dict[str, str]: Dictionary containing
    raw configuration key-value pairs.
    """

    config_name_file = "default.txt"

    if len(sys.argv) == 2:

        try:
            config_name_file = sys.argv[1]
            with open(config_name_file, "r") as _:
                _.close()

        except OSError:

            print(f"{RED}Error invalid arguments or missing configuration "
                  f"file{RESET}\n")
            print("Program executed in default mode\n")

            config_name_file = "default.txt"

    config: dict[str, str] = {}
    try:
        with open(config_name_file, "r") as config_file:

            for line in config_file:

                line = line.strip()

                if line.startswith("#"):
                    continue
                if not line:
                    continue
                if "=" not in line:
                    print("Format error: missing =")
                    sys.exit()

                key, value = line.split("=", 1)

                if not key or not value:
                    print("Format error: missing key or value")
                    sys.exit()

                key = key.strip()
                value = value.strip()

                if key in config:
                    print(f"Duplicate key: {key}")
                    sys.exit()

                config.update({key: value})

    except FileNotFoundError:
        print("Missing file. Unable to find some config file.")
        sys.exit()

    except PermissionError:
        print(f"Failed to access configuration file: {config_name_file}")
        sys.exit()

    except Exception:
        print(f"Corrupted or missing data in {config_name_file}")
        sys.exit()

    return config


def validate_and_convert(config: dict[str, str]) -> dict[str, Any]:
    """
    Validate and convert raw configuration values to appropriate types.

    This function checks the presence of mandatory keys and validates
    their values according to expected constraints:
    - WIDTH and HEIGHT must be integers > 2
    - ENTRY and EXIT must be valid coordinates within bounds
    - ENTRY and EXIT must be different
    - OUTPUT_FILE must be a valid .txt filename
    - PERFECT must be a boolean value ("true" or "false")
    - SEED (optional) must be a valid integer

    All values are converted to their appropriate types (int, tuple, bool).

    On invalid input, the program exits with an error message.

    Args:
        config (dict[str, str]): Raw configuration dictionary.

    Returns:
        dict[str, Any]: Validated and typed configuration dictionary.
    """

    config_name_file = "default.txt"
    if len(sys.argv) == 2:
        config_name_file = sys.argv[1]

    mandatory_keys = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    for key in mandatory_keys:
        if key not in config:
            print(f"Missing key: {key}")
            sys.exit()
    limit = 300
    try:
        checked_width = int(config['WIDTH'])
    except Exception:
        print("Invalid WIDTH: Width type value is not conform")
        sys.exit()

    if not 2 <= checked_width <= limit:
        print(f"Invalid WIDTH: Width must be between 2 and {limit}")
        sys.exit()

    try:
        checked_height = int(config['HEIGHT'])
    except Exception:
        print("Invalid HEIGHT: Height type value is not conform")
        sys.exit()

    if not 2 <= checked_height <= limit:
        print(f"Invalid HEIGHT: Height must be between 2 and {limit}")
        sys.exit()

    try:
        entry_abs, entry_ord = config['ENTRY'].split(',')
        checked_entry_abs = int(entry_abs)
        checked_entry_ord = int(entry_ord)
        checked_entry = (checked_entry_abs, checked_entry_ord)
    except Exception:
        print("Invalid ENTRY: must be 'x,y' with values inside maze bounds")
        sys.exit()

    if checked_entry_abs < 0 or checked_entry_abs >= checked_width:
        print("Invalid ENTRY: must be 'x,y' with values inside maze bounds")
        sys.exit()

    if checked_entry_ord < 0 or checked_entry_ord >= checked_height:
        print("Invalid ENTRY: must be 'x,y' with values inside maze bounds")
        sys.exit()

    try:
        exit_abs, exit_ord = config['EXIT'].split(',')
        checked_exit_abs = int(exit_abs)
        checked_exit_ord = int(exit_ord)
        checked_exit = (checked_exit_abs, checked_exit_ord)
    except Exception:
        print("Invalid EXIT: must be 'x,y' with values inside maze bounds")
        sys.exit()

    if checked_exit_abs < 0 or checked_exit_abs >= checked_width:
        print("Invalid EXIT: must be 'x,y' with values inside maze bounds")
        sys.exit()

    if checked_exit_ord < 0 or checked_exit_ord >= checked_height:
        print("Invalid EXIT: must be 'x,y' with values inside maze bounds")
        sys.exit()

    if checked_entry == checked_exit:
        print("Error: Entry and Exit could not be the same")
        sys.exit()

    try:
        checked_output_file = config['OUTPUT_FILE']
        if not checked_output_file.endswith(".txt"):
            raise ValueError("Invalid outputfile, must respect .txt extension")
        if checked_output_file == "requirements.txt" or \
                checked_output_file == config_name_file:
            raise ValueError(f"Invalid output file, can't be requirements.txt"
                             f" or {config_name_file}")
        if checked_output_file.__contains__("/") or\
                checked_output_file.startswith("."):
            raise ValueError("Error, output file must be in project directory")

    except ValueError as e:
        print(e)
        sys.exit()

    perfect_value = config["PERFECT"].lower()

    if perfect_value not in ["true", "false"]:
        print("Invalid value for PERFECT")
        sys.exit()
    else:
        checked_perfect = config['PERFECT'].lower() == "true"

    seed = None
    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except Exception:
            print("Invalid SEED value")
            sys.exit()

    return {
        "WIDTH": checked_width,
        "HEIGHT": checked_height,
        "ENTRY": checked_entry,
        "EXIT": checked_exit,
        "OUTPUT_FILE": checked_output_file,
        "PERFECT": checked_perfect,
        "SEED": seed
        }


def choose() -> str:
    """
    Display a menu and retrieve a valid user choice.

    The function presents options to the user and ensures that the input
    is valid. If the user chooses to quit, a confirmation is requested.
    Invalid inputs trigger a retry using recursion.

    Returns:
        str: User choice ("1", "2", or "3").
    """

    try:
        print(print_rainbow_text("1: Display Solution\n"
                                 "2: Generate new maze\n"
                                 "3: Change color\n"
                                 "4: Reset\n"
                                 "5: Quit\n"))
        inp = input()
        if inp in ["1", "2", "3", "4"]:
            return inp
        if inp == "5":
            exit = input(
                print_rainbow_text(
                    "\nReally Exit ? (yes or no):\n\n")).lower().strip()
            if exit in ["yes", "y"]:
                print()
                print("Exiting...")
                print()
                print("See you soon !")
                sys.exit()
            if exit in ["no", "n"]:
                return choose()
            else:
                raise ValueError
        else:
            raise ValueError

    except ValueError:
        print()
        print("Incorrect answer. Please choose another option")
        print()
        return choose()


def input_user() -> bool:
    """
    Ask the user whether to reset the program or quit.

    Accepts multiple variations of input (e.g., "reset", "r", "quit", "q").
    Invalid inputs trigger a retry using recursion.

    Returns:
        bool: True if the user chooses to reset, otherwise exits the program.
    """

    try:
        reset = input("\nReset or quit ?\n").lower().strip()
        if reset in ["reset", "r"]:
            return True

        if reset in ["q", "quit", "exit"]:
            print()
            print("Exiting...")
            print()
            print("See you soon !")
            sys.exit()

        else:
            raise ValueError
    except ValueError:
        print()
        print("Incorrect answers please choose another option")
        print()
        return input_user()

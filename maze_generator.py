import random
import sys
from colors import RED, GREEN, RESET, print_rainbow_text
from typing import Optional


class MazeGenerator:
    """
    Generate, manipulate, solve, and export a maze.

    This class encapsulates all logic related to maze creation:
    - Grid initialization with walls
    - Maze generation using DFS (backtracking)
    - Optional imperfections (extra openings)
    - Pathfinding using BFS
    - ASCII display of the maze
    - Export to hexadecimal format with solution
    - Optional reproducibility using a random seed

    Attributes:
        width (int): Width of the maze in number of cells.
        height (int): Height of the maze in number of cells.
        entry (tuple[int, int]): Entry cell coordinates (x, y).
        exit (tuple[int, int]): Exit cell coordinates (x, y).
        output_file (str): Path to the output file.
        perfect (bool): Whether the maze should be perfect (single solution).
        maze (list[list[dict[str, bool]]]): 2D grid representing
        cells and walls.
        logo (set[tuple[int, int]]): Set of coordinates
        reserved for the "42" pattern.
        seed (Optional[int]): Seed used for deterministic generation.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int] = None
    ) -> None:
        """
        Initialize the maze structure with all walls present.

        Each cell is initialized with four walls (North, East, South, West).
        The maze grid is represented as a 2D list of dictionaries.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
            entry (tuple[int, int]): Entry coordinates.
            exit (tuple[int, int]): Exit coordinates.
            output_file (str): Output file path.
            perfect (bool): Whether the maze should be perfect.
            seed (Optional[int]): Seed for reproducible maze generation.
        """

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect

        self.random = random.Random(seed)

        self.maze: list[list[dict[str, bool]]] = []

        self.logo: set[tuple[int, int]] = set()

        for _ in range(self.height):
            row: list[dict[str, bool]] = []
            for _ in range(self.width):
                cell = {
                    "N": True,
                    "E": True,
                    "S": True,
                    "W": True
                }
                row.append(cell)
            self.maze.append(row)

    def add_42_pattern(self) -> None:
        """
        Insert a "42" pattern into the maze using fully closed cells.

        The pattern is centered in the maze if space allows. Cells used
        for the pattern are marked and excluded from maze generation.

        If the maze is too small or if the pattern overlaps with the entry
        or exit, the pattern is skipped.
        """

        pattern = [
            "4   222",
            "4     2",
            "444 222",
            "  4 2  ",
            "  4 222"
        ]

        logo_height = len(pattern)
        logo_width = len(pattern[0])

        if self.width < logo_width + 2 or self.height < logo_height + 2:
            return

        start_x = (self.width - logo_width) // 2
        start_y = (self.height - logo_height) // 2

        temp_logo: set[tuple[int, int]] = set()

        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                if char != " ":
                    x = start_x + dx
                    y = start_y + dy

                    if 0 <= x < self.width and 0 <= y < self.height:
                        temp_logo.add((x, y))

        if self.entry in temp_logo:
            raise ValueError(
                "Conflict between central logo and entry coordinates")

        if self.exit in temp_logo:
            raise ValueError(
                "Conflict between central logo and exit coordinates")

        for (x, y) in temp_logo:
            self.logo.add((x, y))
            self.maze[y][x] = {
                "N": True,
                "E": True,
                "S": True,
                "W": True
            }

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove the wall between two adjacent cells.

        Updates both cells to ensure wall consistency. If either cell is part
        of the "42" pattern, no modification is applied.

        Args:
            x1 (int): X-coordinate of the first cell.
            y1 (int): Y-coordinate of the first cell.
            x2 (int): X-coordinate of the second cell.
            y2 (int): Y-coordinate of the second cell.
        """

        if (x1, y1) in self.logo or (x2, y2) in self.logo:
            return

        if x2 == x1 + 1 and y2 == y1:
            self.maze[y1][x1]["E"] = False
            self.maze[y2][x2]["W"] = False

        elif x2 == x1 - 1 and y2 == y1:
            self.maze[y1][x1]["W"] = False
            self.maze[y2][x2]["E"] = False

        elif y2 == y1 - 1 and x2 == x1:
            self.maze[y1][x1]["N"] = False
            self.maze[y2][x2]["S"] = False

        elif y2 == y1 + 1 and x2 == x1:
            self.maze[y1][x1]["S"] = False
            self.maze[y2][x2]["N"] = False

        else:
            print("Cells are not adjacent")

    def generate_maze_dfs(self) -> None:
        """
        Generate the maze using a depth-first search (DFS) algorithm.

        The algorithm starts from the entry point and explores the grid
        by carving paths between unvisited neighboring cells.

        If the maze is not perfect, additional walls are randomly removed
        to introduce multiple possible paths.

        The "42" pattern is preserved during generation.
        """

        try:
            self.logo.clear()
            self.add_42_pattern()
        except ValueError as error:
            raise ValueError(f"Error: {error}")

        path: list[tuple[int, int]] = []
        explored: set[tuple[int, int]] = set()

        x, y = self.entry

        path.append((x, y))
        explored.add((x, y))

        while path:

            current = path[-1]
            x, y = current

            possibilities: list[tuple[int, int]] = []

            if (
                x + 1 < self.width
                and (x + 1, y) not in explored
                and (x + 1, y) not in self.logo
            ):
                possibilities.append((x + 1, y))

            if (
                x - 1 >= 0
                and (x - 1, y) not in explored
                and (x - 1, y) not in self.logo
            ):
                possibilities.append((x - 1, y))

            if (
                y + 1 < self.height
                and (x, y + 1) not in explored
                and (x, y + 1) not in self.logo
            ):
                possibilities.append((x, y + 1))

            if (
                y - 1 >= 0
                and (x, y - 1) not in explored
                and (x, y - 1) not in self.logo
            ):
                possibilities.append((x, y - 1))

            if possibilities:
                chosen_cell = self.random.choice(possibilities)
                new_x, new_y = chosen_cell
                self.remove_wall(x, y, new_x, new_y)
                path.append((new_x, new_y))
                explored.add((new_x, new_y))
            else:
                path.pop()

        if not self.perfect:

            for _ in range(2):
                hazard_x = self.random.randint(0, self.width - 2)
                hazard_y = self.random.randint(0, self.height - 2)

                self.remove_wall(
                    hazard_x, hazard_y, hazard_x + 1, hazard_y)
                self.remove_wall(
                    hazard_x, hazard_y, hazard_x, hazard_y + 1)

    def display_maze(
        self,
        path: Optional[list[tuple[int, int]]] = None,
        color: str = RESET
    ) -> None:
        """
        Display the maze in the terminal using ASCII characters.

        Walls, entry, exit, and optional solution path are rendered with
        colors. The "42" pattern is displayed as filled cells.

        Args:
            path (Optional[list[tuple[int, int]]]): List of coordinates forming
                the solution path. If None, no path is displayed.
            color (str): ANSI color code used for walls.
        """

        path_set: set[tuple[int, int]] = set(path) if path else set()

        top_line = ""
        for _ in range(self.width):
            top_line += f"{color}+---{RESET}"
        top_line += f"{color}+{RESET}"

        print(top_line)

        for y, row in enumerate(self.maze):

            inside_line = ""
            bottom_line = ""

            for x, cell in enumerate(row):

                bottom_line += f"{color}+{RESET}"

                if cell["W"]:
                    inside_line += f"{color}|{RESET}"
                else:
                    inside_line += " "

                if (x, y) == self.entry:
                    inside_line += f"{GREEN} E {RESET}"
                elif (x, y) == self.exit:
                    inside_line += f"{RED} X {RESET}"
                elif (x, y) in self.logo:
                    inside_line += "###"
                elif (x, y) in path_set:
                    inside_line += print_rainbow_text(" * ")
                else:
                    inside_line += "   "

                if cell["S"]:
                    bottom_line += f"{color}---{RESET}"
                else:
                    bottom_line += "   "

            inside_line += f"{color}|{RESET}"
            bottom_line += f"{color}+{RESET}"

            print(inside_line)
            print(bottom_line)

    def solver_bfs(self) -> dict[tuple[int, int], tuple[int, int]]:
        """
        Perform a breadth-first search to explore the maze.

        Starting from the entry point, this method explores reachable cells
        and records parent relationships for path reconstruction.

        Returns:
            dict[tuple[int, int], tuple[int, int]]:
        Mapping of each visited cell to its parent cell.
        """

        to_explore = [self.entry]

        explored = set([self.entry])
        parents: dict[tuple[int, int], tuple[int, int]] = {}

        while to_explore:

            current = to_explore.pop(0)
            x, y = current

            if current == self.exit:
                break

            cell = self.maze[y][x]

            neighbors: list[tuple[int, int]] = []

            if not cell["N"]:
                neighbors.append((x, y - 1))
            if not cell["E"]:
                neighbors.append((x + 1, y))
            if not cell["S"]:
                neighbors.append((x, y + 1))
            if not cell["W"]:
                neighbors.append((x - 1, y))

            for nx, ny in neighbors:
                if (nx, ny) not in explored:
                    explored.add((nx, ny))
                    to_explore.append((nx, ny))
                    parents[(nx, ny)] = (x, y)

        return parents

    def build_path(
        self,
        parents: dict[tuple[int, int], tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """
        Reconstruct the path from entry to exit using parent relationships.

        Args:
            parents (dict[tuple[int, int], tuple[int, int]]): Mapping of each
                cell to its parent as produced by BFS.

        Returns:
            list[tuple[int, int]]: Ordered list of coordinates
        from entry to exit.

        Returns an empty list if no path exists.
        """

        if self.exit not in parents:
            print("No path found from entry to exit")
            return []

        path: list[tuple[int, int]] = []
        current = self.exit

        while current != self.entry:
            path.append(current)
            current = parents[current]

        path.append(self.entry)
        path.reverse()

        return path

    def path_to_directions(
        self,
        path: list[tuple[int, int]]
    ) -> list[str]:
        """
        Convert a path of coordinates into cardinal directions.

        Each step between consecutive cells is translated into one of
        the directions: "N", "E", "S", or "W".

        Args:
            path (list[tuple[int, int]]):
        List of coordinates representing a path.

        Returns:
            list[str]: List of direction characters.
        """

        directions: list[str] = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 == x1 + 1:
                directions.append("E")
            elif x2 == x1 - 1:
                directions.append("W")
            elif y2 == y1 + 1:
                directions.append("S")
            elif y2 == y1 - 1:
                directions.append("N")

        return directions

    def find_exit(self) -> list[tuple[int, int]]:
        """
        Find the shortest path from entry to exit.

        This method combines BFS and path reconstruction to return
        the final solution path.

        Returns:
            list[tuple[int, int]]: Shortest path from entry to exit.
        """

        parents = self.solver_bfs()

        path = self.build_path(parents)

        return path

    def export_file(self) -> None:
        """
        Export the maze and its solution to a file.

        The maze is written row by row using hexadecimal encoding
        to represent wall configurations for each cell.

        After the grid, the file includes:
        - Entry coordinates
        - Exit coordinates
        - Solution path as a sequence of directions

        Returns:
            None
        """

        try:
            with open(self.output_file, "w") as file:

                for row in self.maze:
                    line = ""

                    for cell in row:
                        value = 0

                        if cell["N"]:
                            value += 1
                        if cell["E"]:
                            value += 2
                        if cell["S"]:
                            value += 4
                        if cell["W"]:
                            value += 8

                        hex_value = hex(value)
                        upper_ex_value = hex_value.upper()
                        purged_upper_ex_value = upper_ex_value[2:]

                        line += purged_upper_ex_value

                    file.write(line + "\n")

                file.write("\n")

                entry_x, entry_y = self.entry
                file.write(f"{entry_x},{entry_y}\n")

                exit_x, exit_y = self.exit
                file.write(f"{exit_x},{exit_y}\n")

                path = self.find_exit()
                directions = self.path_to_directions(path)
                file.write("".join(directions) + "\n")
        except PermissionError:
            print("\nError : unable to export the solution")
            print("Check your output_file permissions and start again")
            print()
            while True:
                file_invalid = input("Do you want to create another one"
                                     "?(y/n)")
                if file_invalid in ["yes", "y"]:
                    self.output_file = "backup.txt"
                    return self.export_file()
                if file_invalid in ["n", "no"]:
                    sys.exit()
                print("Bad answer please try again")

import random
from collections import deque
from typing import Optional


class MazeGenerator:
    """
    Generate and solve a maze using DFS and BFS algorithms.

    This class handles:
    - Grid initialization with walls
    - Maze generation using depth-first search (DFS)
    - Optional imperfections (non-perfect mazes)
    - Pathfinding using breadth-first search (BFS)

    The maze structure is stored internally and can be accessed
    or used to retrieve a solution path.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: Optional[int] = None,
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
            perfect (bool): Whether the maze should be perfect.
            seed (Optional[int]): Seed for random generation.
        """

        if seed is not None:
            random.seed(seed)

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        self.maze: list[list[dict[str, bool]]] = []

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

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove the wall between two adjacent cells.

        Updates both cells to ensure wall consistency.

        Args:
            x1 (int): X-coordinate of the first cell.
            y1 (int): Y-coordinate of the first cell.
            x2 (int): X-coordinate of the second cell.
            y2 (int): Y-coordinate of the second cell.
        """

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
            raise ValueError("Cells are not adjacent")

    def generate(self) -> None:
        """
        Generate the maze using a depth-first search (DFS) algorithm.
        """

        path: list[tuple[int, int]] = []
        explored: set[tuple[int, int]] = set()

        x, y = self.entry

        path.append((x, y))
        explored.add((x, y))

        while path:

            x, y = path[-1]

            possibilities: list[tuple[int, int]] = []

            if (
                x + 1 < self.width
                and (x + 1, y) not in explored
            ):
                possibilities.append((x + 1, y))

            if (
                x - 1 >= 0
                and (x - 1, y) not in explored
            ):
                possibilities.append((x - 1, y))

            if (
                y + 1 < self.height
                and (x, y + 1) not in explored
            ):
                possibilities.append((x, y + 1))

            if (
                y - 1 >= 0
                and (x, y - 1) not in explored
            ):
                possibilities.append((x, y - 1))

            if possibilities:
                chosen_cell = random.choice(possibilities)
                new_x, new_y = chosen_cell
                self.remove_wall(x, y, new_x, new_y)
                path.append((new_x, new_y))
                explored.add((new_x, new_y))
            else:
                path.pop()

        if not self.perfect:

            for _ in range(2):
                hazard_x = random.randint(0, self.width - 2)
                hazard_y = random.randint(0, self.height - 2)

                self.remove_wall(
                    hazard_x, hazard_y, hazard_x + 1, hazard_y)
                self.remove_wall(
                    hazard_x, hazard_y, hazard_x, hazard_y + 1)

    def bfs(self) -> dict[tuple[int, int], tuple[int, int]]:
        """
        Internal BFS used to explore the maze.
        """

        queue = deque([self.entry])
        explored = {self.entry}
        parents: dict[tuple[int, int], tuple[int, int]] = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit:
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
                    queue.append((nx, ny))
                    parents[(nx, ny)] = (x, y)

        return parents

    def solve(self) -> list[tuple[int, int]]:
        """
        Compute the shortest path from entry to exit.

        Returns:
            list[tuple[int, int]]: The solution path.
        """

        parents = self.bfs()
        return self.build_path(parents)

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
            raise ValueError("No path found from entry to exit")

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

    def get_maze(self) -> list[list[dict[str, bool]]]:
        """
        Return the internal maze structure.

        Returns:
            list[list[dict[str, bool]]]: The maze grid.
        """
        return self.maze

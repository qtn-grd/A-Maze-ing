from maze_generator import MazeGenerator


def test_path_exists() -> None:

    maze = MazeGenerator(5, 5, (0, 0), (4, 4), "output.txt", True)
    maze.generate_maze_dfs()

    path = maze.find_exit()

    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)


def test_path_not_empty() -> None:

    maze = MazeGenerator(5, 5, (0, 0), (4, 4), "output.txt", True)
    maze.generate_maze_dfs()

    path = maze.find_exit()

    assert len(path) > 0


def test_small_maze() -> None:
    maze = MazeGenerator(3, 3, (0, 0), (2, 2), "out.txt", True)
    maze.generate_maze_dfs()

    path = maze.find_exit()
    assert len(path) > 0


def test_directions_match_path() -> None:

    maze = MazeGenerator(5, 5, (0, 0), (4, 4), "output.txt", True)
    maze.generate_maze_dfs()

    path = maze.find_exit()
    directions = maze.path_to_directions(path)
    assert len(directions) == len(path) - 1


def test_logo_does_not_overlap_entry_exit() -> None:

    maze = MazeGenerator(10, 10, (1, 1), (8, 8), "output.txt", True)
    maze.generate_maze_dfs()

    assert maze.entry not in maze.logo
    assert maze.exit not in maze.logo


def test_seed_reproducibility() -> None:
    maze1 = MazeGenerator(5, 5, (0, 0), (4, 4), "out.txt", True, seed=42)
    maze2 = MazeGenerator(5, 5, (0, 0), (4, 4), "out.txt", True, seed=42)

    maze1.generate_maze_dfs()
    maze2.generate_maze_dfs()

    assert maze1.maze == maze2.maze


def test_wall_consistency() -> None:
    maze = MazeGenerator(5, 5, (0, 0), (4, 4), "out.txt", True)
    maze.generate_maze_dfs()

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.maze[y][x]

            if x + 1 < maze.width:
                right = maze.maze[y][x + 1]
                assert cell["E"] == right["W"]

            if y + 1 < maze.height:
                down = maze.maze[y + 1][x]
                assert cell["S"] == down["N"]

# A_maze_ing

## 🎯 _Description_

The goal of this project is to build, in Python, a program capable of generating a maze of variable size along with its solution.

The maze is generated using parameters defined in a configuration file (`.txt`), including:

| Key         | Description                   | Example                   |
|:------------|:------------------------------|:--------------------------|
| WIDTH       | Maze width (number of cells)  | WIDTH=20                  |
| HEIGHT      | Maze eight                    | HEIGHT=15                 |
| ENTRY       | Entry coordinates(x,y)        | ENTRY=0,0                 |
| EXIT        | Entry coordinates(x,y)        | EXIT=19,14                |
| OUTPUT_FILE | Output filename               | OUTPUT_FILE=maze.txt      |
| PERFECT     | Is the maze perfect?          | PERFECT=True              |

SEED is an optional integer parameter that allows reproducible maze generation.

In this project, SEED must be an integer value for consistency and predictable reproducibility.

To preserve readability in terminal rendering, maze dimensions are intentionally limited (e.g., width ≤ 60).


### Basic usage

To use this project, import the class MazeGenerator from generator.py, determine parameters and use one or many methods implemented to generate, solve the maze or get the path information.

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42
)

maze.generate()

path = maze.solve()
grid = maze.get_maze()
```

### Parameters

* `width` (int): Width of the maze
* `height` (int): Height of the maze
* `entry` (tuple[int, int]): Entry coordinates
* `exit` (tuple[int, int]): Exit coordinates
* `perfect` (bool): If `True`, generates a perfect maze (single solution)
* `seed` (Optional[int]): Allows reproducible maze generation

### Accessing results

* `maze.get_maze()` → returns the internal maze structure
* `maze.solve()` → returns the shortest path from entry to exit
* `maze.path_to_directions(path)` → converts a path into directions (`N`, `E`, `S`, `W`)

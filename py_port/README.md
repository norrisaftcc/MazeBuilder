# MazeBuilder Python Port

This is a Python port of the MazeBuilder program, originally written in C# and C++.

## Features

- Generation of "perfect" mazes using multiple algorithms:
  - Binary Tree
  - Sidewinder
  - Aldous-Broder
- Multiple rendering options:
  - ASCII-based console display
  - Matplotlib graphical rendering
  - Interactive terminal navigation with asciimatics
- Multiple visual themes (default, wizardry, retro)
- Pathfinding using Dijkstra's algorithm
- Finding the "solution" (longest shortest path) through the maze
- Save/load mazes to/from JSON files

## Installation

No special installation is required beyond Python 3.6+. The program uses only standard library modules.

## Usage

```bash
# Generate a default maze
python run_maze.py

# Specify maze dimensions and algorithm
python run_maze.py --rows 20 --cols 20 --algorithm binary

# Show the solution path
python run_maze.py --show-solution

# Use a specific theme
python run_maze.py --theme wizardry

# Save a generated maze to JSON
python run_maze.py --rows 15 --cols 15 --save-maze my_maze.json

# Load a previously saved maze
python run_maze.py --load-maze my_maze.json --show-solution

# Interactive navigation (requires asciimatics)
python interactive_maze.py
# Or
python run_maze.py --renderer asciimatics
```

## Project Structure

- `cell.py` - Cell class representing a single cell in the maze
- `grid.py` - Grid class containing a 2D collection of cells (with save/load support)
- `run_maze.py` - Unified command-line interface
- `interactive_maze.py` - Interactive maze explorer
- `algorithms/` - Maze generation algorithms
  - `binary_tree.py` - Binary Tree algorithm implementation
  - `sidewinder.py` - Sidewinder algorithm implementation
  - `aldous_broder.py` - Aldous-Broder algorithm implementation
- `pathfinding/` - Pathfinding algorithms
  - `distances.py` - Distance calculation utilities
  - `dijkstra.py` - Dijkstra's algorithm implementation
- `visualization/` - Rendering and theme system
  - `renderer_base.py` - Base renderer interface
  - `text_renderer.py` - Console ASCII renderer
  - `matplotlib_renderer.py` - Graphical renderer
  - `asciimatics_renderer.py` - Interactive terminal renderer
  - `themes.py` - Visual theme definitions
- `tests/` - Pytest test suite

## Save and Load Functionality

Mazes can be saved to JSON files for later use:

```bash
# Save a maze to file
python run_maze.py --rows 20 --cols 20 --algorithm binary --save-maze my_maze.json

# Load and display a saved maze
python run_maze.py --load-maze my_maze.json

# Load a maze and solve it
python run_maze.py --load-maze my_maze.json --show-solution

# Load a maze in interactive mode
python run_maze.py --load-maze my_maze.json --renderer asciimatics
```

The JSON format preserves the complete maze structure, including all cell connections.

## Future Enhancements

- Additional maze generation algorithms:
  - Hunt-and-Kill
  - Recursive Backtracker
  - Eller's algorithm
- Advanced pathfinding algorithms (A*)
- 3D maze generation and visualization
- Web-based interface improvements
- Performance optimizations for large mazes

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.
```
## Export to the Crawler

`export_crawler.py` turns a maze into a pack for **the Crawler**, the first-person party crawler in the `games-osr-fort-on-lake` repository (`crawler/SPEC.md`). The pack is data only; the Crawler's own tools validate it and build it into one HTML page that opens from disk.

```bash
# Write a pack: an 8 by 8 Sidewinder maze, seed 7
python export_crawler.py 8 8 --algorithm sidewinder --seed 7 --out out/hedge

# Check, play and build it with the Crawler's tools
CRAWLER=../../games-osr-fort-on-lake/crawler
node $CRAWLER/tools/validate.mjs out/hedge        # OK hedge
node crawler_walk.mjs $CRAWLER out/hedge          # the replay reaches the far gate
node $CRAWLER/tools/build.mjs out/hedge --out out/hedge.html
```

What the exporter does:

- A maze cell is a 10-foot floor square. A link is a floor square between two cells. Everything else is wall.
- Dijkstra's longest path picks the entrance (a stair back to town) and the exit (a stair out, and an ending).
- Distance bands from the entrance become the Crawler's areas, so the clock ticks as the party goes deeper.
- Dead ends off the solution hold rat fights (`--fights`, default 3). The deepest dead end holds the treasure.
- A plate at the entrance states the algorithm's **tell**: Binary Tree always opens north or east; Sidewinder has one gate north per run; Aldous-Broder has no rule, and the plate says so.
- `replay.json` is `{seed, commands}`: a whole game that walks the solution. `crawler_walk.mjs` plays it against the engine and fights through whatever wanders in.

The party, items, abilities, monsters, rules and theme are copied from the Crawler's test fixture; they live in `crawler_base/`. Change them there, or edit the written pack by hand.

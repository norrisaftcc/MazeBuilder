# MazeBuilder Python Port

This is a Python port of the MazeBuilder program, originally written in C# and C++.

## Features

- Generation of "perfect" mazes using the Binary Tree algorithm
- ASCII-based console display
- Pathfinding using Dijkstra's algorithm
- Finding the "solution" (longest shortest path) through the maze

## Installation

No special installation is required beyond Python 3.6+. The program uses only standard library modules.

## Usage

```bash
# Generate a default 10x10 maze
python main.py

# Generate a custom-sized maze
python main.py 15 20

# Generate a maze and show the solution path
python main.py --solve
```

## Project Structure

- `cell.py` - Cell class representing a single cell in the maze
- `grid.py` - Grid class containing a 2D collection of cells
- `main.py` - Main program entry point
- `algorithms/` - Maze generation algorithms
  - `binary_tree.py` - Binary Tree algorithm implementation
- `pathfinding/` - Pathfinding algorithms
  - `distances.py` - Distance calculation utilities
  - `dijkstra.py` - Dijkstra's algorithm implementation
- `tests/` - Pytest test suite

## Future Enhancements

- Additional maze generation algorithms:
  - Sidewinder
  - Aldous-Broder
- Streamlit web interface
- Additional display options
- Maze export/import functionality

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.
```
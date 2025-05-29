# CLAUDE.md

Quick reference for Claude Code when working with the MazeBuilder project.

## Project Overview

MazeBuilder demonstrates maze generation algorithms in C#, C++, and Python.

**Key algorithms:** Binary Tree, Sidewinder, Aldous-Broder, Dijkstra's pathfinding

## Quick Commands

### Python (Primary Development)
```bash
cd py_port
python main.py                # Generate maze
python interactive_maze.py    # Interactive mode
streamlit run streamlit_app.py # Web UI
```

### C++
```bash
cd cpp_port
g++ -std=c++11 mazebuilder.cpp -o mazebuilder && ./mazebuilder
```

### C#
```bash
cd SimpleMazeBuilder1
msbuild SimpleMazeBuilder1.sln
```

## Testing & Linting

```bash
cd py_port
pytest                        # Run tests
python -m flake8 .           # Lint check
python -m mypy .             # Type check
```

## Documentation

- Build instructions: `docs/BUILD_INSTRUCTIONS.md`
- Architecture details: `docs/ARCHITECTURE.md`
- Algorithm explanations: `docs/ALGORITHMS.md`
- Python-specific docs: `py_port/docs/`

## Key Files

- `py_port/main.py` - Main entry point
- `py_port/grid.py` - Core grid implementation
- `py_port/algorithms/` - Maze generation algorithms
- `py_port/visualization/` - Rendering implementations
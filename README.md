# MazeBuilder
2d Maze Projects

A C# port of "Mazes for Programmers" by Jamis Buck.

# Current Status
Cell and Grid initialization are complete.
Binary Tree, Sidewinder, and Aldous-Broder maze generation algorithms implemented.
Pathfinding with Dijkstra's algorithm added to C++ and Python ports.
Python visualization layer implemented with multiple renderers and themes.

# Sprint 2 Priorities (May 2025)
Based on our recent planning meeting, our priorities for this sprint are:
- Improve visualization in C# version
- Complete Python port with modular architecture
- Add more pathfinding algorithms to C++ version
- Performance optimization for large mazes
- Create user-friendly interfaces for all implementations

# What's New
- **Visualization Layer**: The Python port now features a dedicated visualization layer that separates rendering logic from maze algorithms
- **Multiple Renderers**: Support for text-based (terminal), graphical (matplotlib), and interactive terminal (asciimatics) rendering
- **Theme System**: Built-in themes including "Wizardry" and "Retro Terminal" styles
- **Interactive Exploration**: Navigate through mazes with keyboard controls using the asciimatics renderer
- **Streamlit UI**: Interactive web-based interface for maze generation and exploration

# To Do
- Add A* pathfinding to C++ version
- Complete unit test coverage
- Add 3D visualization options
- Performance optimization for large mazes
- Interactive maze solving in the web UI
- Add more themes and customization options
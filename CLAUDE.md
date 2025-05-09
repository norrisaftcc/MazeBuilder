# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MazeBuilder is a project demonstrating maze generation algorithms across multiple language implementations:
- C# (original port from Ruby)
- C++ (ported from C#)
- Python port (under development)

The project implements various maze generation algorithms:
- Binary Tree
- Sidewinder
- Aldous-Broder
- Dijkstra's algorithm for pathfinding

## Build and Run Commands

### C# Version (Windows Forms)

```bash
# Build the C# project (requires Visual Studio or MSBuild)
cd SimpleMazeBuilder1
msbuild SimpleMazeBuilder1.sln

# Run the compiled executable
./SimpleMazeBuilder1/bin/Debug/SimpleMazeBuilder1.exe
```

### C++ Version

```bash
# Compile the C++ version
cd cpp_port
g++ -std=c++11 mazebuilder.cpp -o mazebuilder

# Run with default dimensions (10x10)
./mazebuilder

# Run with custom dimensions
./mazebuilder [rows] [columns]
# Example: ./mazebuilder 15 20

# Compile the pathfinding version
g++ -std=c++11 djikstras.cpp -o djikstras

# Run the pathfinding demo
./djikstras
```

## Code Architecture

### Core Components

1. **Cell Class**
   - Fundamental building block representing a single maze cell
   - Tracks position (row, column)
   - Manages connections to neighboring cells (north, south, east, west) 
   - Uses bit manipulation in C++ for efficient storage of connections

2. **Grid Class**
   - Contains and manages a 2D collection of cells
   - Provides methods for displaying the maze
   - Handles cell neighbor configuration
   - Offers utility methods for the maze algorithms

3. **MazeBuilder Classes**
   - Abstract base class `MazeBuilder` with derived algorithm implementations
   - Each algorithm provides a different method for maze generation:
     - `BinaryTreeMazeBuilder`: Simple algorithm with NE bias
     - `SidewinderMazeBuilder`: Balanced east passages with occasional north links
     - `AldousBroderMazeBuilder`: Unbiased random walk algorithm

4. **Pathfinding (C++ version)**
   - `Distances` class: Maps cells to their distances from a starting point
   - `Dijkstra` class: Implements pathfinding algorithm
   - Can calculate the "solution path" (longest shortest path through the maze)

### Language-Specific Implementations

1. **C#** 
   - Windows Forms UI implementation
   - Original port from Ruby
   - Visual display of maze with cell distances

2. **C++**
   - Console-based ASCII display
   - Performance-focused implementation
   - Enhanced with pathfinding algorithms
   - Bit manipulation for connection storage

## Implementation Details

### Maze Generation Algorithms

1. **Binary Tree Algorithm**
   - For each cell, randomly carve a passage either north or east
   - Creates a "perfect maze" with exactly one path between any two points
   - Has a bias toward the northeast corner

2. **Sidewinder Algorithm**
   - Creates horizontal "runs" of connected cells
   - Randomly ends runs by connecting one cell northward
   - Creates east-west corridors with occasional north passages

3. **Aldous-Broder Algorithm**
   - Performs a random walk, connecting unvisited cells
   - Creates unbiased, perfect mazes
   - Slower but produces more balanced mazes

### Pathfinding

The C++ implementation includes Dijkstra's algorithm for pathfinding:
- Finding the shortest path between any two cells
- Calculating the "solution" (longest shortest path through the maze)
- Visualizing the path through ASCII display
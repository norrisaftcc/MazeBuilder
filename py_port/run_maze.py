#!/usr/bin/env python3
"""
Unified command-line script for maze generation and visualization.

This script provides a single entry point for all maze functionality:
- Generate mazes with different algorithms
- Visualize mazes with different renderers
- Launch interactive maze exploration
"""

import sys
import argparse
import random

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra
from visualization import TextRenderer, MatplotlibRenderer, ThemeManager

# Check if asciimatics is available
try:
    from visualization import AsciimaticsRenderer
    HAS_ASCIIMATICS = True
except ImportError:
    HAS_ASCIIMATICS = False


def main():
    """Main entry point for the unified maze script."""
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='MazeBuilder - A maze generation and visualization tool')
    
    # Maze generation parameters
    parser.add_argument('--rows', '-r', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', '-c', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder', 'aldous-broder'],
                        default='binary', help='Maze generation algorithm to use')
    parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
    
    # Visualization parameters
    parser.add_argument('--theme', '-t', choices=ThemeManager.list_themes(),
                        default='default', help='Visual theme to use')
    parser.add_argument('--renderer', '-R', choices=['text', 'matplotlib', 'asciimatics'],
                        default='text', help='Renderer to use for visualization')
    parser.add_argument('--show-solution', action='store_true', help='Show solution path')
    parser.add_argument('--no-distances', dest='show_distances', action='store_false',
                        help='Hide distances on solution path')
    parser.add_argument('--save', '-S', help='Save output to file (for matplotlib renderer)')
    
    args = parser.parse_args()

    # Check if asciimatics is requested but not available
    if args.renderer == 'asciimatics' and not HAS_ASCIIMATICS:
        print("Error: The asciimatics renderer was requested but not available.")
        print("Please install it with: pip install asciimatics")
        sys.exit(1)

    # Initialize random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Create grid
    grid = Grid(args.rows, args.cols)

    # Apply selected maze generation algorithm
    if args.algorithm == 'binary':
        BinaryTreeMaze.on(grid)
    elif args.algorithm == 'sidewinder':
        SidewinderMaze.on(grid)
    elif args.algorithm == 'aldous-broder':
        grid, _ = AldousBroderMaze.on(grid)

    # Calculate solution path
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)
    distances = Dijkstra.calculate_distances(grid, exit)

    # Render the maze using the selected renderer
    if args.renderer == 'text':
        # Text renderer
        text_renderer = TextRenderer(theme_name=args.theme, use_color=True)
        output = text_renderer.render_maze(
            grid, 
            solution_path=solution if args.show_solution else None, 
            show_distances=args.show_distances,
            distances=distances
        )
        print(output)
        
    elif args.renderer == 'matplotlib':
        # Matplotlib renderer
        matplot_renderer = MatplotlibRenderer(theme_name=args.theme)
        fig = matplot_renderer.render_maze(
            grid, 
            solution_path=solution if args.show_solution else None, 
            show_distances=args.show_distances
        )
        
        filename = args.save if args.save else f"maze_{args.algorithm}_{args.theme}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Maze saved to {filename}")
        
    elif args.renderer == 'asciimatics':
        # Asciimatics renderer
        print("Launching interactive maze explorer...")
        print("Use arrow keys to navigate, 's' to toggle solution, 'h' for help, 'q' to quit")
        
        asciimatics_renderer = AsciimaticsRenderer(theme_name=args.theme)
        asciimatics_renderer.render_maze(
            grid, 
            solution_path=solution, 
            interactive=True,
            show_solution=args.show_solution,
            current_position=(entrance.row, entrance.col)
        )


if __name__ == "__main__":
    main()
import sys
import argparse
import os
import platform
import random

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cell import Cell
from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra

def display_with_path(grid, path, show_distances=False, distances=None, use_color=True):
    """
    Display the maze with a highlighted solution path and optionally show distances.

    Args:
        grid: The maze grid
        path: The solution path through the maze
        show_distances: Whether to show distances in each cell
        distances: The distances object (if show_distances is True)
        use_color: Whether to use color in the output
    """
    # Define entrance and exit for special marking
    entrance = grid.at(grid.rows-1, 0)  # Bottom left
    exit = grid.at(0, grid.cols-1)      # Top right
    # Disable colors on Windows unless running in a modern terminal
    if platform.system() == "Windows" and "TERM" not in os.environ:
        use_color = False

    # ANSI color codes
    if use_color:
        RESET = "\033[0m"
        GREEN_BG = "\033[42m"
        GREEN_TEXT = "\033[32m"
        CYAN_TEXT = "\033[36m"
        RED_TEXT = "\033[31m"
        YELLOW_TEXT = "\033[33m"
        BOLD = "\033[1m"
    else:
        RESET = ""
        GREEN_BG = ""
        GREEN_TEXT = ""
        CYAN_TEXT = ""
        RED_TEXT = ""
        YELLOW_TEXT = ""
        BOLD = ""

    # Helper function to check if a cell is on the path
    def is_on_path(row, col):
        for cell in path:
            if cell.row == row and cell.col == col:
                return True
        return False

    # Display the top border
    output = ['+' + '---+' * grid.cols]

    for r in range(grid.rows):
        # Display cell contents and eastern boundaries
        row = ['|']
        eastern_boundary = ['+']

        for c in range(grid.cols):
            cell = grid.at(r, c)

            # Cell contents
            # Special rendering for entrance and exit cells
            if cell.row == entrance.row and cell.col == entrance.col:
                # Entrance cell (bottom left)
                if is_on_path(r, c) and distances:
                    dist = distances.get_distance(cell)
                    if dist < 10:
                        content = f"{YELLOW_TEXT}{BOLD} E{dist}{RESET}"
                    else:
                        content = f"{YELLOW_TEXT}{BOLD}E{dist}{RESET}"
                else:
                    content = f"{YELLOW_TEXT}{BOLD} E {RESET}"
            elif cell.row == exit.row and cell.col == exit.col:
                # Exit cell (top right)
                if is_on_path(r, c) and distances:
                    dist = distances.get_distance(cell)
                    # Exit always has distance 0
                    content = f"{RED_TEXT}{BOLD} X {RESET}"
                else:
                    content = f"{RED_TEXT}{BOLD} X {RESET}"
            elif is_on_path(r, c):
                # Path cell always shows distance to exit
                if distances:
                    dist = distances.get_distance(cell)
                    if dist < 10:
                        content = f"{GREEN_TEXT} {dist} {RESET}"
                    else:
                        content = f"{GREEN_TEXT}{dist}{RESET} "
                else:
                    content = f"{GREEN_TEXT} * {RESET}"
            elif show_distances and distances:
                # Regular cell with distance
                dist = distances.get_distance(cell)
                if dist == sys.maxsize:  # Unreachable cell
                    content = "   "
                elif dist < 10:
                    content = f"{CYAN_TEXT} {dist} {RESET}"
                else:
                    content = f"{CYAN_TEXT}{dist}{RESET} "
            else:
                # Regular empty cell
                content = "   "

            row.append(content)

            # Eastern boundary
            if c < grid.cols - 1 and cell.linked(Cell.EAST):
                row.append(' ')
            else:
                row.append('|')

            # Southern boundary
            if r < grid.rows - 1 and cell.linked(Cell.SOUTH):
                eastern_boundary.append('   +')
            else:
                eastern_boundary.append('---+')

        output.append(''.join(row))
        output.append(''.join(eastern_boundary))

    return '\n'.join(output)

def main():
    """Main entry point for the MazeBuilder program."""
    parser = argparse.ArgumentParser(description='Generate and display mazes')
    parser.add_argument('rows', nargs='?', type=int, default=10, help='Number of rows')
    parser.add_argument('cols', nargs='?', type=int, default=10, help='Number of columns')
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder', 'aldous-broder'],
                        default='binary', help='Maze generation algorithm to use')
    parser.add_argument('--solve', action='store_true', help='Display solution path')
    parser.add_argument('--distances', action='store_true', help='Show distances from starting point')
    parser.add_argument('--color', action='store_true', help='Use color in output')
    parser.add_argument('--explain', action='store_true', help='Show explanation of the algorithm')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible maze generation')
    args = parser.parse_args()

    # Create grid
    grid = Grid(args.rows, args.cols)

    # Apply selected maze generation algorithm
    seed_info = f" (seed: {args.seed})" if args.seed is not None else ""

    if args.algorithm == 'binary':
        print(f"Generating maze using Binary Tree algorithm ({args.rows}x{args.cols}){seed_info}...")
        # Set the random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
        BinaryTreeMaze.on(grid)
        if args.explain:
            print("\nBinary Tree Algorithm:")
            print(BinaryTreeMaze.explain())
    elif args.algorithm == 'sidewinder':
        print(f"Generating maze using Sidewinder algorithm ({args.rows}x{args.cols}){seed_info}...")
        # Set the random seed if provided
        if args.seed is not None:
            random.seed(args.seed)
        SidewinderMaze.on(grid)
        if args.explain:
            print("\nSidewinder Algorithm:")
            print(SidewinderMaze.explain())
    elif args.algorithm == 'aldous-broder':
        print(f"Generating maze using Aldous-Broder algorithm ({args.rows}x{args.cols}){seed_info}...")
        print("(This may take longer than other algorithms, especially for larger mazes...)")
        grid, iterations = AldousBroderMaze.on(grid, seed=args.seed)
        print(f"Completed in {iterations} iterations.")
        if args.explain:
            print("\nAldous-Broder Algorithm:")
            print(AldousBroderMaze.explain())

    # Always display the basic maze first
    print("\nGenerated Maze:")
    print(grid.display())
    print()

    if args.solve:
        # Define entrance and exit
        entrance = grid.at(grid.rows-1, 0)  # Bottom left
        exit = grid.at(0, grid.cols-1)      # Top right

        # Find the path from entrance to exit
        solution = Dijkstra.shortest_path(grid, entrance, exit)

        if solution:
            # Calculate distances from the exit to show in each cell
            distances = Dijkstra.calculate_distances(grid, exit)

            print(f"Maze Solution (from entrance at bottom left to exit at top right):")
            print(display_with_path(
                grid,
                solution,
                show_distances=True,  # Always show distances
                distances=distances,
                use_color=args.color
            ))
            print()

            print(f"Solution path length: {len(solution)} cells")
            print(f"Solution path steps: {len(solution) - 1} steps")
            print(f"Path: Entrance ({entrance.row},{entrance.col}) to Exit ({exit.row},{exit.col})")
        else:
            print("No solution path found!")

if __name__ == "__main__":
    main()
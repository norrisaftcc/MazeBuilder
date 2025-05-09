import sys
import argparse
import os
import platform

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cell import Cell
from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
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
    # Disable colors on Windows unless running in a modern terminal
    if platform.system() == "Windows" and "TERM" not in os.environ:
        use_color = False

    # ANSI color codes
    if use_color:
        RESET = "\033[0m"
        GREEN_BG = "\033[42m"
        GREEN_TEXT = "\033[32m"
        CYAN_TEXT = "\033[36m"
    else:
        RESET = ""
        GREEN_BG = ""
        GREEN_TEXT = ""
        CYAN_TEXT = ""

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
            if is_on_path(r, c):
                # Path cell with optional distance
                if show_distances and distances:
                    dist = distances.get_distance(cell)
                    if dist < 10:
                        content = f"{GREEN_TEXT} {dist} {RESET}"
                    else:
                        content = f"{GREEN_TEXT}{dist}{RESET} "
                else:
                    content = f"{GREEN_TEXT} X {RESET}"
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
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder'], default='binary',
                        help='Maze generation algorithm to use')
    parser.add_argument('--solve', action='store_true', help='Display solution path')
    parser.add_argument('--distances', action='store_true', help='Show distances from starting point')
    parser.add_argument('--color', action='store_true', help='Use color in output')
    parser.add_argument('--explain', action='store_true', help='Show explanation of the algorithm')
    args = parser.parse_args()

    # Create grid
    grid = Grid(args.rows, args.cols)

    # Apply selected maze generation algorithm
    if args.algorithm == 'binary':
        print(f"Generating maze using Binary Tree algorithm ({args.rows}x{args.cols})...")
        BinaryTreeMaze.on(grid)
        if args.explain:
            print("\nBinary Tree Algorithm:")
            print("This algorithm connects each cell to either north or east (chosen randomly).")
            print("It creates a distinctive bias toward the northeast corner.")
            print("All northern and eastern corridors are straight lines.")
    else:  # sidewinder
        print(f"Generating maze using Sidewinder algorithm ({args.rows}x{args.cols})...")
        SidewinderMaze.on(grid)
        if args.explain:
            print("\nSidewinder Algorithm:")
            print(SidewinderMaze.explain())

    # Always display the basic maze first
    print("\nGenerated Maze:")
    print(grid.display())
    print()

    if args.solve:
        # Find the longest path through the maze (the true "solution")
        solution = Dijkstra.longest_path(grid)

        # If we want to show a path from top-left to bottom-right instead, use:
        # start = grid.at(0, 0)
        # end = grid.at(grid.rows-1, grid.cols-1)
        # solution = Dijkstra.shortest_path(grid, start, end)

        if solution:
            # Calculate distances from the goal
            start_cell = solution[0]
            distances = Dijkstra.calculate_distances(grid, start_cell)

            print("Maze Solution:")
            print(display_with_path(
                grid,
                solution,
                show_distances=args.distances,
                distances=distances,
                use_color=args.color
            ))
            print()

            print(f"Solution path length: {len(solution)} cells")
            print(f"Solution path steps: {len(solution) - 1} steps")

            # Show path endpoints
            end_cell = solution[-1]
            print(f"Longest path: ({start_cell.row},{start_cell.col}) to ({end_cell.row},{end_cell.col})")
        else:
            print("No solution path found!")

if __name__ == "__main__":
    main()
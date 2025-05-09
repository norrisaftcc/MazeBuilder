import sys
import argparse
from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from pathfinding.dijkstra import Dijkstra

def display_with_path(grid, path):
    """Display the maze with a highlighted solution path."""
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
            
            # Cell contents - mark path cells with 'X'
            if is_on_path(r, c):
                row.append(' X ')
            else:
                row.append('   ')
            
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
    parser.add_argument('--solve', action='store_true', help='Display solution path')
    args = parser.parse_args()
    
    # Create grid and generate maze
    grid = Grid(args.rows, args.cols)
    BinaryTreeMaze.on(grid)
    
    print("Generated Maze:")
    print(grid.display())
    print()
    
    if args.solve:
        # Find and display the solution path
        solution = Dijkstra.longest_path(grid)
        
        print("Maze Solution:")
        print(display_with_path(grid, solution))
        print()
        
        print(f"Solution path length: {len(solution)} cells")
        print(f"Solution path steps: {len(solution) - 1} steps")

if __name__ == "__main__":
    main()
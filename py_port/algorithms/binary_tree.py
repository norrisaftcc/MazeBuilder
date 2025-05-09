import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell

class BinaryTreeMaze:
    """
    Binary Tree maze generation algorithm.
    
    For each cell in the grid, this algorithm randomly carves a passage either
    north or east. If the cell is on the north edge, it always carves east.
    If the cell is on the east edge, it always carves north. If the cell is in
    the northeast corner, it doesn't carve any passages.
    
    This creates a "perfect maze" (one with exactly one path between any two
    cells) with a bias toward the northeast corner.
    """
    
    @staticmethod
    def on(grid):
        """Apply the Binary Tree algorithm to the given grid."""
        for r in range(grid.rows):
            for c in range(grid.cols):
                neighbors = []
                
                # Consider linking north
                if r > 0:
                    neighbors.append(Cell.NORTH)
                
                # Consider linking east
                if c < grid.cols - 1:
                    neighbors.append(Cell.EAST)
                
                # If we have neighbors to link, choose one at random
                if neighbors:
                    direction = neighbors[grid.random_int(0, len(neighbors) - 1)]
                    grid.link_cells(r, c, direction)
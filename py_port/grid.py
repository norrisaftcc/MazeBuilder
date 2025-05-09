import random
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cell import Cell

class Grid:
    """
    Grid represents the maze as a collection of cells in a 2D grid.
    """
    # Direction offsets (row, col)
    DIRECTION_OFFSETS = {
        Cell.NORTH: (0, -1),
        Cell.SOUTH: (0, 1),
        Cell.EAST: (1, 0),
        Cell.WEST: (-1, 0)
    }
    
    def __init__(self, rows, cols):
        """Initialize a new grid with the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.cells = self._initialize_cells()
    
    def _initialize_cells(self):
        """Create and configure cells for the grid."""
        # Create cells
        cells = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        return cells
    
    def is_valid(self, row, col):
        """Check if the given row and column are within the grid bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def at(self, row, col):
        """Get the cell at the given row and column."""
        if not self.is_valid(row, col):
            raise IndexError(f"Cell position ({row}, {col}) is outside the grid")
        return self.cells[row][col]
    
    def random_int(self, min_val, max_val):
        """Generate a random integer between min_val and max_val (inclusive)."""
        return random.randint(min_val, max_val)
    
    def link_cells(self, row1, col1, direction):
        """Link the cell at (row1, col1) to its neighbor in the given direction."""
        if not self.is_valid(row1, col1):
            return
            
        row_offset, col_offset = Grid.DIRECTION_OFFSETS[direction]
        row2 = row1 + row_offset
        col2 = col1 + col_offset
        
        if not self.is_valid(row2, col2):
            return
            
        # Link both cells
        self.at(row1, col1).link(direction)
        self.at(row2, col2).link(Cell.OPPOSITES[direction])
    
    def display(self):
        """Display the maze as ASCII art."""
        # Display the top border
        output = ['+' + '---+' * self.cols]
        
        for r in range(self.rows):
            # Display cell contents and eastern boundaries
            row = ['|']
            eastern_boundary = ['+']
            
            for c in range(self.cols):
                cell = self.at(r, c)
                
                # Cell contents (3 spaces)
                row.append('   ')
                
                # Eastern boundary
                if c < self.cols - 1 and cell.linked(Cell.EAST):
                    row.append(' ')
                else:
                    row.append('|')
                
                # Southern boundary
                if r < self.rows - 1 and cell.linked(Cell.SOUTH):
                    eastern_boundary.append('   +')
                else:
                    eastern_boundary.append('---+')
            
            output.append(''.join(row))
            output.append(''.join(eastern_boundary))
        
        return '\n'.join(output)
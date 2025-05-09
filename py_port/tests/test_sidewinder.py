import sys
import os
import pytest
from unittest.mock import patch

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.sidewinder import SidewinderMaze
from grid import Grid
from cell import Cell

class TestSidewinderMaze:
    """
    Tests for the Sidewinder maze generation algorithm.
    These tests verify that the algorithm creates valid mazes with the expected
    characteristics of Sidewinder mazes.
    """
    
    def test_northern_row_connected(self):
        """Test that all cells in the northern row are connected."""
        grid = Grid(5, 5)
        SidewinderMaze.on(grid)
        
        # The northern row should be one continuous passage from west to east
        for c in range(grid.cols - 1):
            assert grid.at(0, c).linked(Cell.EAST) is True
    
    def test_vertical_connections(self):
        """Test that vertical connections are created (except in top row)."""
        grid = Grid(10, 10)

        # Mock random choice to always create north links (end runs immediately)
        with patch('grid.Grid.random_int', return_value=0):
            SidewinderMaze.on(grid)
            
            # Check that each cell in rows 1+ (except the northernmost) has a north link
            north_links_count = 0
            for r in range(1, grid.rows):
                for c in range(grid.cols):
                    if grid.at(r, c).linked(Cell.NORTH):
                        north_links_count += 1
            
            # There should be vertical connections in a 10x10 grid
            assert north_links_count > 0
            
            # In this special case (always end runs), each cell should link north
            # except the northern row
            expected_north_links = grid.rows * grid.cols - grid.cols  # Total cells - northern row
            assert north_links_count == expected_north_links
    
    def test_horizontal_runs(self):
        """Test that horizontal runs are created when random choice favors east connections."""
        grid = Grid(10, 10)

        # First mock call returns 1 (continue run), second returns 0 (end run)
        # This creates runs of length 2
        call_count = 0
        def alternating_random(*args):
            nonlocal call_count
            call_count += 1
            return call_count % 2  # Returns 1, 0, 1, 0, ...

        with patch('grid.Grid.random_int', side_effect=alternating_random):
            SidewinderMaze.on(grid)
            
            # Count horizontal connections
            east_links_count = 0
            for r in range(grid.rows):
                for c in range(grid.cols - 1):  # Exclude rightmost column
                    if grid.at(r, c).linked(Cell.EAST):
                        east_links_count += 1
            
            # There should be horizontal connections
            assert east_links_count > 0
            
            # Verify the pattern in bottom rows (not the northern row)
            # With our alternating mock, every other cell should connect east
            # This is a simplified check for demonstration purposes
            assert east_links_count > grid.cols - 1  # More than just the northern row
    
    def test_is_connected_maze(self):
        """Test that the maze is fully connected (all cells can reach all others)."""
        grid = Grid(5, 5)
        SidewinderMaze.on(grid)
        
        # We can verify connectivity by checking that from any starting point,
        # we can reach all cells. We'll use a simple breadth-first search.
        
        start = grid.at(0, 0)
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            current_key = f"{current.row},{current.col}"
            
            if current_key in visited:
                continue
                
            visited.add(current_key)
            
            # Add all linked neighbors to the queue
            for direction in current.get_links():
                r, c = current.row, current.col
                dr, dc = Grid.DIRECTION_OFFSETS[direction]
                nr, nc = r + dr, c + dc
                
                if grid.is_valid(nr, nc):
                    queue.append(grid.at(nr, nc))
        
        # All cells should be visited in a perfect maze
        assert len(visited) == grid.rows * grid.cols
    
    def test_explain_method(self):
        """Test that the explain method returns a non-empty string."""
        explanation = SidewinderMaze.explain()
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "SIDEWINDER ALGORITHM" in explanation
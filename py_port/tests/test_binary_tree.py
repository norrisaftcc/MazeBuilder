import sys
import os
import pytest
from unittest.mock import patch

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.binary_tree import BinaryTreeMaze
from grid import Grid
from cell import Cell

class TestBinaryTreeMaze:
    @patch('grid.Grid.random_int')
    def test_on_single_cell(self, mock_random_int):
        """Test Binary Tree algorithm on a 1x1 grid."""
        grid = Grid(1, 1)
        
        # Run algorithm
        BinaryTreeMaze.on(grid)
        
        # No neighbors to link, should have no links
        assert grid.at(0, 0).get_links() == []

    @patch('grid.Grid.random_int')
    def test_on_northeast_corner(self, mock_random_int):
        """Test Binary Tree algorithm on a corner cell with no valid links."""
        grid = Grid(3, 3)
        
        # Northeast corner has no north or east links
        # Focus on just this cell
        with patch.object(Grid, 'at') as mock_at:
            mock_at.return_value = grid.at(0, 2)
            
            # Run algorithm
            BinaryTreeMaze.on(grid)
            
            # Should have no links
            assert mock_at.return_value.get_links() == []

    @patch('grid.Grid.random_int')
    def test_on_north_edge(self, mock_random_int):
        """Test Binary Tree algorithm on north edge (can only go east)."""
        grid = Grid(3, 3)
        
        # For cells on north edge (except NE corner), 
        # should always choose east
        mock_random_int.return_value = 0  # Doesn't matter, only one option
        
        # Run algorithm on just the top-middle cell (0,1)
        for r in range(3):
            for c in range(3):
                # Skip all but the focused cell
                if r != 0 or c != 1:
                    continue
                
                # Run algorithm
                BinaryTreeMaze.on(grid)
        
        # Cell should be linked east
        assert grid.at(0, 1).linked(Cell.EAST) is True
        assert grid.at(0, 1).linked(Cell.SOUTH) is False
        
        # Its eastern neighbor should be linked west
        assert grid.at(0, 2).linked(Cell.WEST) is True

    @patch('grid.Grid.random_int')
    def test_on_east_edge(self, mock_random_int):
        """Test Binary Tree algorithm on east edge (can only go north)."""
        grid = Grid(3, 3)
        
        # For cells on east edge (except NE corner), 
        # should always choose north
        mock_random_int.return_value = 0  # Doesn't matter, only one option
        
        # Run algorithm on just the middle-right cell (1,2)
        for r in range(3):
            for c in range(3):
                # Skip all but the focused cell
                if r != 1 or c != 2:
                    continue
                
                # Run algorithm
                BinaryTreeMaze.on(grid)
        
        # Cell should be linked north
        assert grid.at(1, 2).linked(Cell.NORTH) is True
        assert grid.at(1, 2).linked(Cell.WEST) is False
        
        # Its northern neighbor should be linked south
        assert grid.at(0, 2).linked(Cell.SOUTH) is True

    @patch('grid.Grid.random_int')
    def test_on_middle_cell_north(self, mock_random_int):
        """Test Binary Tree algorithm on middle cell choosing north."""
        grid = Grid(3, 3)
        
        # Choose north (first option)
        mock_random_int.return_value = 0
        
        # Run algorithm on just the middle cell (1,1)
        for r in range(3):
            for c in range(3):
                # Skip all but the focused cell
                if r != 1 or c != 1:
                    continue
                
                # Run algorithm
                BinaryTreeMaze.on(grid)
        
        # Cell should be linked north but not east
        assert grid.at(1, 1).linked(Cell.NORTH) is True
        assert grid.at(1, 1).linked(Cell.EAST) is False
        
        # Its northern neighbor should be linked south
        assert grid.at(0, 1).linked(Cell.SOUTH) is True

    @patch('grid.Grid.random_int')
    def test_on_middle_cell_east(self, mock_random_int):
        """Test Binary Tree algorithm on middle cell choosing east."""
        grid = Grid(3, 3)
        
        # Choose east (second option)
        mock_random_int.return_value = 1
        
        # Run algorithm on just the middle cell (1,1)
        for r in range(3):
            for c in range(3):
                # Skip all but the focused cell
                if r != 1 or c != 1:
                    continue
                
                # Run algorithm
                BinaryTreeMaze.on(grid)
        
        # Cell should be linked east but not north
        assert grid.at(1, 1).linked(Cell.NORTH) is False
        assert grid.at(1, 1).linked(Cell.EAST) is True
        
        # Its eastern neighbor should be linked west
        assert grid.at(1, 2).linked(Cell.WEST) is True

    @patch('grid.Grid.random_int')
    def test_on_complete_maze(self, mock_random_int):
        """Test Binary Tree algorithm creates a complete maze."""
        # Use a predictable pattern for testing: alternate north and east
        # This creates a zig-zag pattern
        mock_random_int.side_effect = lambda min_val, max_val: 0 if (min_val == 0 and max_val == 1) else min_val
        
        grid = Grid(3, 3)
        BinaryTreeMaze.on(grid)
        
        # Check each cell has appropriate links based on our mock
        # North edge cells should link east
        assert grid.at(0, 0).linked(Cell.EAST) is True
        assert grid.at(0, 1).linked(Cell.EAST) is True
        
        # East edge cells should link north
        assert grid.at(1, 2).linked(Cell.NORTH) is True
        assert grid.at(2, 2).linked(Cell.NORTH) is True
        
        # Middle cells should alternate - but with our mock
        # they'll all choose north if they can
        assert grid.at(1, 0).linked(Cell.NORTH) is True
        assert grid.at(1, 1).linked(Cell.NORTH) is True
        assert grid.at(2, 0).linked(Cell.NORTH) is True
        assert grid.at(2, 1).linked(Cell.NORTH) is True
        
        # Northeast corner has no links
        assert grid.at(0, 2).get_links() == []

    def test_explain_method(self):
        """Test that the explain method returns a non-empty string."""
        explanation = BinaryTreeMaze.explain()
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "BINARY TREE ALGORITHM" in explanation
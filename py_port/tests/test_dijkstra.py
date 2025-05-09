import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathfinding.dijkstra import Dijkstra
from pathfinding.distances import Distances
from grid import Grid
from cell import Cell

class TestDijkstra:
    def setup_method(self):
        """Create a simple 3x3 grid for testing."""
        self.grid = Grid(3, 3)
        
        # Create a simple path through the maze:
        # (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (2,1) -> (2,0)
        # +---+---+---+
        # |       |   |
        # +---+   +   +
        # |   |       |
        # +   +---+   +
        # |       |   |
        # +---+---+---+
        
        # Horizontal connections
        self.grid.link_cells(0, 0, Cell.EAST)  # (0,0) -> (0,1)
        self.grid.link_cells(0, 1, Cell.EAST)  # (0,1) -> (0,2)
        self.grid.link_cells(2, 0, Cell.EAST)  # (2,0) -> (2,1)
        
        # Vertical connections
        self.grid.link_cells(0, 2, Cell.SOUTH)  # (0,2) -> (1,2)
        self.grid.link_cells(1, 2, Cell.SOUTH)  # (1,2) -> (2,2)
        self.grid.link_cells(2, 1, Cell.WEST)   # (2,1) -> (2,0)

    def test_calculate_distances(self):
        """Test Dijkstra's distance calculations."""
        # Calculate distances from top-left
        start = self.grid.at(0, 0)
        distances = Dijkstra.calculate_distances(self.grid, start)
        
        # Check distances to several cells
        assert distances.get_distance(self.grid.at(0, 0)) == 0  # Start cell
        assert distances.get_distance(self.grid.at(0, 1)) == 1  # One step east
        assert distances.get_distance(self.grid.at(0, 2)) == 2  # Two steps east
        assert distances.get_distance(self.grid.at(1, 2)) == 3  # Down from (0,2)
        assert distances.get_distance(self.grid.at(2, 2)) == 4  # Down from (1,2)
        assert distances.get_distance(self.grid.at(2, 1)) == 5  # Left from (2,2)
        assert distances.get_distance(self.grid.at(2, 0)) == 6  # Left from (2,1)
        
        # Cells not reachable in our contrived maze
        assert distances.get_distance(self.grid.at(1, 0)) == sys.maxsize
        assert distances.get_distance(self.grid.at(1, 1)) == sys.maxsize

    def test_shortest_path(self):
        """Test finding shortest path between two cells."""
        start = self.grid.at(0, 0)
        end = self.grid.at(2, 0)
        
        path = Dijkstra.shortest_path(self.grid, start, end)
        
        # Check path length
        assert len(path) == 7  # 7 cells including start and end
        
        # Check path cells
        assert path[0] == start
        assert path[1] == self.grid.at(0, 1)
        assert path[2] == self.grid.at(0, 2)
        assert path[3] == self.grid.at(1, 2)
        assert path[4] == self.grid.at(2, 2)
        assert path[5] == self.grid.at(2, 1)
        assert path[6] == end
        
        # Test path between cells with no connection
        unreachable = self.grid.at(1, 1)  # This cell has no connections
        empty_path = Dijkstra.shortest_path(self.grid, start, unreachable)
        assert len(empty_path) == 0  # No path exists

    def test_longest_path(self):
        """Test finding the longest path (solution) in the maze."""
        # In our contrived example, the longest path is known:
        # (0,0) to (2,0) or vice versa
        path = Dijkstra.longest_path(self.grid)
        
        # Check path length
        assert len(path) == 7  # 7 cells
        
        # Check path endpoints
        assert (path[0] == self.grid.at(0, 0) and path[-1] == self.grid.at(2, 0)) or \
               (path[0] == self.grid.at(2, 0) and path[-1] == self.grid.at(0, 0))
        
        # Create a new 2x2 grid with different pattern to test algorithm more thoroughly
        small_grid = Grid(2, 2)
        small_grid.link_cells(0, 0, Cell.EAST)
        small_grid.link_cells(0, 0, Cell.SOUTH)
        small_grid.link_cells(1, 0, Cell.EAST)
        
        # Longest path should be (0,0) to (1,1) or vice versa
        small_path = Dijkstra.longest_path(small_grid)
        
        # Check path endpoints
        assert (small_path[0] == small_grid.at(0, 0) and small_path[-1] == small_grid.at(1, 1)) or \
               (small_path[0] == small_grid.at(1, 1) and small_path[-1] == small_grid.at(0, 0))
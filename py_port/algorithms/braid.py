import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell
from grid import Grid


class Braid:
    """
    Braiding: turn a perfect maze into one with loops.

    A perfect maze has exactly one path between any two cells, and every
    wall-following rule (keep one hand on the wall) is sure to find the way
    out. Braiding visits each dead end and, with probability p, knocks out
    one of its walls to join a neighbour. Each knocked-out wall makes a loop.
    With loops, a wall follower can circle forever, and the general way to
    find the exit is a search with memory (breadth-first or depth-first).

    Neighbours that are themselves dead ends are joined first, which turns two
    dead ends into one corridor rather than leaving a stub.

    All randomness goes through grid.random_int, so a grid with seeded dice
    braids the same way every time.

    Time complexity: O(n) where n is the number of cells in the grid
    Space complexity: O(1)
    """

    @staticmethod
    def dead_ends(grid):
        """Every cell with exactly one link, in row-major order."""
        return [grid.at(r, c) for r in range(grid.rows) for c in range(grid.cols)
                if len(grid.at(r, c).get_links()) == 1]

    @staticmethod
    def on(grid, p=1.0):
        """
        Braid the grid in place. p is the chance (0.0 to 1.0) that a dead end
        is joined to a neighbour. Returns the number of walls knocked out.
        """
        if not 0.0 <= p <= 1.0:
            raise ValueError("p must be between 0.0 and 1.0")
        knocked = 0
        for cell in Braid.dead_ends(grid):
            # The list is taken once; a cell joined by an earlier neighbour is no longer a dead end.
            if len(cell.get_links()) != 1:
                continue
            if p < 1.0 and grid.random_int(1, 100) > int(round(p * 100)):
                continue
            unlinked = []
            for direction, (dr, dc) in Grid.DIRECTION_OFFSETS.items():
                r, c = cell.row + dr, cell.col + dc
                if grid.is_valid(r, c) and not cell.linked(direction):
                    unlinked.append((direction, grid.at(r, c)))
            if not unlinked:
                continue
            best = [pair for pair in unlinked if len(pair[1].get_links()) == 1] or unlinked
            direction, _ = best[grid.random_int(0, len(best) - 1)]
            grid.link_cells(cell.row, cell.col, direction)
            knocked += 1
        return knocked

    @staticmethod
    def explain():
        return """
        Braiding removes dead ends from a finished maze. For each dead end it
        picks a wall and knocks it out, joining the cell to a neighbour. Every
        wall removed adds a loop, so the maze stops being "perfect": there is
        now more than one way between some pairs of cells.

        Why it matters:
        - Wall following (the left-hand rule) solves every perfect maze. In a
          braided maze it can go round a loop forever.
        - Finding the way then needs memory: breadth-first search, depth-first
          search with backtracking, or a map.
        - Dead ends are what make a maze feel like a maze; braiding trades
          them for choice.

        The parameter p is the fraction of dead ends to remove. p = 1.0 leaves
        none; p = 0.5 removes about half.
        """

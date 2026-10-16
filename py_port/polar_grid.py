"""A polar grid: rings and spokes, growing outward from a well.

Rows are rings; row 0 is the innermost ring, around a well that is not a cell.
Columns are spokes, and the column index wraps: the cell sunwise of the last
spoke is the first. So every ring is a circle, and the grid is a disc with a
hole in the middle.

The four directions keep Cell's names, read round:

    NORTH  inward, toward the well       SOUTH  outward, toward the rim
    EAST   sunwise (clockwise)           WEST   widdershins (anticlockwise)

Every ring has the same number of cells. A true polar grid doubles its cell
count as the rings widen, but then a cell may have two outward neighbours,
which Cell's four flags cannot say. Equal spokes keep the cell, and keep every
algorithm working unchanged.

The seam. Binary Tree and Sidewinder treat the last column as an edge: they
never link it east. On a polar grid that leaves one wall running from the well
to the rim, along one spoke, and it keeps their mazes perfect. (A ring whose
every cell linked sunwise would be a loop.) Aldous-Broder and Braid use
is_valid, which wraps, so their mazes can cross the seam.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cell import Cell  # noqa: E402
from grid import Grid  # noqa: E402


class PolarGrid(Grid):
    """A Grid whose columns wrap. rows are rings, cols are spokes."""

    def __init__(self, rings, spokes):
        if rings < 1 or spokes < 3:
            raise ValueError("a polar grid needs at least one ring and three spokes")
        super().__init__(rings, spokes)

    @property
    def rings(self):
        return self.rows

    @property
    def spokes(self):
        return self.cols

    def is_valid(self, row, col):
        """Any column is valid on a valid ring: the ring goes all the way round."""
        return 0 <= row < self.rows

    def at(self, row, col):
        if not 0 <= row < self.rows:
            raise IndexError(f"Ring {row} is outside the grid")
        return self.cells[row][col % self.cols]

    def link_cells(self, row1, col1, direction):
        if not self.is_valid(row1, col1):
            return
        row_offset, col_offset = Grid.DIRECTION_OFFSETS[direction]
        row2, col2 = row1 + row_offset, col1 + col_offset
        if not self.is_valid(row2, col2):
            return
        self.at(row1, col1).link(direction)
        self.at(row2, col2).link(Cell.OPPOSITES[direction])

    def display(self):
        """The grid unrolled: inward is up, sunwise is right, and the two ends join.

        A ':' instead of '|' at either end marks the seam, where the last column
        meets the first. The well is the top edge."""
        out = ["  inward (the well)"]
        out.append("+" + "---+" * self.cols)
        for r in range(self.rows):
            row, below = [], ["+"]
            first = self.at(r, 0)
            row.append(" " if first.linked(Cell.WEST) else ":")
            for c in range(self.cols):
                cell = self.at(r, c)
                row.append("   ")
                if c < self.cols - 1:
                    row.append(" " if cell.linked(Cell.EAST) else "|")
                else:
                    row.append(" " if cell.linked(Cell.EAST) else ":")
                below.append("   +" if r < self.rows - 1 and cell.linked(Cell.SOUTH) else "---+")
            out.append("".join(row))
            out.append("".join(below))
        out.append("  outward (the rim); the ':' ends join")
        return "\n".join(out)

    def to_dict(self):
        data = super().to_dict()
        data["polar"] = True
        return data

    @classmethod
    def from_dict(cls, data):
        grid = cls(data["rows"], data["cols"])
        for r in range(grid.rows):
            for c in range(grid.cols):
                grid.at(r, c).links = data["cells"][r][c]["links"]
        return grid

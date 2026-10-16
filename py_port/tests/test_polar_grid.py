"""Tests for the polar grid: rings and spokes, a wrapping column, a seam."""

import os
import random
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.aldous_broder import AldousBroderMaze  # noqa: E402
from algorithms.binary_tree import BinaryTreeMaze  # noqa: E402
from algorithms.braid import Braid  # noqa: E402
from algorithms.sidewinder import SidewinderMaze  # noqa: E402
from cell import Cell  # noqa: E402
from grid import Grid  # noqa: E402
from pathfinding.dijkstra import Dijkstra  # noqa: E402
from polar_grid import PolarGrid  # noqa: E402

ALGORITHMS = {
    "binary": BinaryTreeMaze.on,
    "sidewinder": SidewinderMaze.on,
    "aldous-broder": lambda g: AldousBroderMaze.on(g)[0],
}


def links(grid):
    return sum(len(grid.at(r, c).get_links()) for r in range(grid.rows) for c in range(grid.cols)) // 2


def reached(grid):
    return len(Dijkstra.calculate_distances(grid, grid.at(0, 0)).cells)


def test_the_column_wraps():
    g = PolarGrid(3, 8)
    assert g.at(1, 8) is g.at(1, 0) and g.at(1, -1) is g.at(1, 7)
    assert g.is_valid(1, 99) and not g.is_valid(3, 0) and not g.is_valid(-1, 0)
    g.link_cells(1, 7, Cell.EAST)
    assert g.at(1, 7).linked(Cell.EAST) and g.at(1, 0).linked(Cell.WEST)
    g.link_cells(0, 0, Cell.NORTH)  # no ring inward of the first: nothing happens
    assert not g.at(0, 0).linked(Cell.NORTH)
    assert g.rings == 3 and g.spokes == 8


def test_too_small():
    with pytest.raises(ValueError):
        PolarGrid(0, 8)
    with pytest.raises(ValueError):
        PolarGrid(3, 2)


@pytest.mark.parametrize("name", sorted(ALGORITHMS))
def test_every_algorithm_grows_a_perfect_polar_maze(name):
    random.seed(7)
    g = PolarGrid(6, 12)
    ALGORITHMS[name](g)
    assert links(g) == g.rows * g.cols - 1   # a tree
    assert reached(g) == g.rows * g.cols     # one tree


@pytest.mark.parametrize("name", ["binary", "sidewinder"])
def test_binary_tree_and_sidewinder_keep_the_seam(name):
    random.seed(7)
    g = PolarGrid(6, 12)
    ALGORITHMS[name](g)
    assert not any(g.at(r, g.cols - 1).linked(Cell.EAST) for r in range(g.rows))
    if name == "binary":
        # Inward or sunwise from anywhere reaches the innermost ring at the seam.
        for r in range(g.rows):
            for c in range(g.cols):
                cell = g.at(r, c)
                assert (r, c) == (0, g.cols - 1) or cell.linked(Cell.NORTH) or cell.linked(Cell.EAST)
    else:
        # The innermost ring is one walk round the well, broken only at the seam.
        assert all(g.at(0, c).linked(Cell.EAST) for c in range(g.cols - 1))


def test_aldous_broder_and_braid_cross_the_seam():
    crossed = 0
    for seed in range(10):
        random.seed(seed)
        g = PolarGrid(5, 8)
        AldousBroderMaze.on(g)
        crossed += sum(1 for r in range(g.rows) if g.at(r, g.cols - 1).linked(Cell.EAST))
    assert crossed > 0
    random.seed(7)
    g = PolarGrid(5, 8)
    SidewinderMaze.on(g)
    Braid.on(g, 1.0)
    assert Braid.dead_ends(g) == [] and reached(g) == g.rows * g.cols


def test_aldous_broder_on_a_square_grid_is_unchanged():
    # The wrap fix keys visited cells by the cell's own coordinates. On a square grid
    # those are the coordinates it always used, so the same seed grows the same maze.
    random.seed(11)
    a = Grid(6, 6)
    AldousBroderMaze.on(a)
    assert links(a) == 35 and reached(a) == 36


def test_display_and_dict_round_trip():
    random.seed(3)
    g = PolarGrid(3, 6)
    SidewinderMaze.on(g)
    text = g.display()
    assert text.startswith("  inward (the well)") and ":" in text and "join" in text
    again = PolarGrid.from_dict(g.to_dict())
    assert g.to_dict()["polar"] is True and again.display() == text

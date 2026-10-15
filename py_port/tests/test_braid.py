"""Tests for braiding: turning a perfect maze into one with loops."""

import os
import random
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.braid import Braid  # noqa: E402
from algorithms.sidewinder import SidewinderMaze  # noqa: E402
from algorithms.aldous_broder import AldousBroderMaze  # noqa: E402
from grid import Grid  # noqa: E402
from pathfinding.dijkstra import Dijkstra  # noqa: E402


def perfect(seed=7, rows=8, cols=8):
    random.seed(seed)
    grid = Grid(rows, cols)
    SidewinderMaze.on(grid)
    return grid


def links(grid):
    return sum(len(grid.at(r, c).get_links()) for r in range(grid.rows) for c in range(grid.cols)) // 2


def test_a_perfect_maze_is_a_tree():
    grid = perfect()
    assert links(grid) == grid.rows * grid.cols - 1
    assert len(Braid.dead_ends(grid)) > 0


def test_full_braid_leaves_no_dead_ends_and_adds_loops():
    grid = perfect()
    before = links(grid)
    knocked = Braid.on(grid, 1.0)
    assert knocked > 0
    assert Braid.dead_ends(grid) == []
    assert links(grid) == before + knocked  # every knocked wall is one more link, so one more loop


def test_half_braid_removes_about_half():
    totals = []
    for seed in range(20):
        grid = perfect(seed)
        dead = len(Braid.dead_ends(grid))
        random.seed(seed)
        Braid.on(grid, 0.5)
        totals.append((dead, len(Braid.dead_ends(grid))))
    removed = sum(d - left for d, left in totals)
    dead = sum(d for d, _ in totals)
    assert 0.3 * dead < removed < 0.7 * dead


def test_zero_braid_changes_nothing():
    grid = perfect()
    before = grid.display()
    assert Braid.on(grid, 0.0) == 0
    assert grid.display() == before


def test_bad_p_is_refused():
    with pytest.raises(ValueError):
        Braid.on(perfect(), 1.5)


def test_braid_is_deterministic_through_the_grid_dice():
    a, b = perfect(3), perfect(3)
    random.seed(11)
    Braid.on(a, 0.5)
    random.seed(11)
    Braid.on(b, 0.5)
    assert a.display() == b.display()


def test_every_cell_is_still_reachable():
    grid = perfect(5)
    Braid.on(grid, 1.0)
    d = Dijkstra.calculate_distances(grid, grid.at(0, 0))
    assert all(d.get_distance(grid.at(r, c)) < sys.maxsize for r in range(grid.rows) for c in range(grid.cols))


def test_braid_prefers_joining_dead_ends_to_each_other():
    # Two dead ends side by side: the braid joins them to each other, not to a corridor.
    grid = Grid(1, 4)
    grid.link_cells(0, 0, 4)  # (0,0)-(0,1)   Cell.EAST == 4
    grid.link_cells(0, 2, 4)  # (0,2)-(0,3)
    # (0,1) and (0,2) are dead ends facing each other; (0,0) and (0,3) are dead ends at the edges.
    Braid.on(grid, 1.0)
    assert grid.at(0, 1).linked(4)  # joined across the middle
    # The two end cells of a one-row grid have no other neighbour, so they stay dead ends.
    assert [(c.row, c.col) for c in Braid.dead_ends(grid)] == [(0, 0), (0, 3)]


def test_works_on_any_perfect_maze():
    grid = Grid(6, 6)
    AldousBroderMaze.on(grid, seed=2)
    Braid.on(grid, 1.0)
    assert Braid.dead_ends(grid) == []

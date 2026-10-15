"""Tests for export_crawler: the maze-to-Crawler-pack exporter."""

import json
import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import export_crawler as ec  # noqa: E402
from cell import Cell  # noqa: E402


@pytest.fixture
def pack(tmp_path):
    out = str(tmp_path / "hedge")
    grid, p = ec.export(6, 7, "sidewinder", 11, out, fights=2)
    files = {}
    for name in ["pack", "events", "encounters", "endings", "hub"] + ec.BASE_FILES:
        with open(os.path.join(out, name + ".json")) as f:
            files[name] = json.load(f)
    with open(os.path.join(out, "maps", "hedge.json")) as f:
        files["map"] = json.load(f)
    with open(os.path.join(out, "replay.json")) as f:
        files["replay"] = json.load(f)
    return grid, p, files


def test_grid_shape_and_walls(pack):
    grid, p, files = pack
    g = files["map"]["grid"]
    assert len(g) == 2 * grid.rows + 1
    assert all(len(row) == 2 * grid.cols + 1 for row in g)
    assert set(g[0]) == {"#"} and set(g[-1]) == {"#"}
    assert all(row[0] == "#" and row[-1] == "#" for row in g)
    # Every maze cell is a floor square; a wall square between cells means no link.
    for r in range(grid.rows):
        for c in range(grid.cols):
            x, y = 2 * c + 1, 2 * r + 1
            assert g[y][x] != "#"
            if c + 1 < grid.cols:
                assert (g[y][x + 1] != "#") == grid.at(r, c).linked(Cell.EAST)
            if r + 1 < grid.rows:
                assert (g[y + 1][x] != "#") == grid.at(r, c).linked(Cell.SOUTH)


def test_stairs_at_the_ends_of_the_longest_path(pack):
    grid, p, files = pack
    g = files["map"]["grid"]
    ex, ey = ec.square(p["entrance"])
    xx, xy = ec.square(p["exit"])
    assert g[ey][ex] == "<" and g[xy][xx] == ">"
    cells = files["map"]["cells"]
    assert cells[f"{ex},{ey}"]["link"] == {"hub": True}
    assert cells[f"{xx},{xy}"]["link"] == {"scene": "out"}
    # The ends of the longest path are dead ends.
    assert len(p["entrance"].get_links()) == 1
    assert len(p["exit"].get_links()) == 1


def test_every_glyph_is_known(pack):
    grid, p, files = pack
    m = files["map"]
    known = set("#<>") | set(m["legend"])
    assert all(ch in known for row in m["grid"] for ch in row)
    assert set(m["legend"]) == set(m["areas"])
    assert len(m["areas"]) == p["n_bands"] <= len(ec.GLYPHS)


def test_fights_and_treasure_are_in_dead_ends_off_the_path(pack):
    grid, p, files = pack
    on_path = {(c.row, c.col) for c in p["path"]}
    for cell in p["fights"] + [p["treasure"]]:
        assert len(cell.get_links()) == 1
        assert (cell.row, cell.col) not in on_path
    assert len(p["fights"]) == 2
    events, encounters = files["events"], files["encounters"]
    for cell in p["fights"]:
        sid = ec.scene_id(cell)
        assert sid in events
        assert "enc-" + sid in encounters


def test_every_reference_resolves(pack):
    grid, p, files = pack
    m, events, encounters, endings = files["map"], files["events"], files["encounters"], files["endings"]
    for cell in m["cells"].values():
        if "event" in cell:
            assert cell["event"] in events
        if "link" in cell and "scene" in cell["link"]:
            assert cell["link"]["scene"] in events
    for ev in events.values():
        for choice in ev["choices"]:
            goto = choice.get("effects", {}).get("goto", {})
            if "encounter" in goto:
                assert goto["encounter"] in encounters
            if "ending" in goto:
                assert goto["ending"] in endings
    assert files["pack"]["start"]["scene"] in events
    assert files["rules"]["endings"]["wipe"] in endings


def test_replay_walks_the_solution(pack):
    grid, p, files = pack
    commands = files["replay"]["commands"]
    assert files["replay"]["seed"] == 11
    assert commands[0]["t"] == "pick"
    assert commands[-1] == {"t": "choose", "id": "go"}
    moves = [c for c in commands if c["t"] == "move"]
    # Two squares per maze step, from the first cell after the entrance to the exit.
    assert len(moves) == 2 * (len(p["path"]) - 2)
    # Walk the moves on the glyph grid: never into a wall, and end on the exit stair.
    g = files["map"]["grid"]
    x, y = ec.square(p["path"][1])
    facing = ec.FACING[ec.direction_between(p["path"][0], p["path"][1])]
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for c in commands[5:-1]:
        if c["t"] == "turn":
            facing = (facing + {"right": 1, "about": 2, "left": 3}[c["dir"]]) % 4
        else:
            dx, dy = dirs[facing]
            x, y = x + dx, y + dy
            assert g[y][x] != "#"
    assert g[y][x] == ">"


def test_same_seed_same_pack(tmp_path):
    outs = []
    for i in range(2):
        out = str(tmp_path / f"run{i}")
        ec.export(5, 5, "binary", 42, out)
        with open(os.path.join(out, "maps", "hedge.json")) as f:
            outs.append(f.read())
    assert outs[0] == outs[1]


def test_tells_cover_every_algorithm():
    assert set(ec.TELLS) == {"binary", "sidewinder", "aldous-broder"}

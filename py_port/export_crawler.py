"""
Export a maze as a pack for the Crawler.

The Crawler is the first-person party crawler in the games-osr-fort-on-lake
repository (crawler/SPEC.md). A pack is data: a glyph grid, areas, scenes,
monsters. This script builds a maze with one of MazeBuilder's algorithms and
writes a complete pack around it:

- The maze becomes a grid of 10-foot squares: a cell is a floor square, a
  link is a floor square between two cells, everything else is wall.
- Dijkstra's longest path picks the entrance and the exit. The entrance is a
  stair back to town; the exit is a stair out, and an ending.
- Distance bands from the entrance become the Crawler's areas, so the clock
  ticks as the party goes deeper and the wandering monsters get their rolls.
- Dead ends hold fights, and the deepest dead end holds the treasure.
- A plate at the entrance states the algorithm's tell: the rule a player can
  discover by walking. Aldous-Broder has none, and the plate says so.
- replay.json is {seed, commands}: a whole game that walks the solution.
  crawler_walk.mjs plays it against the engine.

The party, items, abilities, monsters, rules and theme come from the
Crawler's test fixture, vendored in crawler_base/.

Usage:
    python export_crawler.py 8 8 --algorithm sidewinder --seed 7 --out out/hedge
    node crawler_walk.mjs <crawler root> out/hedge
"""

import argparse
import json
import math
import os
import random
import shutil
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cell import Cell
from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(HERE, "crawler_base")
BASE_FILES = ["party", "items", "abilities", "bestiary", "rules", "theme"]

# Crawler facings: 0 north, 1 east, 2 south, 3 west. x grows east, y grows south.
FACING = {Cell.NORTH: 0, Cell.EAST: 1, Cell.SOUTH: 2, Cell.WEST: 3}
# Area glyphs. L and S are the Crawler's locked and secret doors, so they are left out.
GLYPHS = "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKMNOPQRTUVWXYZ"
MAX_BANDS = 20  # the fixture party carries about thirty turns of torchlight
MAP_ID = "hedge"

TELLS = {
    "binary": {
        "brush": "The hedge leans. Every square seems to open north, or east, or both.",
        "rule": ("Every square opens north or east. Walk north and east and you reach "
                 "the north-east corner from anywhere. From that corner, one way leads "
                 "down to every square."),
    },
    "sidewinder": {
        "brush": "A long walk runs along the north edge. The rows below are broken into runs.",
        "rule": ("Every row is runs of squares, and every run has one gate north. "
                 "Go up to the long walk, along it, and down. The way down is the only way."),
    },
    "aldous-broder": {
        "brush": "The hedge has no grain. It was grown by something that wandered.",
        "rule": "There is no rule. Every maze of this size was as likely as this one. Map it.",
    },
}


def build_maze(rows, cols, algorithm, seed):
    """Build a maze with the named algorithm. The seed makes it repeatable."""
    grid = Grid(rows, cols)
    if algorithm == "aldous-broder":
        grid, _ = AldousBroderMaze.on(grid, seed=seed)
    else:
        random.seed(seed)
        (BinaryTreeMaze if algorithm == "binary" else SidewinderMaze).on(grid)
    return grid


def neighbour(grid, cell, direction):
    dr, dc = Grid.DIRECTION_OFFSETS[direction]
    return grid.at(cell.row + dr, cell.col + dc)


def direction_between(a, b):
    """The direction from cell a to adjacent cell b."""
    for direction, (dr, dc) in Grid.DIRECTION_OFFSETS.items():
        if (a.row + dr, a.col + dc) == (b.row, b.col):
            return direction
    raise ValueError("cells are not adjacent")


def square(cell):
    """The grid square (x, y) of a maze cell."""
    return 2 * cell.col + 1, 2 * cell.row + 1


def key(x, y):
    return f"{x},{y}"


def plan(grid, algorithm, seed, fights):
    """Decide where everything goes. Returns a dict the writers read."""
    path = Dijkstra.longest_path(grid)
    entrance, exit_ = path[0], path[-1]
    dist = Dijkstra.calculate_distances(grid, entrance)
    cells = [grid.at(r, c) for r in range(grid.rows) for c in range(grid.cols)]
    max_d = max(dist.get_distance(c) for c in cells)
    width = max(1, math.ceil((max_d + 1) / MAX_BANDS))
    band = {(c.row, c.col): dist.get_distance(c) // width for c in cells}
    n_bands = max_d // width + 1

    on_path = {(c.row, c.col) for c in path}
    dead_ends = [c for c in cells
                 if len(c.get_links()) == 1 and (c.row, c.col) not in on_path]
    dead_ends.sort(key=lambda c: -dist.get_distance(c))
    treasure = dead_ends[0] if dead_ends else None
    rest = dead_ends[1:]
    stride = max(1, len(rest) // fights) if fights else 1
    fight_cells = rest[::stride][:fights]

    return {
        "algorithm": algorithm, "seed": seed, "rows": grid.rows, "cols": grid.cols,
        "path": path, "entrance": entrance, "exit": exit_, "dist": dist,
        "band": band, "n_bands": n_bands, "width": width,
        "treasure": treasure, "fights": fight_cells,
    }


def make_grid(grid, p):
    """The glyph grid: one character per 10-foot square."""
    W, H = 2 * grid.cols + 1, 2 * grid.rows + 1
    g = [["#"] * W for _ in range(H)]
    glyph = lambda cell: GLYPHS[p["band"][(cell.row, cell.col)]]
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.at(r, c)
            x, y = square(cell)
            g[y][x] = glyph(cell)
            for direction in (Cell.EAST, Cell.SOUTH):
                if cell.linked(direction):
                    other = neighbour(grid, cell, direction)
                    ox, oy = square(other)
                    lower = cell if p["band"][(r, c)] <= p["band"][(other.row, other.col)] else other
                    g[(y + oy) // 2][(x + ox) // 2] = glyph(lower)
    ex, ey = square(p["entrance"])
    g[ey][ex] = "<"
    xx, xy = square(p["exit"])
    g[xy][xx] = ">"
    return ["".join(row) for row in g]


def scene_id(cell):
    return f"end-{cell.row}-{cell.col}"


def make_map(grid, p):
    band_name = lambda b: "The Mouth of the Hedge" if b == 0 else f"Ring {b} of the Hedge"
    areas = {GLYPHS[b]: {"name": band_name(b), "light": "dark"} for b in range(p["n_bands"])}
    legend = {GLYPHS[b]: {"area": GLYPHS[b]} for b in range(p["n_bands"])}
    cells = {}
    ex, ey = square(p["entrance"])
    cells[key(ex, ey)] = {"area": GLYPHS[p["band"][(p["entrance"].row, p["entrance"].col)]],
                          "link": {"hub": True}}
    xx, xy = square(p["exit"])
    cells[key(xx, xy)] = {"area": GLYPHS[p["band"][(p["exit"].row, p["exit"].col)]],
                          "link": {"scene": "out"}}
    px, py = square(p["path"][1])
    cells[key(px, py)] = {"event": "plate"}
    for cell in p["fights"]:
        x, y = square(cell)
        cells[key(x, y)] = {"event": scene_id(cell)}
    if p["treasure"]:
        x, y = square(p["treasure"])
        cells[key(x, y)] = {"event": "treasure"}
    return {
        "id": MAP_ID,
        "title": "The Hedge",
        "tier": f"{p['algorithm']}, seed {p['seed']}, {p['rows']} by {p['cols']}",
        "grid": make_grid(grid, p),
        "legend": legend,
        "cells": cells,
        "areas": areas,
        "wander": [{"weight": 1, "encounter": "lone-rat"}],
    }


def make_events(grid, p):
    first = p["path"][1]
    fx, fy = square(first)
    facing = FACING[direction_between(p["entrance"], first)]
    tell = TELLS[p["algorithm"]]
    events = {
        "job": {
            "title": "The Hedge",
            "text": ["Maren unrolls nothing. \"There is no map. The hedge grew itself. "
                     "Find the far gate and come back with what you find.\""],
            "choices": [{"id": "ok", "mode": "plan", "text": "Take the job.",
                         "effects": {"goto": {"close": True}}}],
        },
        "gate": {
            "title": "The Gate",
            "text": ["The hedge stands past the last field. The stair down is at its mouth."],
            "choices": [
                {"id": "go", "mode": "act", "text": "Go down into the hedge.",
                 "effects": {"goto": {"map": MAP_ID, "x": fx, "y": fy, "facing": facing}}},
                {"id": "stay", "mode": "plan", "text": "Not yet.",
                 "effects": {"goto": {"close": True}}},
            ],
        },
        "plate": {
            "title": "The Plate",
            "text": [tell["brush"], "A plate is set in the wall beside the stair."],
            "choices": [
                {"id": "read", "mode": "plan", "text": "Read the plate.",
                 "say": [tell["rule"]], "once": True},
                {"id": "on", "mode": "plan", "text": "Walk on.",
                 "effects": {"goto": {"close": True}}},
            ],
        },
        "out": {
            "title": "The Far Gate",
            "text": ["A stair up. Daylight at the top of it."],
            "choices": [
                {"id": "go", "mode": "act", "text": "Climb out.",
                 "effects": {"goto": {"ending": "end-out"}}},
                {"id": "stay", "mode": "plan", "text": "Not yet.",
                 "effects": {"goto": {"close": True}}},
            ],
        },
        "dark": {
            "title": "Dark",
            "text": ["The last light goes out."],
            "noLeave": True,
            "choices": [{"id": "feel", "mode": "act", "text": "Feel your way back.",
                         "effects": {"goto": {"hub": True}}}],
        },
        "treasure": {
            "title": "The Heart of the Hedge",
            "text": ["The deepest dead end. Something has been left on a flat stone."],
            "choices": [{"id": "take", "mode": "act", "text": "Take it.", "turns": 1, "once": True,
                         "effects": {"item": {"add": {"stone-apple": 1, "gold": 20}},
                                     "say": ["An apple of stone, and coins under it."]}}],
        },
    }
    for cell in p["fights"]:
        back = neighbour(grid, cell, cell.get_links()[0])
        bx, by = square(back)
        events[scene_id(cell)] = {
            "title": "A Dead End",
            "text": ["The hedge closes. Eyes in the dark at the end of it."],
            "noLeave": True,
            "choices": [
                {"id": "fight", "mode": "act", "text": "Fight.",
                 "effects": {"goto": {"encounter": "enc-" + scene_id(cell)}}},
                {"id": "back", "mode": "act", "text": "Back out.",
                 "effects": {"goto": {"map": MAP_ID, "x": bx, "y": by,
                                      "facing": FACING[direction_between(cell, back)]}}},
            ],
        }
    return events


def make_encounters(p):
    encounters = {
        "lone-rat": {"foes": [{"id": "giant-rat", "count": 1, "hp": [2]}], "first": "foes",
                     "nonLethal": True, "text": ["A rat runs at the light."]},
    }
    for cell in p["fights"]:
        n = 2 + random.randint(0, 1)
        encounters["enc-" + scene_id(cell)] = {
            "foes": [{"id": "giant-rat", "count": n, "hp": [random.randint(1, 4) for _ in range(n)]}],
            "first": "foes",
            "text": [f"{'Two' if n == 2 else 'Three'} rats the size of dogs come out of the hedge."],
            "onWin": {"item": {"add": {"gold": 5 * n}}},
        }
    return encounters


def make_replay(p, party_ids):
    """Commands that walk the solution from the town to the far gate."""
    commands = [
        {"t": "pick", "ids": party_ids},
        {"t": "choose", "id": "ok"},
        {"t": "hub", "action": "go"},
        {"t": "choose", "id": "go"},
        {"t": "choose", "id": "on"},
    ]
    path = p["path"]
    facing = FACING[direction_between(path[0], path[1])]
    for here, there in zip(path[1:], path[2:]):
        want = FACING[direction_between(here, there)]
        turn = (want - facing) % 4
        if turn:
            commands.append({"t": "turn", "dir": {1: "right", 2: "about", 3: "left"}[turn]})
            facing = want
        commands.append({"t": "move", "dir": "forward"})
        commands.append({"t": "move", "dir": "forward"})
    commands.append({"t": "choose", "id": "go"})
    return {"seed": p["seed"], "commands": commands}


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def export(rows, cols, algorithm, seed, out, fights=3, pack_id="hedge"):
    grid = build_maze(rows, cols, algorithm, seed)
    p = plan(grid, algorithm, seed, fights)
    os.makedirs(os.path.join(out, "maps"), exist_ok=True)
    for name in BASE_FILES:
        shutil.copy(os.path.join(BASE_DIR, name + ".json"), os.path.join(out, name + ".json"))
    with open(os.path.join(BASE_DIR, "party.json")) as f:
        party_ids = json.load(f)["default"]
    write_json(os.path.join(out, "pack.json"), {
        "id": pack_id,
        "title": f"The Hedge ({algorithm}, seed {seed})",
        "version": "0.1",
        "credits": "Maze by MazeBuilder. Party, items and monsters from the Crawler's test fixture.",
        "start": {"scene": "job"},
        "storage": f"hedge-{algorithm}-{seed}",
    })
    write_json(os.path.join(out, "hub.json"), {
        "title": "The Fort", "text": ["Smoke, goats, the lake."],
        "places": [
            {"id": "hall", "label": "The Hall", "text": "Maren's table.",
             "actions": [{"id": "roster", "label": "Change the party", "kind": "roster"}]},
            {"id": "shop", "label": "Harrow's Cart", "text": "Harrow sells, and buys.",
             "actions": [{"id": "buy", "label": "Trade", "kind": "shop",
                          "stock": [{"item": "torch", "price": 1}, {"item": "oil-flask", "price": 2}]}]},
            {"id": "shrine", "label": "The Shrine", "text": "The Terminal scrolls.",
             "actions": [{"id": "rest", "label": "Rest", "kind": "rest", "price": 0}]},
            {"id": "gate", "label": "The Gate", "text": "The way out.",
             "actions": [{"id": "go", "label": "Go out", "kind": "scene", "scene": "gate"}]},
        ],
        "report": {"title": "What you tell Maren", "lines": {}},
    })
    write_json(os.path.join(out, "endings.json"), {
        "end-dead": {"title": "The Hedge Keeps You", "kind": "dead", "text": ["Nobody comes back."]},
        "end-out": {"title": "The Far Gate", "kind": "good",
                    "text": ["You come up in a field you do not know, with the hedge behind you."]},
    })
    write_json(os.path.join(out, "events.json"), make_events(grid, p))
    write_json(os.path.join(out, "encounters.json"), make_encounters(p))
    write_json(os.path.join(out, "maps", MAP_ID + ".json"), make_map(grid, p))
    write_json(os.path.join(out, "replay.json"), make_replay(p, party_ids))
    return grid, p


def main():
    parser = argparse.ArgumentParser(description="Export a maze as a Crawler pack")
    parser.add_argument("rows", nargs="?", type=int, default=8)
    parser.add_argument("cols", nargs="?", type=int, default=8)
    parser.add_argument("--algorithm", "-a", choices=sorted(TELLS), default="sidewinder")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--fights", type=int, default=3, help="dead ends that hold a fight")
    parser.add_argument("--out", "-o", default="out/hedge", help="pack directory to write")
    parser.add_argument("--id", default="hedge", help="pack id (lower-kebab-case)")
    args = parser.parse_args()
    grid, p = export(args.rows, args.cols, args.algorithm, args.seed, args.out, args.fights, args.id)
    print(grid.display())
    e, x = p["entrance"], p["exit"]
    print(f"\nEntrance ({e.row},{e.col}), exit ({x.row},{x.col}), "
          f"{len(p['path']) - 1} steps, {p['n_bands']} bands of {p['width']}, "
          f"{len(p['fights'])} fights. Pack written to {args.out}")


if __name__ == "__main__":
    main()

# MazeBuilder Python Port Tests

This directory contains tests for the Python port of the MazeBuilder application.

## Running Tests

To run all tests:

```bash
cd py_port
pytest
```

To run a specific test file:

```bash
pytest tests/test_cell.py
```

To run with verbose output:

```bash
pytest -v
```

## Test Coverage

The tests cover:

1. **Cell Class** - `test_cell.py`
   - Initialization
   - Linking and unlinking
   - Bit operations
   - Direction mapping

2. **Grid Class** - `test_grid.py`
   - Initialization
   - Cell access
   - Position validation
   - Cell linking
   - Grid display

3. **Binary Tree Algorithm** - `test_binary_tree.py`
   - Algorithm execution on various grid positions
   - Edge cases (corners, edges)
   - Complete maze generation

4. **Pathfinding** - `test_dijkstra.py` and `test_distances.py`
   - Distance calculations
   - Shortest path finding
   - Longest path (maze solution) finding
   - Distance tracking

## Testing Strategy

The tests use various techniques:

1. **Unit Testing** - Testing individual components in isolation
2. **Mock Objects** - Mocking random number generation for deterministic tests
3. **Fixtures** - Shared maze configurations (see `conftest.py`)
4. **Edge Cases** - Testing boundary conditions (grid edges, corners)

## Adding New Tests

When adding new maze algorithms or features, follow this pattern:

1. Create a new test file named `test_your_feature.py`
2. Use the existing test structure as a template
3. Test both normal operation and edge cases
4. For randomized algorithms, use mocking to create deterministic tests
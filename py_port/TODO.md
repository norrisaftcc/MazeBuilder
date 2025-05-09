# MazeBuilder Python Port - TODO List

## Sprint 1: Basic Console Implementation ✅
- [x] Implement Cell class with bit flag directions
- [x] Implement Grid class with ASCII display
- [x] Implement Binary Tree maze generation algorithm
- [x] Add Dijkstra's algorithm for pathfinding
- [x] Create command-line interface with basic options
- [x] Add colored output
- [x] Implement distance markers display
- [x] Create test framework for all components

**Status: COMPLETE**  
The basic console implementation is now functional with the Binary Tree algorithm.
The application can generate mazes, display them with colored text, find the "longest path" 
solution, and show distances from the start point to each cell.

## Sprint 2: Additional Maze Algorithms
- [x] Implement Sidewinder algorithm
  - [x] Add tests for Sidewinder algorithm
  - [x] Create command-line option to select algorithm
- [ ] Implement Aldous-Broder algorithm
  - [ ] Add tests for Aldous-Broder algorithm
- [ ] Create visualization that shows step-by-step algorithm execution
- [ ] Add custom seed option for reproducible maze generation
- [ ] Add ability to save/load mazes to files

## Sprint 3: Advanced Features
- [ ] Implement Hunt-and-Kill algorithm
- [ ] Implement Recursive Backtracker algorithm
- [ ] Add Eller's algorithm
- [ ] Add Growing Tree algorithm
- [ ] Create maze difficulty comparison metrics
- [ ] Add optimization options for large mazes
- [ ] Create multi-threading support for maze generation
- [ ] Add statistics about mazes (dead-end count, river, etc.)

## Sprint 4: Streamlit Web Interface
- [ ] Set up basic Streamlit app structure
- [ ] Implement maze visualization component
- [ ] Add algorithm selection controls
- [ ] Add maze size controls
- [ ] Implement real-time visualization of maze generation
- [ ] Create interactive pathfinding visualization
- [ ] Add export options (PNG, SVG, etc.)
- [ ] Create help/documentation pages
- [ ] Add animation options
- [ ] Optimize for mobile/desktop viewing

## Sprint 5: Extensions and Enhancements
- [ ] Add 3D maze generation option
- [ ] Implement "perfect" vs "imperfect" maze options
- [ ] Add multiple entrance/exit options
- [ ] Create theme options for maze display
- [ ] Add maze solver comparisons (A*, BFS, DFS)
- [ ] Create maze game mode
- [ ] Implement maze difficulty levels
- [ ] Add tutorial mode with step-by-step algorithm explanations
- [ ] Create API endpoints for maze generation

## Development Notes
- Use clean, Pythonic code throughout
- Maintain high test coverage for all features
- Ensure command-line help text is comprehensive
- Make the console interface and Streamlit UI share code when possible
- Keep performance in mind, especially for larger mazes
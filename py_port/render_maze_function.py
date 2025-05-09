def render_maze(grid, solution_path=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Set theme-specific colors
    if st.session_state.theme == "wizardry":
        # Wizardry theme (midnight blue with yellow walls)
        bg_color = '#000000'  # Black background
        wall_color = '#FFFF00'  # Bright yellow walls
        entrance_color = '#32CD32'  # Lime green
        exit_color = '#FF4500'  # Orange-red
        path_color = '#00BFFF'  # Deep sky blue
        path_text_color = '#FFFFFF'  # White text
        title_color = 'gold'
        title_font = 'serif'
        title_text = 'The Maze Construction'
    else:
        # Retro 1980s terminal theme (black with green phosphor)
        bg_color = '#000000'  # Black background
        wall_color = '#00FF00'  # Bright green walls
        entrance_color = '#00AA00'  # Darker green
        exit_color = '#00AA00'  # Darker green
        path_color = '#003300'  # Very dark green
        path_text_color = '#00FF00'  # Bright green text
        title_color = '#00FF00'  # Green
        title_font = 'monospace'
        title_text = 'MAZE GENERATION COMPLETE'
    
    # Set background color
    ax.set_facecolor(bg_color)
    
    # Calculate cell size
    cell_size = 1.0
    
    # Draw the cells
    for r in range(grid.rows):
        for c in range(grid.cols):
            cell = grid.at(r, c)
            
            # Cell position (y-axis inverted to match grid coordinates)
            x = c * cell_size
            y = (grid.rows - 1 - r) * cell_size
            
            # Check for entrance and exit
            is_entrance = (r == grid.rows - 1 and c == 0)
            is_exit = (r == 0 and c == grid.cols - 1)
            is_on_path = False
            
            # Check if cell is on solution path
            if solution_path:
                for path_cell in solution_path:
                    if path_cell.row == r and path_cell.col == c:
                        is_on_path = True
                        break
            
            # Draw walls where there are no links
            line_style = '-' if st.session_state.theme == "wizardry" else '--' if is_on_path else '-'
            linewidth = 3 if st.session_state.theme == "wizardry" else 2
            
            if not cell.linked(Cell.NORTH) and r > 0:
                ax.plot([x, x + cell_size], [y + cell_size, y + cell_size], wall_color, linewidth=linewidth, linestyle=line_style)
            if not cell.linked(Cell.EAST) and c < grid.cols - 1:
                ax.plot([x + cell_size, x + cell_size], [y, y + cell_size], wall_color, linewidth=linewidth, linestyle=line_style)
            if not cell.linked(Cell.SOUTH) and r < grid.rows - 1:
                ax.plot([x, x + cell_size], [y, y], wall_color, linewidth=linewidth, linestyle=line_style)
            if not cell.linked(Cell.WEST) and c > 0:
                ax.plot([x, x], [y, y + cell_size], wall_color, linewidth=linewidth, linestyle=line_style)
            
            # Process special cells (entrance, exit, path)
            if is_entrance:
                if st.session_state.theme == "retro":
                    # For retro theme, just show a character
                    ax.text(x + cell_size/2, y + cell_size/2, 'E', color=entrance_color, 
                            fontsize=14, ha='center', va='center', fontweight='bold', family='monospace')
                else:
                    # For wizardry theme, use a colored rectangle
                    ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, fill=True, color=entrance_color, alpha=0.8))
                    ax.text(x + cell_size/2, y + cell_size/2, 'E', color='white', 
                            fontsize=12, ha='center', va='center', fontweight='bold')
            elif is_exit:
                if st.session_state.theme == "retro":
                    # For retro theme, just show a character
                    ax.text(x + cell_size/2, y + cell_size/2, 'X', color=exit_color, 
                            fontsize=14, ha='center', va='center', fontweight='bold', family='monospace')
                else:
                    # For wizardry theme, use a colored rectangle
                    ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, fill=True, color=exit_color, alpha=0.8))
                    ax.text(x + cell_size/2, y + cell_size/2, 'X', color='white', 
                            fontsize=12, ha='center', va='center', fontweight='bold')
            elif is_on_path and st.session_state.show_solution:
                # Calculate distance from the exit for cells on the path
                if solution_path:
                    distance = 0
                    for i, path_cell in enumerate(solution_path):
                        if path_cell.row == r and path_cell.col == c:
                            distance = len(solution_path) - i - 1
                            break
                    
                    if st.session_state.theme == "retro":
                        # For retro theme, show distance without background
                        ax.text(x + cell_size/2, y + cell_size/2, str(distance), color=path_text_color, 
                                fontsize=12, ha='center', va='center', fontweight='bold', family='monospace')
                    else:
                        # For wizardry theme, use a colored rectangle
                        ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, fill=True, color=path_color, alpha=0.9))
                        ax.text(x + cell_size/2, y + cell_size/2, str(distance), color=path_text_color, 
                                fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Set limits and remove axes
    ax.set_xlim(0, grid.cols * cell_size)
    ax.set_ylim(0, grid.rows * cell_size)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Set title based on theme
    plt.title(title_text, color=title_color, fontsize=16, fontweight='bold', family=title_font)
    
    return fig
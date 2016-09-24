using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    class AldousBroderMazeBuilder : MazeBuilder
    {
        // random walk using the Aldous-Broder algorithm.

        public void buildMaze(Grid grid)
        {
            Cell cell, neighbor;
            // start in a random location within the grid
            int x = rand.Next(grid.Columns);
            int y = rand.Next(grid.Rows);
            int unvisited = (grid.getSize() - 1);

            cell = grid.Cells[x, y];

            while (unvisited > 0) // continue rand walk until all cells are visited
            {
                List<Cell> neighbors = cell.getNeighbors();
                int randNeighbor = rand.Next(neighbors.Count);
                neighbor = neighbors[randNeighbor];

                if (neighbor.Links.Count == 0)
                {
                    // if no links in neighbor, it's unvisited, so link it and count it as visited
                    cell.link(neighbor);
                    unvisited -= 1; 
                }
                cell = neighbor; // continue the random walk 
            }
        }
    }
}

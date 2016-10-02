using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    class DistanceCalculator
    {
        // uses Dijkstra's Algorithm to calculate distance of each cell from start
        public DistanceCalculator()
        {

        }

        public void ClearDistanceInfo(Grid g)
        {
            // distance -1 represents empty data
            for (int r=0; r<g.Rows; r++)
            {
                for (int c=0; c<g.Columns; c++)
                {
                    g.Cells[r, c].DistanceFromStart = -1;
                }
            }
        }

        public void CalculateDistances(Grid g, Cell startCell)
        {
            // Determine the distance of each cell in the grid from start
            // populate the cell.DistanceFromStart of each cell with the distance.

            // Begin at starting point, its distance is zero
            // Add all cells linked to start to the frontier and mark those distance 1
            // repeat with a new frontier, increasing distance by 1
            List<Cell> frontier = new List<Cell>();
            List<Cell> new_frontier; 
            frontier.Add(startCell); // begin with starting cell 
            startCell.DistanceFromStart = 0;
            while (frontier.Count > 0)
            {
                new_frontier = new List<Cell>();
                foreach (Cell c in frontier)
                {
                    foreach (Cell n in c.getNeighbors())
                    {
                        
                        if (n.isLinked(c) && n.DistanceFromStart == -1)
                        {
                            // no distance yet assigned, so do so
                            n.DistanceFromStart = c.DistanceFromStart + 1;
                            // add to new_frontier
                            new_frontier.Add(n);
                        }
                    }
                } // foreach cell in frontier
                frontier = new_frontier;

            } // while(frontier.count > 0)
            // complete -- grid cells all have a distance value

        } // CalculateDistance
    }
}

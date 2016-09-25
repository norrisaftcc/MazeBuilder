using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    public class SidewinderMazeBuilder: MazeBuilder
    {
        // general algorithm:
        //
        // iterate through the grid, row by row.
        // at start of each row, create a new "run" of cells in an array.
        // if it's time to close the run (because we're at a N or E boundary,
        // or if a random roll dictates to close this run now), then link
        // to the north if possible, finish the run, and start a new run. 
        // else link this cell to the east.

        public new void buildMaze(Grid grid)
        {
            List<Cell> run = new List<Cell>();
            Cell cell, member;
            Boolean bAtEastBound, bAtNorthBound, bShouldCloseOut;
            int coinFlip;

            // iterate through rows
            for (int i = 0; i < grid.Rows; i++)
            {
                for (int j = 0; j < grid.Columns; j++)
                {
                    cell = grid.Cells[i, j];
                    run.Add(cell);

                    bAtEastBound = (cell.East == null);
                    bAtNorthBound = (cell.North == null);

                    coinFlip = rand.Next(2);

                    bShouldCloseOut = bAtEastBound || (!bAtNorthBound && coinFlip == 0);

                    if (bShouldCloseOut)
                    {
                        int sample = rand.Next(run.Count);
                        member = run[sample];
                        if (member.North != null)
                        {
                            member.link(member.North);
                        }
                        run.Clear();
                    }
                    else
                    {
                        cell.link(cell.East);
                    }
                } // for columns

            } // for rows
        }

    }
}

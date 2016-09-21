using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    class BinaryTree
    {
        // build a maze from a Grid using the BinaryTree method
        public void buildMaze(Grid grid)
        {
            int rows = grid.Rows;
            int cols = grid.Columns;
            // not sure if starting at top left will work o_O
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    Cell c = grid.Cells[i,j];
                    processCell(c);
                }
            }
        }

        public void processCell(Cell c)
        {
            List<Cell> neighbors = new List<Cell>();
            if (c.North != null)
            {
                neighbors.Add(c.North);
            }
            if (c.East != null)
            {
                neighbors.Add(c.East);
            }

            Random r = new Random();
            int index = r.Next(neighbors.Count());
            Cell neighbor = null;
            if (index > 0)
            {
                neighbor = neighbors.ElementAt(index);
            }
            if (neighbor != null)
            {
                c.link(neighbor);
            }
        }
    }
}

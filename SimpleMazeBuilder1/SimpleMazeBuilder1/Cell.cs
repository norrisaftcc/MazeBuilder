using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    public class Cell
    {
        public int Row { get; set; }
        public int Column { get; set; }

        public Cell North { get; set; }
        public Cell South { get; set; }
        public Cell East  { get; set; }
        public Cell West  { get; set; }

        public List<Cell> Links { get; set; }

        public Cell(int row, int col)
        {
            this.Row = row;
            this.Column = col;
            this.Links = new List<Cell>();
        }

        public void link(Cell c, Boolean bidi=true)
        {
            this.Links.Add(c);
            if (bidi)
            {
                c.link(this, false); // link the other way    
            }
        }

        public void unlink(Cell c, Boolean bidi=true)
        {
            if (this.Links.IndexOf(c) != -1) 
            {
                this.Links.Remove(c);
                c.unlink(this, false); // unlink the other way
            }
        }

        public bool isLinked(Cell c)
        {
            if (c == null) { return false; }
            if (this.Links.IndexOf(c) == -1) { return false;  }
            return true;
        }

        public List<Cell> getNeighbors()
        {
            List<Cell> neighbors = new List<Cell>();
            if (this.North != null)
            {
                neighbors.Add(this.North);
            }
            if(this.South != null)
            {
                neighbors.Add(this.South);
            }
            if(this.East != null)
            {
                neighbors.Add(this.East);
            }
            if(this.West != null)
            {
                neighbors.Add(this.West);
            }
            return neighbors;
        }

    }
}

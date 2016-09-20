﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    public class Grid
    {
        public int Rows { get; set; }
        public int Columns { get; set; }

        private Cell[,] _cells;
        public Cell[,] Cells
        {
            get { return _cells; }
            set { _cells = value; }
        }

        public Grid(int rows, int cols)
        {
            this.Rows = rows;
            this.Columns = cols;

            _cells = new Cell[rows,cols];
            createCells();
            configureCells();
        }

        private void createCells()
        {
            int r, c = 0;

            for (r = 0; r < this.Rows; r++)
            {
                for (c = 0; c < this.Columns; c++)
                {
                    _cells[r,c] = new Cell(r, c);
                }
            }
        }

        private void configureCells()
        {
            int r,c = 0;

            for (r = 0; r < this.Rows; r++)
            {
                for (c = 0; c < this.Columns; c++)
                {
                    Cell cell = _cells[r, c];

                    //cell.Row = r;
                    //cell.Column = c;
                    // if the neighbor in a direction would be within the grid, add it, else null
                    if (r > 0) { cell.North = _cells[r - 1, c]; }
                    if (r < this.Rows - 1) { cell.South = _cells[r + 1, c]; }
                    if (c > 0) { cell.West = _cells[r, c - 1]; }
                    if (c < this.Columns - 1) { cell.East = _cells[r, c + 1]; }
                }
            }
            Console.WriteLine("Grid of " + this.Rows + " rows by " + this.Columns + " columns initialized.");
        }

        public Cell getRandomCell()
        {
            Random rand = new Random();
            int row = rand.Next(this.Rows);
            int col = rand.Next(this.Columns);

            return this.Cells[row, col];
        }

        public int getSize()
        {
            return this.Rows * this.Columns;
        }
    }
       
}
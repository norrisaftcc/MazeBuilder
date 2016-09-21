﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    class BinaryTree
    {
        // build a maze from a Grid using the BinaryTree method
        Random r;
        public BinaryTree()
        {
            // Random is terrible, so we'll seed it using a different RNG
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                // Buffer storage.
                byte[] data = new byte[4];
                rng.GetBytes(data);

                // Convert to int 32.
                int value = BitConverter.ToInt32(data, 0);
                Console.WriteLine(value);
                r = new Random(value);
            }        
    }

        public void buildMaze(Grid grid)
        {

            int rows = grid.Rows;
            int cols = grid.Columns;
            // iterate over each cell
            // start at the bottom [rows-1,0] and move upwards
            for (int i = rows-1; i >= 0 ; i--)
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
            // randomly link cell with north or east neighbor, if available
            
            int n = neighbors.Count();
            if (n == 0)
            {
                return;
            }
            int roll = r.Next(20);
            int index = roll % n; // pick one of the possible n or e exits
            Console.Write("("+roll+","+n+","+index+")");
            Cell neighbor = null;
            if (n > 0)
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

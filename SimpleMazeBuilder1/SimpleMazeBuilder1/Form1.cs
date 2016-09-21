using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SimpleMazeBuilder1
{
    public partial class Form1 : Form
    {
        public Grid grid;

        public Form1()
        {
            InitializeComponent();
        }

        private void btnInitGrid_Click(object sender, EventArgs e)
        {
            // create a 10x10 grid 
            grid = new Grid(10, 10);

        }

        private void btnRandomCell_Click(object sender, EventArgs e)
        {
            if (grid != null)
            {
                BinaryTree bt = new BinaryTree();
                bt.buildMaze(grid);
            }
            Console.WriteLine("Maze Built");
        }
    }
}

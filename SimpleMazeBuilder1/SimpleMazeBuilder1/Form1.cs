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
            // create a 10x10 grid 
            grid = new Grid(10, 10);
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
                BinaryTreeMazeBuilder bt = new BinaryTreeMazeBuilder();
                bt.buildMaze(grid);
            }
            Console.WriteLine("Binary Tree Maze Built");
        }

        private void btnUpdateTextBox_Click(object sender, EventArgs e)
        {
            if (grid != null)
            {
                String output = grid.toString();
                textOutput.Text = output;
            }
        }

        private void btnSidewinder_Click(object sender, EventArgs e)
        {
            if (grid != null)
            {
                SidewinderMazeBuilder sw = new SidewinderMazeBuilder();
                sw.buildMaze(grid);
            }
            Console.WriteLine("Sidewinder Maze Built");
        }

        private void btnAldousBroder_Click(object sender, EventArgs e)
        {
            // don't try to run random walk on a previously built maze -- it never exits
            // so always init grid
            // create a 10x10 grid 
            grid = new Grid(10, 10);
            AldousBroderMazeBuilder ab = new AldousBroderMazeBuilder();
            ab.buildMaze(grid);
            
            Console.WriteLine("Aldous-Broder Maze Built");
        }
    }
}

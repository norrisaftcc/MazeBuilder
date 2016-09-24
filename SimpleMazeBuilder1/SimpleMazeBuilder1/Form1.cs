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
                textOutput.Show();
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

        private void btnBitmapDraw_Click(object sender, EventArgs e)
        {
            textOutput.Hide();
            // first take: draw directly on the form
            System.Drawing.SolidBrush myBrush = new System.Drawing.SolidBrush(System.Drawing.Color.LightGray);
            System.Drawing.Graphics formGraphics;
            formGraphics = this.CreateGraphics();
            int x_init, y_init;
            x_init = 120;
            y_init = 50;
            int canvas_x = 300;
            int canvas_y = 300;
            formGraphics.FillRectangle(myBrush, new Rectangle(x_init, y_init, x_init+canvas_x, y_init+canvas_y));
            myBrush.Dispose();

            int cell_size = 30;
            int width = cell_size * grid.Columns;
            int height = cell_size * grid.Rows;
            System.Drawing.Pen pen;
            pen = new System.Drawing.Pen(System.Drawing.Color.Black);
            // currently broken
            for (int i=0; i<grid.Rows; i++)
            {
                for (int j=0; j<grid.Columns; j++)
                {
                    // for each cell
                    Cell c = grid.Cells[i, j];
                    int x1 = i * cell_size;
                    int y1 = j * cell_size;
                    int x2 = (i + 1) * cell_size;
                    int y2 = (j + 1) * cell_size;
                    x1 += x_init;
                    x2 += x_init;
                    y1 += y_init;
                    y2 += y_init;

                    if (c.North == null)
                    {
                        formGraphics.DrawLine(pen, x1, y1, x2, y1);
                    }
                    if (c.West == null)
                    {
                        formGraphics.DrawLine(pen, x1, y1, x1, y2);
                    }
                    if (c.East != null && !c.isLinked(c.East))
                    {
                        formGraphics.DrawLine(pen, x2, y1, x2, y2);
                    }
                    if (c.South !=null && !c.isLinked(c.South))
                    {
                        formGraphics.DrawLine(pen, x1, y2, x2, y2);
                    }
                }
            }

            pen.Dispose();
            // cleanup
            formGraphics.Dispose();
        }
    }
}

namespace SimpleMazeBuilder1
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnInitGrid = new System.Windows.Forms.Button();
            this.btnDoBinaryTreeMaze = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // btnInitGrid
            // 
            this.btnInitGrid.Location = new System.Drawing.Point(32, 29);
            this.btnInitGrid.Name = "btnInitGrid";
            this.btnInitGrid.Size = new System.Drawing.Size(96, 23);
            this.btnInitGrid.TabIndex = 0;
            this.btnInitGrid.Text = "Init 10x10 Grid";
            this.btnInitGrid.UseVisualStyleBackColor = true;
            this.btnInitGrid.Click += new System.EventHandler(this.btnInitGrid_Click);
            // 
            // btnDoBinaryTreeMaze
            // 
            this.btnDoBinaryTreeMaze.Location = new System.Drawing.Point(32, 80);
            this.btnDoBinaryTreeMaze.Name = "btnDoBinaryTreeMaze";
            this.btnDoBinaryTreeMaze.Size = new System.Drawing.Size(96, 23);
            this.btnDoBinaryTreeMaze.TabIndex = 1;
            this.btnDoBinaryTreeMaze.Text = "Binary Tree Maze";
            this.btnDoBinaryTreeMaze.UseVisualStyleBackColor = true;
            this.btnDoBinaryTreeMaze.Click += new System.EventHandler(this.btnRandomCell_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(284, 262);
            this.Controls.Add(this.btnDoBinaryTreeMaze);
            this.Controls.Add(this.btnInitGrid);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnInitGrid;
        private System.Windows.Forms.Button btnDoBinaryTreeMaze;
    }
}


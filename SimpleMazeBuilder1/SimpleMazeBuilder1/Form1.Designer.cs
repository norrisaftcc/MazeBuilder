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
            this.textOutput = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.btnUpdateTextBox = new System.Windows.Forms.Button();
            this.btnSidewinder = new System.Windows.Forms.Button();
            this.btnAldousBroder = new System.Windows.Forms.Button();
            this.btnBitmapDraw = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // btnInitGrid
            // 
            this.btnInitGrid.Location = new System.Drawing.Point(12, 12);
            this.btnInitGrid.Name = "btnInitGrid";
            this.btnInitGrid.Size = new System.Drawing.Size(96, 23);
            this.btnInitGrid.TabIndex = 0;
            this.btnInitGrid.Text = "Init 10x10 Grid";
            this.btnInitGrid.UseVisualStyleBackColor = true;
            this.btnInitGrid.Click += new System.EventHandler(this.btnInitGrid_Click);
            // 
            // btnDoBinaryTreeMaze
            // 
            this.btnDoBinaryTreeMaze.Location = new System.Drawing.Point(11, 70);
            this.btnDoBinaryTreeMaze.Name = "btnDoBinaryTreeMaze";
            this.btnDoBinaryTreeMaze.Size = new System.Drawing.Size(96, 23);
            this.btnDoBinaryTreeMaze.TabIndex = 1;
            this.btnDoBinaryTreeMaze.Text = "Binary Tree Maze";
            this.btnDoBinaryTreeMaze.UseVisualStyleBackColor = true;
            this.btnDoBinaryTreeMaze.Click += new System.EventHandler(this.btnRandomCell_Click);
            // 
            // textOutput
            // 
            this.textOutput.Font = new System.Drawing.Font("Courier New", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textOutput.Location = new System.Drawing.Point(126, 54);
            this.textOutput.Multiline = true;
            this.textOutput.Name = "textOutput";
            this.textOutput.Size = new System.Drawing.Size(397, 359);
            this.textOutput.TabIndex = 2;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(161, 21);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(70, 13);
            this.label1.TabIndex = 3;
            this.label1.Text = "Display Maze";
            // 
            // btnUpdateTextBox
            // 
            this.btnUpdateTextBox.Location = new System.Drawing.Point(237, 21);
            this.btnUpdateTextBox.Name = "btnUpdateTextBox";
            this.btnUpdateTextBox.Size = new System.Drawing.Size(88, 23);
            this.btnUpdateTextBox.TabIndex = 4;
            this.btnUpdateTextBox.Text = "Update(ASCII)";
            this.btnUpdateTextBox.UseVisualStyleBackColor = true;
            this.btnUpdateTextBox.Click += new System.EventHandler(this.btnUpdateTextBox_Click);
            // 
            // btnSidewinder
            // 
            this.btnSidewinder.Location = new System.Drawing.Point(12, 108);
            this.btnSidewinder.Name = "btnSidewinder";
            this.btnSidewinder.Size = new System.Drawing.Size(95, 23);
            this.btnSidewinder.TabIndex = 5;
            this.btnSidewinder.Text = "Sidewinder";
            this.btnSidewinder.UseVisualStyleBackColor = true;
            this.btnSidewinder.Click += new System.EventHandler(this.btnSidewinder_Click);
            // 
            // btnAldousBroder
            // 
            this.btnAldousBroder.Location = new System.Drawing.Point(13, 148);
            this.btnAldousBroder.Name = "btnAldousBroder";
            this.btnAldousBroder.Size = new System.Drawing.Size(94, 23);
            this.btnAldousBroder.TabIndex = 6;
            this.btnAldousBroder.Text = "Aldous-Broder";
            this.btnAldousBroder.UseVisualStyleBackColor = true;
            this.btnAldousBroder.Click += new System.EventHandler(this.btnAldousBroder_Click);
            // 
            // btnBitmapDraw
            // 
            this.btnBitmapDraw.Location = new System.Drawing.Point(377, 20);
            this.btnBitmapDraw.Name = "btnBitmapDraw";
            this.btnBitmapDraw.Size = new System.Drawing.Size(75, 23);
            this.btnBitmapDraw.TabIndex = 7;
            this.btnBitmapDraw.Text = "Bitmap";
            this.btnBitmapDraw.UseVisualStyleBackColor = true;
            this.btnBitmapDraw.Click += new System.EventHandler(this.btnBitmapDraw_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(549, 473);
            this.Controls.Add(this.btnBitmapDraw);
            this.Controls.Add(this.btnAldousBroder);
            this.Controls.Add(this.btnSidewinder);
            this.Controls.Add(this.btnUpdateTextBox);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textOutput);
            this.Controls.Add(this.btnDoBinaryTreeMaze);
            this.Controls.Add(this.btnInitGrid);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnInitGrid;
        private System.Windows.Forms.Button btnDoBinaryTreeMaze;
        private System.Windows.Forms.TextBox textOutput;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btnUpdateTextBox;
        private System.Windows.Forms.Button btnSidewinder;
        private System.Windows.Forms.Button btnAldousBroder;
        private System.Windows.Forms.Button btnBitmapDraw;
    }
}


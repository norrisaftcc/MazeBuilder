using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace SimpleMazeBuilder1
{
    public class MazeBuilder
    {
        public Random rand; 

        public MazeBuilder()
        {
            // Random is terrible, so we'll seed it using a different RNG
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                // Buffer storage.
                byte[] data = new byte[4];
                rng.GetBytes(data);

                // Convert to int 32.
                int value = BitConverter.ToInt32(data, 0);
                Console.WriteLine("MazeBuilder random seed: " + value);
                rand = new Random(value);
            }
        }

        public void buildMaze(Grid g)
        {
            throw new NotImplementedException("You must use a subclass of MazeBuilder instead");
        }
    }
}

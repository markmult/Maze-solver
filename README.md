# Maze-solver

The main idea of maze solver is to place our beloved character Pentti into a difficult maze and see how he manages to find his way out.

In this approach Pentti uses Depth First Search algorithm to find the exit. Pentti's route is shown on the screen so you inspect how lost he was.

## How to setup and use

Clone this repository and install packages mentioned in requirements.txt.
```
git clone https://github.com/markmult/Data-visualizer.git
pip install -r relative\path\requirements.txt
```
After you have installed the required packages, run main.py.

When pygame screen opens, press key 1 or 2 on your keyboard to select maze. Maze is then printed to screen and you can start the journey by hitting space bar. Algorithm then tries to find a way out of the maze and propmts the results. You can return to start screen by pressing backspace -key.

If you wish to try this out with your own maze, replace one of the mazes in mazes folder. If you change the name of the file, update the file name accordingly also to the main.py file. Correct line is illustrated with comment.
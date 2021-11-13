# Maze-solver

The main idea of maze solver is to place our beloved character Pentti into a difficult maze and see how he manages to find his way out.

In this approach Pentti uses Depth First Search algorithm to find the exit. Pentti's route is shown on the screen so you can inspect how lost he was.

## How to setup and use

Clone this repository and install packages mentioned in requirements.txt.
```
git clone https://github.com/markmult/Data-visualizer.git
pip install -r relative\path\requirements.txt
```
After you have installed the required packages, run main.py.

When pygame screen opens, press key 1 or 2 on your keyboard to select maze. Maze is then printed to screen and you can start the journey by hitting space bar. Algorithm then tries to find a way out of the maze and results are shown. You can return to start screen by pressing backspace -key.

If you wish to try this out with your own maze, replace one of the mazes in mazes folder. If you change the name of the file, update the file name accordingly also to the main.py file. Correct line is shown with comment.

Maze should be given in txt file where "#" represents walls, " " represents movable space. "E" means exit and "^" start position. Other characters are not recognized.

## How to interpret the results

* Blocks Pentti visited are shown as blue in screen
* Total moves are shown on top right corner when algorithm is finished. This includes also steps back, so the amount of visited blocks is less than the number of total moves.
* Blue path does not represent the final path that DFS algorithm outputs.
* If there is no possible route, it is announced on top right corner
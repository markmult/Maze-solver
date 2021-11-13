import pygame
from enum import Enum

pygame.init()

# Global definitions
TITLE = "Maze"
SIZE = (1200, 600)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FONT_LARGE = pygame.font.SysFont("comicsans", 40, bold=True)
FONT_MED = pygame.font.SysFont("comicsans", 25, bold=True)
FONT_SMALL = pygame.font.SysFont("comicsans", 15, bold=False)

# Relative paths to the mazes. Change these files if you wish to try out
# the algorithm with different mazes. The program can read two files at
# a time.
FILE1 = "mazes/maze-task-first.txt"
FILE2 = "mazes/maze-task-second.txt"

class State(Enum):
    """
    Enum for game states.
    """
    START = 1
    INIT = 2
    RUNNING = 3
    DONE = 4
    HOLD = 5

class Maze:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.filename = None
        self.block_size = None
        self.horizontal_offset = None
        self.vertical_offset = None
        self.blocks = []
        self.path = []
        self.moves = 0
        self.finished = False


    def __adapt_display(self):
        """
        Set maze to center of the screen and adapt block sizes based on
        maze and screen size.
        """
        empty_vertical_space = self.screen_height / 10
        self.block_size = (self.screen_height - empty_vertical_space) / len(self.blocks)
        self.vertical_offset = empty_vertical_space / 2
        self.horizontal_offset = (self.screen_width - self.block_size * len(self.blocks[0])) / 2


    def display_results(self):
        """
        Display results when maze algorithm finds exit or all blocks are
        searched. Results are shown in the top-right corner of the screen.
        Content differs whether the algorithm succeeded or not.
        """
        pygame.draw.rect(self.screen,
                         WHITE,
                         (self.screen_width - 450, 10, 500, 150),
                         0)
        if self.finished:
            text_done = FONT_MED.render("DONE!", 1, BLACK)

            if self.moves > 200:
                success = "Failed to solve with under 200 moves."
            elif self.moves > 150:
                success = "Failed to solve with under 150 moves."
            elif self.moves > 20:
                success = "Failed to solve with under 20 moves."
            else:
                success = "Solving with 20 moves succeeded!"

            results = "{} moves used. {}".format(self.moves, success)
            text_results = FONT_SMALL.render(results, 1, BLACK)

            self.screen.blit(text_results, (self.screen_width - 430, 50))

        else:
            text_done = FONT_MED.render("Unable to solve given puzzle.", 1, BLACK)

        desc = "Blocks that Pentti visited are shown as blue on the screen."
        desc_text = FONT_SMALL.render(desc, 1, BLACK)
        text_info = FONT_SMALL.render("Press backspace to return to start screen.",
                                      1,
                                      BLACK)
        self.screen.blit(text_done, (self.screen_width - 430, 10))
        self.screen.blit(desc_text, (self.screen_width - 430, 70))
        self.screen.blit(text_info, (self.screen_width - 430, 120))
        pygame.display.update()


    def draw_maze(self):
        """
        Draw current state of maze to game screen.
        """
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                block_type = self.blocks[i][j]
                # Draw rect one pixel larger than given block size to avoid
                # cracks in maze wall
                rect = pygame.Rect(j * self.block_size + self.horizontal_offset,
                                    i * self.block_size + self.vertical_offset,
                                    self.block_size+1,
                                    self.block_size+1)
                if block_type == "#":
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif block_type == "E":
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif block_type == "^":
                    pygame.draw.rect(self.screen, RED, rect)
                elif block_type == "+":
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)


    def find_start(self):
        """
        Return maze start postion as (x,y) coordinate tuple.
        """
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks)):
                if self.blocks[i][j] == "^":
                    return (j, i)


    def load_maze(self, filename):
        """
        Load given file and store its content to list.

        :param str filename: Path to file with text maze.
        """
        maze = []
        try:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    maze.append([c for c in line])

            f.close()
        except FileNotFoundError:
            print("Unable to load file")

        self.blocks = maze
        self.__adapt_display()


    def refresh_maze_screen(self):
        """
        Update maze screen by re-drawing the blocks.
        """
        self.screen.fill(WHITE)
        self.draw_maze()
        pygame.display.update()


    def solve_maze(self, point):
        """
        Find a way out of maze with Depth first search -algorithm.
        Function takes certain coordinate in maze and checks if
        move is allowed. If given point is not exit or illegal, call
        this function again with point where x or y position is + or
        - 1 from square given as parameter. This function solves the
        maze recursively when called with maze start point.

        :param tuple[int, int] point: (x,y) -coordinate of point in maze.
        """
        if self.finished:
            return

        x_pos = point[0]
        y_pos = point[1]

        # Return if given position is outside of the maze
        if x_pos < 0 or x_pos > len(self.blocks[0])-1 or y_pos < 0 or y_pos > len(self.blocks)-1:
            return

        # Return if given postion is wall or already visited
        if point in self.path or self.blocks[y_pos][x_pos] == "#" or self.blocks[y_pos][x_pos] == "+":
            return

        # Add coordinate to solution stack
        self.path.append(point)
        self.moves += 1

        if self.blocks[y_pos][x_pos] == "E":
            self.finished = True
            self.path.pop()
            return
        else:
            # Check neighbor blocks
            self.blocks[y_pos][x_pos] = "+"
            self.solve_maze((x_pos - 1, y_pos))
            self.solve_maze((x_pos + 1, y_pos))
            self.solve_maze((x_pos, y_pos - 1))
            self.solve_maze((x_pos, y_pos + 1))

        # Remove coordinate from solution stack
        self.path.pop()
        self.refresh_maze_screen()


def show_start_screen(screen):
    screen.fill(WHITE)
    screen.blit(FONT_LARGE.render("INTERESTED IN SOLVING SOME MAZES?", 1, BLACK),
                                  (50, 100))
    screen.blit(FONT_MED.render("PRESS NUMBER 1 to open first maze", 1, BLACK),
                                  (50, 400))
    screen.blit(FONT_MED.render("PRESS NUMBER 2 to open second maze", 1, BLACK),
                                  (50, 450))
    pygame.display.update()


def run():
    """
    Initialize maze and run game loop.
    """
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(TITLE)
    maze = Maze(screen)

    game_state = State.START
    key = None

    running = True
    # Run game loop as long as running is true.
    while running:

        # Check event type
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and game_state == State.START:
                    key = 1
                    game_state = State.INIT
                if event.key == pygame.K_2 and game_state == State.START:
                    key = 2
                    game_state = State.INIT
                if event.key == pygame.K_SPACE and game_state == State.HOLD:
                    screen.fill(WHITE)
                    maze.solve_maze(maze.find_start())
                    game_state = State.DONE
                if event.key == pygame.K_BACKSPACE and game_state == State.HOLD:
                    maze = Maze(screen)
                    game_state = State.START

        # Handle game states
        if game_state == State.START:
            show_start_screen(screen)

        elif game_state == State.INIT:
            maze.load_maze(FILE1 if key == 1 else FILE2)
            maze.refresh_maze_screen()
            text = FONT_LARGE.render("Hit SPACE to start!", 1, RED)
            screen.blit(text, (400, 10))
            pygame.display.update()
            game_state = State.HOLD

        elif game_state == State.RUNNING:
            maze.refresh_maze_screen()

        elif game_state == State.DONE:
            maze.display_results()
            game_state = State.HOLD


if __name__ == "__main__":
    run()
    pygame.quit()

import pygame

pygame.init()

TITLE = "Maze"
SIZE = (1000, 600)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

FILE1 = "mazes/maze-task-first.txt"
FILE2 = "mazes/maze-task-second.txt"

FONT_LARGE = pygame.font.SysFont("comicsans", 40, bold=True)
FONT_SMALL = pygame.font.SysFont("comicsans", 25, bold=True)

class Maze:
    def __init__(self, screen):
        self.screen = screen
        self.filename = None
        self.maze = []


    def draw_maze(self):
        pass


    def load_maze(self, filename):
        maze = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                maze.append([c for c in line])

        f.close()
        print(maze[0])
        print(maze[1])
        self.maze = maze


def refresh_maze_screen(screen, maze):
    text = FONT_SMALL.render("Hit SPACE to start!", 1, BLACK)
    screen.blit(text, (570, 100))
    maze.draw_maze()


def show_start_screen(screen):
    screen.fill(WHITE)
    screen.blit(FONT_LARGE.render("INTERESTED IN SOLVING SOME MAZES?", 1, BLACK),
                                  (50, 100))
    screen.blit(FONT_SMALL.render("PRESS NUMBER 1 to open first maze", 1, BLACK),
                                  (50, 400))
    screen.blit(FONT_SMALL.render("PRESS NUMBER 2 to open second maze", 1, BLACK),
                                  (50, 450))
    pygame.display.update()


def run():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(TITLE)

    show_start = True
    done = False
    key = None
    maze = Maze(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                    show_start = False
                if event.key == pygame.K_2:
                    key = 2
                    show_start = False
                if event.key == pygame.K_SPACE and show_start == False:
                    pygame.draw.rect(screen, WHITE, (560, 90, 440, 60), 0)
                    text = FONT_SMALL.render("Solving...", 1, BLACK)
                    screen.blit(text, (570, 100))
                    done = True
                if event.key == pygame.K_DELETE:
                    show_start = True
                    done = False

        if show_start:
            show_start_screen(screen)
        elif not done:
            screen.fill(WHITE)
            maze.load_maze(FILE1 if key == 1 else FILE2)
            refresh_maze_screen(screen, maze)
            pygame.display.update()


if __name__ == "__main__":
    run()
    pygame.quit()

import pygame


class Images:

    def __init__(self):
        self.width = 50
        self.background = pygame.image.load('background.gif')
        self.black = pygame.image.load('black.gif')
        self.white = pygame.image.load('white.gif')
        self.available = pygame.image.load('available.gif')
        self.blank = pygame.image.load('blank.gif')


class Chessboard:
    def __init__(self):
        self.width = 60
        self.row = self.col = 8
        self.margin = 100
        self.chesses = [[0 for _ in range(self.col)] for _ in range(self.row)]
        # set white chesses
        self.chesses[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.chesses[self.row // 2][self.col // 2] = 1
        # set black chesses
        self.chesses[self.row // 2][self.col // 2 - 1] = 2
        self.chesses[self.row // 2 - 1][self.col // 2] = 2


def draw(screen, images, chessboard):

    # draw backgroud
    screen.blit(images.background, (0, 0))

    # draw grid
    width = chessboard.width
    row = chessboard.row
    col = chessboard.col
    margin = chessboard.margin
    for i in range(row + 1):
        for j in range(col + 1):
            pygame.draw.line(screen, (0, 0, 0), 
                (margin + i * width, margin), 
                (margin + i * width, margin + col * width))
            pygame.draw.line(screen, (0, 0, 0), 
                (margin, margin + j * width), 
                (margin + row * width, margin + j * width))

    # draw chesses
    for i in range(row):
        for j in range(col):
            color = images.blank
            # if white chess
            if chessboard.chesses[i][j] == 1:
                color = images.white
            # if black chess
            elif chessboard.chesses[i][j] == 2:
                color = images.black
            screen.blit(color, (margin + j * width + width // 2 - images.width // 2,
                margin + i * width + width // 2 - images.width // 2))


def main():

    # set parameters
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-PVP')

    # load images
    images = Images()

    # main loop
    while True:

        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     screen.blit(black, pygame.mouse.get_pos())

        chessboard = Chessboard()
        draw(screen, images, chessboard)

        # update screen
        pygame.display.update()


if __name__ == "__main__":
    main()

import pygame
from Othello import *


def main():

    # set parameters
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 680

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-PVP')

    # load images
    images = Images()

    # init chessboard
    chessboard = Chessboard()
    chessboards = [chessboard]

    draw(screen, images, chessboard)
    pygame.display.update()

    # main loop
    while True:

        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    px, py = pygame.mouse.get_pos()
                    chessboard_new = setChess(chessboard, px, py)
                    if chessboard_new:
                        chessboard = chessboard_new
                        chessboards.append(chessboard)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_b:
                        if len(chessboards) > 1:
                            chessboards.pop(-1)
                            chessboard = chessboards[-1]
                
                # update screen
                draw(screen, images, chessboard)
                pygame.display.update()


if __name__ == "__main__":
    main()

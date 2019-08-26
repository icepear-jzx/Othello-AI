import pygame
from Othello import *


def setChess(chessboard, px, py):

    set_i = (py - chessboard.margin) // chessboard.width
    set_j = (px - chessboard.margin) // chessboard.width

    chessboard_new = None

    if 0 <= set_i < chessboard.row and 0 <= set_j < chessboard.col and \
    chessboard.chesses[set_i][set_j] == -1:
        # deep copy to new chessboard
        chessboard_new = Chessboard()
        for i in range(chessboard.row):
            for j in range(chessboard.col):
                chessboard_new.chesses[i][j] = chessboard.chesses[i][j]
                chessboard_new.stable[i][j] = chessboard.stable[i][j]
        # set chess
        chessboard_new.chesses[set_i][set_j] = chessboard.offense
        chessboard_new.offense = 3 - chessboard.offense
        # update
        chessboard_new.reverse(set_i, set_j)
        chessboard_new.updateAvailable()
        chessboard_new.updateStable()
        chessboard_new.updateCount()

        if chessboard_new.count_available == 0:
            chessboard_new.offense = 3 - chessboard_new.offense
            chessboard_new.updateAvailable()
            chessboard_new.updateCount()

    return chessboard_new



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
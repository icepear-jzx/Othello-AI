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
        # init stable chesses
        self.stable = [[0 for _ in range(self.col)] for _ in range(self.row)]
        # black on the offensive
        self.offense = 2
        # init white chesses
        self.chesses[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.chesses[self.row // 2][self.col // 2] = 1
        # init black chesses
        self.chesses[self.row // 2][self.col // 2 - 1] = 2
        self.chesses[self.row // 2 - 1][self.col // 2] = 2
        # init count
        self.count_black = self.count_white = 2
        self.count_available = 4
        self.count_stable = 0
        # init available pos
        self.updateAvailable()


    def updateAvailable(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.offense
        color_reverse = 3 - color
        # clear available pos
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == -1:
                    self.chesses[i][j] = 0
        # find available pos
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == self.offense:
                    for dx, dy in directions:
                        checking_i = i + dy
                        checking_j = j + dx
                        find_one_reverse_color = False
                        while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                            chess = self.chesses[checking_i][checking_j]
                            if chess == color_reverse:
                                checking_i += dy
                                checking_j += dx
                                find_one_reverse_color = True
                            elif chess == 0 and find_one_reverse_color:
                                self.chesses[checking_i][checking_j] = -1
                                break
                            else:
                                break


    def reverse(self, set_i, set_j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color_reverse = self.offense
        color = 3 - color_reverse
        for dx, dy in directions:
            checking_i = set_i + dy
            checking_j = set_j + dx
            find_one_reverse_color = False
            while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                chess = self.chesses[checking_i][checking_j]
                if chess == color_reverse:
                    checking_i += dy
                    checking_j += dx
                elif chess == color:
                    reversing_i = set_i + dy
                    reversing_j = set_j + dx
                    while (reversing_i, reversing_j) != (checking_i, checking_j):
                        self.chesses[reversing_i][reversing_j] = color
                        reversing_i += dy
                        reversing_j += dx
                    break
                else:
                    break


    def updateStable(self):
        pass


    def updateCount(self):
        self.count_black = self.count_white = self.count_available = self.count_stable = 0
        for i in range(self.row):
            for j in range(self.col):
                chess = self.chesses[i][j]
                if chess == 1:
                    self.count_white += 1
                elif chess == 2:
                    self.count_black += 1
                elif chess == -1:
                    self.count_available += 1
                elif self.stable[i][j] == 1:
                    self.count_stable += 1
        print(self.count_stable, self.count_available)


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

    return chessboard_new


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
            chess = chessboard.chesses[i][j]
            # if white chess
            if chess == 1:
                color = images.white
            # if black chess
            elif chess == 2:
                color = images.black
            elif chess == -1:
                color = images.available
            screen.blit(color, (margin + j * width + width // 2 - images.width // 2,
                                margin + i * width + width // 2 - images.width // 2))
    
    # draw count
    pos = margin * 2 + chessboard.width * col
    if chessboard.offense == 1:
        screen.blit(images.available, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.white, (pos, pos // 2 + images.width * 0.5))
    else:
        screen.blit(images.black, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.available, (pos, pos // 2 + images.width * 0.5))
    fontObj = pygame.font.Font(None, images.width)
    textSurfaceObj = fontObj.render(str(chessboard.count_black), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 - images.width)
    screen.blit(textSurfaceObj, textRectObj)
    textSurfaceObj = fontObj.render(str(chessboard.count_white), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 + images.width)
    screen.blit(textSurfaceObj, textRectObj)


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

    # init chessboard
    chessboard = Chessboard()
    chessboards = [chessboard]

    # main loop
    while True:

        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                px, py = pygame.mouse.get_pos()
                chessboard = setChess(chessboard, px, py)
                if chessboard:
                    chessboards.append(chessboard)

        draw(screen, images, chessboard)

        # update screen
        pygame.display.update()


if __name__ == "__main__":
    main()

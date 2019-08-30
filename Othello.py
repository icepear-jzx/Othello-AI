import pygame


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
        self.count_stable_black = 0
        self.count_stable_white = 0
        self.count_total_stable_direct_black = 0
        self.count_total_stable_direct_white = 0
        # init available pos
        self.available = []
        self.updateAvailable()


    def updateAvailable(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.offense
        color_reverse = 3 - color
        # clear available pos
        self.available = []
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
                                # find available pos, add it into self.available
                                self.available.append((checking_i, checking_j))
                                break
                            else:
                                break


    # reverse chesses
    def reverse(self, set_i, set_j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color_reverse = self.offense
        color = 3 - color_reverse
        for dx, dy in directions:
            checking_i = set_i + dy
            checking_j = set_j + dx
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
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        find_new_stable_chess = True
        while find_new_stable_chess:
            find_new_stable_chess = False
            self.count_total_stable_direct_black = 0
            self.count_total_stable_direct_white = 0
            for i in range(self.row):
                for j in range(self.col):
                    if (self.chesses[i][j] == 1 or self.chesses[i][j] == 2) and not self.stable[i][j]:
                        count_stable_direction = 0
                        for direction in directions:
                            if self.checkDirectionStable(i, j, direction):
                                count_stable_direction += 1
                        if count_stable_direction == 4:
                            find_new_stable_chess = True
                            self.stable[i][j] = 1
                        else:
                            if self.chesses[i][j] == 1:
                                self.count_total_stable_direct_white += count_stable_direction
                            elif self.chesses[i][j] == 2:
                                self.count_total_stable_direct_black += count_stable_direction


    def checkDirectionStable(self, i, j, direction):
        directions = [direction, (-direction[0], -direction[1])]
        color = self.chesses[i][j]
        color_reverse = 3 - color
        count_tmp = 0
        for dx, dy in directions:
            find_unstable_chess = False
            checking_i = i + dy
            checking_j = j + dx
            while True:
                if not (0 <= checking_i < self.row and 0 <= checking_j < self.col):
                    if find_unstable_chess:
                        count_tmp += 1
                        break
                    else:
                        return True
                if self.chesses[checking_i][checking_j] == color:
                    if self.stable[checking_i][checking_j]:
                        return True
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                elif self.chesses[checking_i][checking_j] == color_reverse:
                    if self.stable[checking_i][checking_j]:
                        count_tmp += 1
                        break
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                else:
                    break
        if count_tmp == 2:
            return True
        else:
            return False


    def updateCount(self):
        self.count_black = self.count_white = 0
        self.count_available = 0
        self.count_stable_white = self.count_stable_black = 0
        for i in range(self.row):
            for j in range(self.col):
                chess = self.chesses[i][j]
                if chess == 1:
                    self.count_white += 1
                elif chess == 2:
                    self.count_black += 1
                elif chess == -1:
                    self.count_available += 1
                if self.stable[i][j] == 1:
                    if self.chesses[i][j] == 1:
                        self.count_stable_white += 1
                    elif self.chesses[i][j] == 2:
                        self.count_stable_black += 1
    

    def copy(self):
        chessboard_new = Chessboard()
        chessboard_new.offense = self.offense
        chessboard_new.available = [item for item in self.available]
        for i in range(self.row):
            for j in range(self.col):
                chessboard_new.chesses[i][j] = self.chesses[i][j]
                chessboard_new.stable[i][j] = self.stable[i][j]
        chessboard_new.count_black = self.count_black
        chessboard_new.count_white = self.count_white
        chessboard_new.count_available = self.count_available
        chessboard_new.count_stable_black = self.count_stable_black
        chessboard_new.count_stable_white = self.count_stable_white
        chessboard_new.count_total_stable_direct_black = self.count_total_stable_direct_black
        chessboard_new.count_total_stable_direct_white = self.count_total_stable_direct_white
        return chessboard_new


def setChess(chessboard, px, py):

    set_i = (py - chessboard.margin) // chessboard.width
    set_j = (px - chessboard.margin) // chessboard.width

    chessboard_new = None

    if 0 <= set_i < chessboard.row and 0 <= set_j < chessboard.col and \
    chessboard.chesses[set_i][set_j] == -1:
        # deep copy to new chessboard
        chessboard_new = chessboard.copy()
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


class Images:

    def __init__(self):
        self.width = 50
        self.background = pygame.image.load('images/background.gif')
        self.black = pygame.image.load('images/black.gif')
        self.white = pygame.image.load('images/white.gif')
        self.available = pygame.image.load('images/available.gif')
        self.blank = pygame.image.load('images/blank.gif')


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

    # draw text
    textSurfaceObj = fontObj.render("Press 'b' to undo", True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + 100, pos - 150)
    screen.blit(textSurfaceObj, textRectObj)

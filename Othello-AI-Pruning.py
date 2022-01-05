import pygame
from Othello import *


class ChessboardTreeNode:

    def __init__(self, chessboard):
        self.parent = None
        # self.kids: {(i, j): node}
        self.kids = {}
        self.chessboard = chessboard

    def getScore(self):
        chessboard = self.chessboard
        return 100 * (chessboard.count_stable_white - chessboard.count_stable_black) \
            + (chessboard.count_total_stable_direct_white
               - chessboard.count_total_stable_direct_black)


class ChessboardTree:

    def __init__(self, node):
        self.root = node
        # self.expandLayer >= 2
        self.expandLayer = 5

    def expandTree(self):
        node = self.root
        # expand the first layer
        for i, j in node.chessboard.available:
            if (i, j) not in node.kids:
                chessboard_new = setChessAI(node.chessboard, i, j)
                node_new = ChessboardTreeNode(chessboard_new)
                node.kids[(i, j)] = node_new
                node_new.parent = node

    def findBestChess(self, player_color):
        scores = {}
        alpha = -6400
        for key in self.root.kids:
            score = self.MaxMin(self.root.kids[key], player_color,
                                self.expandLayer - 1, alpha)
            scores.update({key: score})
            if alpha < score:
                alpha = score
        if not scores:
            return (-1, -1)
        max_key = max(scores, key=scores.get)
        min_key = min(scores, key=scores.get)
        print(scores[min_key], scores[max_key])
        return max_key

    def MaxMin(self, node, player_color, layer, pruning_flag):
        if layer and node.chessboard.available:
            # min layer
            if node.chessboard.offense == player_color:
                beta = 6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, beta)
                    else:
                        # count += 1
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, beta)
                    if score <= pruning_flag:
                        beta = score
                        break
                    if beta > score:
                        beta = score
                # print('layer:', layer, 'min:', beta, 'pruning:', pruning_flag)
                return beta
            # max layer
            else:
                alpha = -6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, alpha)
                    else:
                        # count += 1
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, alpha)
                    if score >= pruning_flag:
                        alpha = score
                        break
                    if alpha < score:
                        alpha = score
                # print('layer:', layer, 'max:', alpha, 'pruning:', pruning_flag)
                return alpha
        else:
            node.chessboard.updateStable()
            node.chessboard.updateCount()
            score = node.getScore()
            # print('layer:', layer, 'leaf:', node.score)
            return score


def setChessAI(chessboard, set_i, set_j):

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
        # chessboard_new.updateStable()
        chessboard_new.updateCount()

        if chessboard_new.count_available == 0:
            chessboard_new.offense = 3 - chessboard_new.offense
            chessboard_new.updateAvailable()
            # chessboard_new.updateCount()

    return chessboard_new


def main():

    # set parameters
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 680
    player_color = 2  # black

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-AI-Pruning')

    # load images
    images = Images()

    # init chessboard
    chessboard = Chessboard()

    # init tree
    node = ChessboardTreeNode(chessboard)
    chessboardTree = ChessboardTree(node)
    chessboardTree.expandTree()

    draw(screen, images, chessboard)
    pygame.display.update()

    # main loop
    while True:

        # catch events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                set_i = set_j = -1
                if chessboard.offense == player_color:
                    px, py = pygame.mouse.get_pos()
                    set_i = (py - chessboard.margin) // chessboard.width
                    set_j = (px - chessboard.margin) // chessboard.width
                else:
                    set_i, set_j = chessboardTree.findBestChess(player_color)
                if (set_i, set_j) in chessboard.available:
                    chessboardTree.root = chessboardTree.root.kids[(
                        set_i, set_j)]
                    chessboard = chessboardTree.root.chessboard
                    # update screen
                    draw(screen, images, chessboard)
                    pygame.display.update()
                    # expand only 1 layer
                    chessboardTree.expandTree()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    if chessboardTree.root.parent:
                        chessboardTree.root = chessboardTree.root.parent
                        chessboard = chessboardTree.root.chessboard
                # update screen
                draw(screen, images, chessboard)
                pygame.display.update()


if __name__ == "__main__":
    main()

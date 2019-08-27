import pygame
from Othello import *


class ChessboardTreeNode:
    
    def __init__(self, chessboard):
        self.parent = None
        # self.kids: {(i, j): node}
        self.kids = {}
        self.chessboard = chessboard
        self.score = 100 * (chessboard.count_stable_white - chessboard.count_stable_black) \
            + (chessboard.count_total_stable_direct_white 
            - chessboard.count_total_stable_direct_black)


class ChessboardTree:

    def __init__(self, node):
        self.root = node
        # self.expandLayer >= 1
        # the first expansion will expand self.expandLayer layers
        # then self.exapndLayer will be set to 1
        # so that the prediction is always ahead of current chessboard for 
        # self.expandLayer layers
        self.expandLayer = 3
        self.greedyNum = 0
    

    # expand self.expandLayer layers using BFS
    # then expand greedily for self.greedyNum nodes
    def expandTree(self):
        BFS_list = []
        BFS_list_next = []
        self.DFS(self.root, BFS_list)
        # expand layer
        for _ in range(self.expandLayer):
            for node in BFS_list:
                for i, j in node.chessboard.available:
                    chessboard_new = setChessAI(node.chessboard, i ,j)
                    node_new = ChessboardTreeNode(chessboard_new)
                    node.kids[(i, j)] = node_new
                    BFS_list_next.append(node_new)
            BFS_list = BFS_list_next
            BFS_list_next = []
        self.expandLayer = 1
        # print(len(BFS_list))
        # expand greedily
        # BFS_list.sort()
        
    
    def DFS(self, node, BFS_list):
        if node.kids:
            for key in node.kids:
                self.DFS(node.kids[key], BFS_list)
        else:
            BFS_list.append(node)


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
    player_color = 2 # black

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-PVP')

    # load images
    images = Images()

    # init chessboard
    chessboard = Chessboard()
    chessboards = [chessboard]

    # init tree
    node = ChessboardTreeNode(chessboard)
    chessboardTree = ChessboardTree(node)

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
                px, py = pygame.mouse.get_pos()
                set_i = (py - chessboard.margin) // chessboard.width
                set_j = (px - chessboard.margin) // chessboard.width
                if (set_i, set_j) in chessboard.available:
                    chessboardTree.expandTree()
                    chessboardTree.root = chessboardTree.root.kids[(set_i, set_j)]
                    chessboard = chessboardTree.root.chessboard
                        
                # update screen
                draw(screen, images, chessboard)
                pygame.display.update()

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
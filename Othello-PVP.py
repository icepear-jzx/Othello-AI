import pygame


def main():

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Othello-PVP')

    background = pygame.image.load('background.gif')

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()

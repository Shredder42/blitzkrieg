import os
import pygame
from battle_spaces import BattleSpace

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 1000
ESPRESSO = (75, 56, 42) # table top color

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blitzkrieg!')

board = pygame.image.load(os.path.join('images', 'blitzkrieg_game_board_italian.jpg'))
board = pygame.transform.scale_by(board, 2)
surface = pygame.Surface((1060, 1000), pygame.SRCALPHA) # need for creating transparent rect
clock = pygame.time.Clock()

battle_space_1 = BattleSpace(196, 207, 'production')

# def main():
run = True

while run:
    screen.fill(ESPRESSO)
    screen.blit(board, (0,0))
    screen.blit(surface, (0,0))
    battle_space_1.draw(surface)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

    clock.tick(60)

# if __name__ == '__main__':
#     main()



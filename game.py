import os
import pygame
from battle_spaces import BattleSpace
from tokens import AlliedToken

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

battle_space_1 = BattleSpace(196, 207, 'production', 'west_europe', 1)
allied_1 = AlliedToken(50, 800, 'allied_army_1.png', 1)
allied_2 = AlliedToken(120, 800, 'allied_army_2.png', 2)

# def main():
run = True
moving = False
while run:
    screen.fill(ESPRESSO)
    screen.blit(board, (0,0))
    screen.blit(surface, (0,0))
    battle_space_1.draw(surface)
    allied_1.draw(screen)
    allied_2.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            
            if allied_1.rect.collidepoint(pos):
                print('clicked on tile')
        #         # print(tile1.rect)
                moving = True
            
        elif event.type == pygame.MOUSEMOTION:
            if moving:
                allied_1.rect.move_ip(event.rel)

        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
            if allied_1.rect.collidepoint(battle_space_1.rect.center):
                allied_1.rect.center = battle_space_1.rect.center



    pygame.display.flip()

    clock.tick(60)

# if __name__ == '__main__':
#     main()



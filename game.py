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

battle_space_1 = BattleSpace(196, 207, 'production', 'sea', 'west_europe', 1)
allied_1 = AlliedToken('army', 1, 50, 800, 'allied_army_1.png')
allied_2 = AlliedToken('navy', 2, 120, 800, 'allied_navy_2.png')
allied_3 = AlliedToken('navy', 3, 190, 800, 'allied_navy_3.png')
allied_4 = AlliedToken('airforce', 1, 260, 800, 'allied_airforce_1.png')

# def clicked_token(token):
#     if token.rect.collidepoint(pos):
#         print('clicked on token')
#         token.moving = True

# def move_token(token):
#     if token.moving:
#         token.rect.move_ip(event.rel)

# def token_original_location(token):
#     x = token.rect.x
#     y = token.rect.y
#     return x, y

# def match_type_and_unit(token, space):
#     if (token.unit == 'army' and space.type in ('land', 'both')) or \
#     (token.unit == 'navy' and space.type in ('sea', 'both')) or \
#     token.unit == 'airforce':
#         return True

#     else:
#         return False

# def place_token(original_x, original_y, token, space):
#     if token.moving:
#         if (match_type_and_unit(token, space)) and (token.rect.collidepoint(space.rect.center) and not space.occupied):
#                 token.rect.center = space.rect.center
#                 space.occupied = True

#         else:
#             token.rect.x = original_x
#             token.rect.y = original_y

#         token.moving = False 

           


def main():
    run = True
    moving = False
    while run:
        screen.fill(ESPRESSO)
        screen.blit(board, (0,0))
        screen.blit(surface, (0,0))
        battle_space_1.draw(surface)
        allied_1.draw(screen)
        allied_2.draw(screen)
        allied_3.draw(screen)
        allied_4.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)


                allied_1.clicked_token(pos)
                allied_2.clicked_token(pos)
                allied_3.clicked_token(pos)
                allied_4.clicked_token(pos)
            
            elif event.type == pygame.MOUSEMOTION:
                allied_1.move_token(event)
                allied_2.move_token(event)
                allied_3.move_token(event)
                allied_4.move_token(event)


            elif event.type == pygame.MOUSEBUTTONUP:
                allied_1.place_token(battle_space_1)
                allied_2.place_token(battle_space_1)
                allied_3.place_token(battle_space_1)
                allied_4.place_token(battle_space_1)

        pygame.display.flip()

        clock.tick(60)



if __name__ == '__main__':
    main()



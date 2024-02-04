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

def token_original_location(piece):
    x = piece.rect.x
    y = piece.rect.y
    return x, y

def match_type_and_unit(piece, space):
    # match = None
    if (piece.unit == 'army' and space.type == 'land') or \
    (piece.unit == 'navy' and space.type == 'sea') or \
    piece.unit == 'airforce':
        return True

    else:
        return False

def place_piece(x, y, piece, space):
    if match_type_and_unit(piece, space):
        if piece.rect.collidepoint(space.rect.center):
            piece.rect.center = space.rect.center
        else:
            piece.rect.x = x
            piece.rect.y = y 

    else:
        piece.rect.x = x
        piece.rect.y = y 

           



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
            
            if allied_2.rect.collidepoint(pos):
                print('clicked on tile')
        #         # print(tile1.rect)
                moving = True
                original_x, original_y = token_original_location(allied_2)

            
        elif event.type == pygame.MOUSEMOTION:
            if moving:
                allied_2.rect.move_ip(event.rel)

        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
            place_piece(original_x, original_y, allied_2, battle_space_1)
            # if allied_1.rect.collidepoint(battle_space_1.rect.center):
            #     allied_1.rect.center = battle_space_1.rect.center



    pygame.display.flip()

    clock.tick(60)

# if __name__ == '__main__':
#     main()



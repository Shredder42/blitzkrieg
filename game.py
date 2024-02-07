import os
import pygame
from gameboard import GameBoard, BattleSpace, Theater, Campaign
from tokens import Token
from manage_tokens import PlayerHand, TokenBag

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



theaters = {
    'west_europe': Theater(),
    'pacific': Theater(),
    'east_europe': Theater(),
    'africa': Theater(),
    'Asia': Theater()
}
campaigns = {
    'northern_west_europe': Campaign(),
    'central_west_europe': Campaign(),
    'southern_west_europe': Campaign(),
    'northern_pacific': Campaign(),
    'central_pacific': Campaign(),
    'southern_pacific': Campaign(),
    'northern_east_europe': Campaign(),
    'central_east_europe': Campaign(),
    'southern_east_europe': Campaign(),
    'northern_africa': Campaign(),
    'southern_africa': Campaign(),
    'northern_asia': Campaign(),
    'southern_asia': Campaign()
}


game_board = GameBoard(theaters, campaigns)

# allied_1 = Token('allied', 'army', 1, 50, 800, 'allied_army_1.png')
# allied_2 = Token('allied', 'navy', 2, 120, 800, 'allied_navy_2.png')
# allied_3 = Token('allied', 'navy', 3, 190, 800, 'allied_navy_3.png')
# allied_4 = Token('allied', 'airforce', 1, 260, 800, 'allied_airforce_1.png')

bag = TokenBag()
# print(bag.allied_token_bag)
hand = PlayerHand(bag.allied_token_bag)
for token in hand.hand_list:
    print(f'{token.unit} value {token.value}')


def main():
    run = True
    moving = False
    while run:
        screen.fill(ESPRESSO)
        screen.blit(board, (0,0))
        screen.blit(surface, (0,0))
        for space in game_board.battle_spaces:
            space.draw(surface)
        for token in game_board.placed_tokens:
            token.draw(screen)
        # allied_1.draw(screen)
        # allied_2.draw(screen)
        # allied_3.draw(screen)
        # allied_4.draw(screen)
        for token in hand.hand_list:
            token.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)


                # allied_1.clicked_token(pos)
                # allied_2.clicked_token(pos)
                # allied_3.clicked_token(pos)
                # allied_4.clicked_token(pos)
                for token in hand.hand_list:
                    token.clicked_token(pos)
            
            elif event.type == pygame.MOUSEMOTION:
                # allied_1.move_token(event)
                # allied_2.move_token(event)
                # allied_3.move_token(event)
                # allied_4.move_token(event)
                for token in hand.hand_list:
                    token.move_token(event)



            elif event.type == pygame.MOUSEBUTTONUP:
                # allied_1.place_token(game_board.battle_spaces[1])
                # allied_2.place_token(game_board.battle_spaces[1])
                # allied_3.place_token(game_board.battle_spaces[1])
                # allied_4.place_token(game_board.battle_spaces[1])west_europe
                for token in hand.hand_list:
                    token.place_token(game_board.battle_spaces, hand.hand_list, game_board.placed_tokens)

        pygame.display.flip()

        clock.tick(60)

    for token in hand.hand_list:
        print(token.rect)

if __name__ == '__main__':
    main()



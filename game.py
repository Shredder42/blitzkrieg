import os
import pygame
from gameboard import GameBoard, BattleSpace, Theater, Campaign
from tokens import Token
from manage_tokens import PlayerHand, TokenBags

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 900
ESPRESSO = (75, 56, 42) # table top color

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blitzkrieg!')

board = pygame.image.load(os.path.join('images', 'blitzkrieg_game_board_italian.jpg'))
board = pygame.transform.scale_by(board, 2)
surface = pygame.Surface((1060, 900), pygame.SRCALPHA) # need for creating transparent rect
clock = pygame.time.Clock()

'''
blitz tokens
closing campaigns
closing theaters
fix up axis & ally hands - is this done????
turns - keep working on them
    only switch turn if token is placed - this is big
    check for victory
use the side token attribute in conjunction with turns to determine who can play token and where scores go
    assign the side to the special tokens when they are drawn into the player hand
figure out playing over internet?
check for correct victory point tracking after getting closing campaigns implemented
test task force
'''

theaters = {
    'west_europe': Theater('west_europe', 284, 179),
    'pacific': Theater('pacific', 239, 446),
    'east_europe': Theater('east_europe', 816, 110),
    'africa': Theater('africa', 716, 381),
    'asia': Theater('asia', 817, 589)
}
campaigns = {
    'northern_west_europe': Campaign('northern_west_europe', 1, True),
    'central_west_europe': Campaign('central_west_europe', 2,),
    'southern_west_europe': Campaign('southern_west_europe', 3),
    'northern_pacific': Campaign('northern_pacific', 1, True),
    'central_pacific': Campaign('central_pacific', 2),
    'southern_pacific': Campaign('southern_pacific', 3),
    'northern_east_europe': Campaign('northern_east_europe', 1, True),
    'central_east_europe': Campaign('central_east_europe', 2),
    'southern_east_europe': Campaign('southern_east_europe', 3),
    'northern_africa': Campaign('northern_africa', 1, True),
    'southern_africa': Campaign('southern_africa', 2),
    'northern_asia': Campaign('northern_asia', 1, True),
    'southern_asia': Campaign('southern_asia', 2)
}


game_board = GameBoard(theaters, campaigns)

# campaigns['northern_west_europe'].add_spaces_to_campaign(game_board.battle_spaces[0:3])
for campaign in campaigns:
    campaigns[campaign].add_spaces_to_campaign(game_board)
# print(campaigns['northern_west_europe'].spaces)
# print(campaigns['southern_west_europe'].spaces)

for theater in theaters:
    theaters[theater].add_campaigns_to_theater(campaigns)
# theaters['west_europe'].add_campaigns_to_theater(campaigns)
# print(theaters['west_europe'].campaigns)
# print(theaters['pacific'].campaigns)


# allied_1 = Token('allied', 'army', 1, 50, 800, 'allied_army_1.png')
# allied_2 = Token('allied', 'navy', 2, 120, 800, 'allied_navy_2.png')
# allied_3 = Token('allied', 'navy', 3, 190, 800, 'allied_navy_3.png')
# allied_4 = Token('allied', 'airforce', 1, 260, 800, 'allied_airforce_1.png')

bags = TokenBags()
# print(bag.allied_token_bag)
allied_hand = PlayerHand(bags.allied_token_bag, 'allied')
axis_hand = PlayerHand(bags.axis_token_bag, 'axis')
# for token in allied_hand.hand_list:
#     print(f'{token.unit} value {token.value}')
# print('\n')
# print('axis hand')
# for token in axis_hand.hand_list:
#     print(f'{token.unit} value {token.value}')
# print(bags.axis_token_bag)
# for token in bags.axis_token_bag:
#     print(token.special)
    
def end_turn(turn):
    if turn == 'allied':
        game_board.industrial_production(allied_hand)
        turn = 'axis'
    elif turn == 'axis':
        game_board.industrial_production(axis_hand)
        turn = 'allied'
    print('Turn:', turn)
    return turn


def main():
    run = True
    # moving = False
    played_space = None
    turn = 'allied' # this will need to be changed to axis eventually
    blitz = False
    while run:
        screen.fill(ESPRESSO)
        screen.blit(board, (0,0))
        screen.blit(surface, (0,0))
        for space in game_board.battle_spaces:
            space.draw(surface)
        for button in game_board.theater_buttons:
            button.draw(surface)
        game_board.draw_symbols(screen)
        for theater in theaters:
            theaters[theater].draw_track_marker(screen)
        for token in game_board.placed_tokens:
            token.draw(screen)
        # allied_1.draw(screen)
        # allied_2.draw(screen)
        # allied_3.draw(screen)
        # allied_4.draw(screen)
        for token in allied_hand.hand_list:
            token.draw(screen)
        for token in axis_hand.hand_list:
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
                if turn == 'allied':
                    for token in allied_hand.hand_list:
                        token.clicked_token(pos, game_board)
                elif turn == 'axis':
                    for token in axis_hand.hand_list:
                        token.clicked_token(pos, game_board)        
            
            elif event.type == pygame.MOUSEMOTION:
                # allied_1.move_token(event)
                # allied_2.move_token(event)
                # allied_3.move_token(event)
                # allied_4.move_token(event)
                if turn == 'allied':
                    for token in allied_hand.hand_list:
                        token.move_token(event)
                elif turn == 'axis':
                    for token in axis_hand.hand_list:
                        token.move_token(event)


            elif event.type == pygame.MOUSEBUTTONUP:
                # allied_1.place_token(game_board.battle_spaces[1])
                # allied_2.place_token(game_board.battle_spaces[1])
                # allied_3.place_token(game_board.battle_spaces[1])
                # allied_4.place_token(game_board.battle_spaces[1])west_europe
                # blitz = True

                if turn == 'axis':
                    for token in axis_hand.hand_list:
                        if token.moving:
                            played_space = token.place_token(game_board, axis_hand, allied_hand, bags.research_bag, bags.axis_token_bag, bags.allied_token_bag, theaters, turn)
                            if token.effect == 'blitz':
                                blitz = True
                            else:
                                blitz = False
                            break


                    if played_space:
                        if played_space.effect == 'strategic':                            
                            for button in game_board.theater_buttons:
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    played_space = None
                                    if not blitz:
                                        turn = end_turn(turn)
                                    else:
                                        print('place another token')
                                    break
                            else:
                                print('pick a theater')
                                
                        else:
                            if not blitz:
                                turn = end_turn(turn)
                            else:
                                print('place another token')


                elif turn == 'allied':
                    for token in allied_hand.hand_list:
                        if token.moving:
                            played_space = token.place_token(game_board, allied_hand, axis_hand, bags.research_bag, bags.allied_token_bag, bags.axis_token_bag, theaters, turn)
                            if token.effect == 'blitz':
                                blitz = True
                            else:
                                blitz = False
                            break


                    if played_space:
                        if played_space.effect == 'strategic':
                            for button in game_board.theater_buttons :
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    played_space = None
                                    if not blitz:
                                        turn = end_turn(turn)
                                    else:
                                        print('place another token')
                                    break
                            else:
                                print('pick a theater')
                                
                        else:
                            if not blitz:
                                turn = end_turn(turn)
                            else:
                                print('place another token')


               

        pygame.display.flip()

        clock.tick(60)

    for token in allied_hand.hand_list:
        print(token.rect)
    print('\n')
    for token in axis_hand.hand_list:
        print(f'{token.unit} value {token.value}')
    print(len(axis_hand.hand_list))
    # print(bags.axis_token_bag)
    # print(played_space.effect)
    # for token in bags.axis_token_bag:
    #     print(token.special)

    print('allied victory points:', game_board.allied_victory_points)
    print(turn)


if __name__ == '__main__':
    main()



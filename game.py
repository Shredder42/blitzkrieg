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
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # need for creating transparent rect
clock = pygame.time.Clock()

'''
closing theaters
    copy to allies
blitz has to be in same theater - coded but check a little more
render instructions on screen
add pauses for time to read between moves
only display tiles for one side at a time


nuclear bomb moved back axis score on theater with all tiles placed - will close the theater when tiles
    placed or score reaches end - amke sure it doesn't move it theater closed
figure out playing over internet? - start with pass and play for now
'''

theaters = {
    'west_europe': Theater('west_europe', 284, 179),
    'pacific': Theater('pacific', 239, 446),
    'east_europe': Theater('east_europe', 816, 110),
    'africa': Theater('africa', 716, 381),
    'asia': Theater('asia', 817, 589)
}
campaigns = {
    'northern_west_europe': Campaign('northern_west_europe', 2, True),
    'central_west_europe': Campaign('central_west_europe', 3,),
    'southern_west_europe': Campaign('southern_west_europe', 5),
    'northern_pacific': Campaign('northern_pacific', 2, True),
    'central_pacific': Campaign('central_pacific', 3),
    'southern_pacific': Campaign('southern_pacific', 5),
    'northern_east_europe': Campaign('northern_east_europe', 2, True),
    'central_east_europe': Campaign('central_east_europe', 3),
    'southern_east_europe': Campaign('southern_east_europe', 6),
    'northern_africa': Campaign('northern_africa', 3, True),
    'southern_africa': Campaign('southern_africa', 5),
    'northern_asia': Campaign('northern_asia', 2, True),
    'southern_asia': Campaign('southern_asia', 4)
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
    
def end_turn(turn, played_space, game_board, axis_hand, allied_hand, run):
    if turn == 'allied':
        # check for winning on points
        winner = check_for_victory_points(game_board)
        # if game_board.axis_victory_points >= 25 or game_board.allied_victory_points >= 25:
        #     if game_board.axis_victory_points > game_board.allied_victory_points:
        if winner == 'axis':
            print(f'Axis forces win the war: {game_board.axis_victory_points} - {game_board.allied_victory_points}')
            run = False
        elif winner == 'allies':
            print(f'Allied forces win the war: {game_board.allied_victory_points} - {game_board.axis_victory_points}')
            run = False
        else:
            game_board.industrial_production(allied_hand)
            if check_for_victory_availabilty(game_board, axis_hand.hand_list):
                turn = 'axis'
            else:
                print('Allied forces win the war. Axis commander out of options')
                run = False
    elif turn == 'axis':
        game_board.industrial_production(axis_hand)
        if check_for_victory_availabilty(game_board, allied_hand.hand_list):
            turn = 'allied'
        else:
            print('Axis forces win the war. Allied commander out of options')
            run = False

    played_space = None
    print('Turn:', turn)
    return turn, played_space, run

def check_for_victory_points(game_board):
    winner = None
    if game_board.axis_victory_points >= 25 or game_board.allied_victory_points >= 25:
        if game_board.axis_victory_points > game_board.allied_victory_points:
            winner = 'axis'
        else:
            winner = 'allies'

    return winner

# keep looking at this function
# also need to lose the game if hand is empty - this might already work
def check_for_victory_availabilty(game_board, hand):
    available_list = []
    available_move = True
    # if not hand:
    #     return False
    for space in game_board.battle_spaces:
        if not space.occupied and space.theater.available and space.campaign.available:
            available_list.append(space)
    # for space in available_list:
        # print(space.campaign.campaign)
        # print(space.theater.theater)
        # print(space.effect)
    for token in hand:
        print(token.unit)
        print(token.value)
        if token.effect == 'scientist':
            for theater in game_board.theaters.values():
                if theater.available:
                    available_move = True
                    break
        else:
            for space in available_list:
                if token.effect == 'spy' and game_board.placed_tokens[-1].match_type_and_unit(space):
                    available_move = True
                    break
                elif token.match_type_and_unit(space):
                    available_move = True
                    break
        if available_move:
            break
    else:
        available_move = False
    # if not hand.hand_list:
    #     available_move = False
        
    print(available_move)

    return available_move




def main():
    run = True
    # moving = False
    played_space = None
    turn = 'axis'
    blitz = False
    task_force = False
    closed_theater = False
    strategic = False
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
        if len(game_board.placed_tokens) > 1:
            for token in game_board.placed_tokens[1:]:
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

                if turn == 'allied':
                    for token in allied_hand.hand_list:
                        token.clicked_token(pos, game_board)
                elif turn == 'axis':
                    for token in axis_hand.hand_list:
                        token.clicked_token(pos, game_board)        
            
            elif event.type == pygame.MOUSEMOTION:
                if turn == 'allied':
                    for token in allied_hand.hand_list:
                        token.move_token(event)
                elif turn == 'axis':
                    for token in axis_hand.hand_list:
                        token.move_token(event)


            elif event.type == pygame.MOUSEBUTTONUP:

                if turn == 'axis':
                    for token in axis_hand.hand_list:
                        if token.moving:
                            played_space, closed_theater, available_list = token.place_token(game_board, axis_hand, allied_hand, bags.research_bag, bags.axis_token_bag, bags.allied_token_bag, theaters, turn)
                            if token.effect == 'blitz':
                                blitz = True
                            else:
                                blitz = False
                            if token.effect == 'task_force':
                                task_force = True
                            else:
                                task_force = False
                            # if available_list:
                            #     closed_theater = True
                            # else:
                            #     closed_theater = False
                            print('closed theater', closed_theater)
                            print(available_list)
                            # if played_space:
                            #     print(played_space.effect)
                            #     print(played_space.theater.theater)
                            #     print(played_space.campaign.campaign)
                            #     print(played_space.effect_value)
                            break

                        # print(token.effect)
                    if played_space and not task_force and not closed_theater:
                        if played_space.effect == 'strategic':                            
                            for button in game_board.theater_buttons:
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    # played_space = None
                                    if not blitz:
                                        turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                                    elif blitz :
                                        print('place another token')                                       
                                    break
                            else:
                                print('pick a theater')
                                
                        else:
                            # played_space = None
                            if not blitz and not closed_theater:
                                # print(played_space.effect)
                                # print(played_space.theater.theater)
                                # print(played_space.campaign.campaign)
                                # print(played_space.effect_value)
                                turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                            elif blitz and not closed_theater:
                                print('place another token')
                    elif played_space and not closed_theater:
                        turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                    if closed_theater:
                        # print(played_space.effect)
                        # print(played_space.theater.theater)
                        # print(played_space.campaign.campaign)
                        # print(played_space.effect_value)
                        if played_space:
                            if played_space.effect == 'strategic': 
                                print(played_space.effect)                           
                                for button in game_board.theater_buttons:
                                    if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                        played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                        played_space = None                                  
                                        break
                                else:
                                    print('pick a theater')
                        print('theater closed - select all other battle spaces')
                        # clickable_spaces = len(available_list)
                        # count = 0
                        # for i in range()
                        # strategic = False
                        for battle_space in available_list:
                            if battle_space.rect.collidepoint(pos) and not strategic:
                                if battle_space.effect == 'propaganda':
                                    for i in range(battle_space.effect_value):
                                        game_board.propaganda(turn)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'production':
                                    game_board.industrial_production(axis_hand)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'imp_production':
                                    for i in range(battle_space.effect_value):
                                        game_board.industrial_production(axis_hand)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                # if battle_space.effect == 'tactical':
                                #     game_board.tactical_advantage(battle_space.theater, battle_space.effect_value, turn)
                                #     available_list.remove(battle_space)
                                if battle_space.effect == 'bombing':
                                    game_board.bombing(allied_hand, bags.allied_token_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'research':
                                    game_board.research(bags.axis_token_bag, bags.research_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'imp_research':
                                    for i in range(battle_space.effect_value):
                                        game_board.research(bags.axis_token_bag, bags.research_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'res_industry':
                                    print('clicked on res ind')
                                    game_board.research_industry(axis_hand, bags.research_bag, turn)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'strategic': 
                                    strategic = True
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                occupied_list = []
                                for space in battle_space.campaign.spaces:
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)
                                if all(occupied_list):
                                    for i in range(battle_space.campaign.victory_points):
                                        game_board.propaganda(turn)
                                        # print(battle_space.campaign.campaign)
                                        # print(occupied_list)
                                        # print('ran propaganda')
                                # if battle_space.occupied:
                                #     available_list.remove(battle_space)
                        if strategic: # think about how to get this into the above loop
                            # may have to reorder the loop - maybe put the collide point within each space
                            for button in game_board.theater_buttons: 
                                if button.rect.collidepoint(pos) and (button.theater != battle_space.theater.theater) and strategic:
                                    # print(battle_space.theater.theater)
                                    # print(battle_space.effect_value)
                                    battle_space.theater.move_track_marker_strategic(theaters, battle_space.effect_value, button.theater, turn)
                                    # print(battle_space.theater.theater)
                                    # print(battle_space.effect)
                                    # print(battle_space.effect_value)
                                    strategic = False
                                    # available_list.remove(battle_space)
                                    break
                            else:
                                print('pick a theater')
                        # new campaign points here
                        # occupied_list = []
                        # for item in space.campaign.spaces:
                        #     occupied_list.append(item.occupied)
                        # if all(occupied_list):
                        #     print('All campaign spaces full')
                        #     space.campaign.available = False
                        #     board.campaign_victory_points(space.campaign, space.theater)

                        if not available_list and not strategic:
                            for i in range(2):
                                game_board.propaganda(turn)
                            turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)                        

                elif turn == 'allied':
                    for token in allied_hand.hand_list:
                        if token.moving:
                            played_space, closed_theater, available_list = token.place_token(game_board, allied_hand, axis_hand, bags.research_bag, bags.allied_token_bag, bags.axis_token_bag, theaters, turn)
                            if token.effect == 'blitz':
                                blitz = True
                            else:
                                blitz = False
                            if token.effect == 'task_force':
                                task_force = True
                            else:
                                task_force = False
                            break

                    # print(played_space.effect)
                    if played_space and not task_force and not closed_theater:
                        if played_space.effect == 'strategic':
                            for button in game_board.theater_buttons:
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    # played_space = None
                                    if not blitz:
                                        turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                                    else:
                                        print('place another token')
                                    break
                            else:
                                print('pick a theater')
                                
                        else:
                            if not blitz and not closed_theater:
                                turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                            elif blitz and not closed_theater:
                                print('place another token')
                    elif played_space and not closed_theater:
                        turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)
                    if closed_theater:
                        if played_space:
                            if played_space.effect == 'strategic':
                                for button in game_board.theater_buttons:
                                    if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater:
                                        played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                        played_space = None                                                        
                                        break                               
                                else:
                                    print('pick a theater')
                        print('theater closed - select all other battle spaces')              
                        for battle_space in available_list:
                            if battle_space.rect.collidepoint(pos) and not strategic:
                                if battle_space.effect == 'propaganda':
                                    for i in range(battle_space.effect_value):
                                        game_board.propaganda(turn)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'production':
                                    game_board.industrial_production(allied_hand)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'imp_production':
                                    for i in range(battle_space.effect_value):
                                        game_board.industrial_production(allied_hand)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                # if battle_space.effect == 'tactical':
                                #     game_board.tactical_advantage(battle_space.theater, battle_space.effect_value, turn)
                                #     available_list.remove(battle_space)
                                if battle_space.effect == 'bombing':
                                    game_board.bombing(axis_hand, bags.allied_token_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'research':
                                    game_board.research(bags.allied_token_bag, bags.research_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'imp_research':
                                    for i in range(battle_space.effect_value):
                                        game_board.research(bags.allied_token_bag, bags.research_bag)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'res_industry':
                                    print('clicked on res ind')
                                    game_board.research_industry(allied_hand, bags.research_bag, turn)
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                if battle_space.effect == 'strategic': 
                                    strategic = True
                                    available_list.remove(battle_space)
                                    battle_space.occupied = True
                                occupied_list = []
                                for space in battle_space.campaign.spaces:
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)
                                if all(occupied_list):
                                    for i in range(battle_space.campaign.victory_points):
                                        game_board.propaganda(turn)
                                        print(battle_space.campaign.campaign)
                                        print(occupied_list)
                                        print('ran propaganda')
                                # if battle_space.occupied:
                                #     available_list.remove(battle_space)
                        if strategic: # think about how to get this into the above loop
                            # may have to reorder the loop - maybe put the collide point within each space
                            for button in game_board.theater_buttons: 
                                if button.rect.collidepoint(pos) and (button.theater != battle_space.theater.theater) and strategic:
                                    # print(battle_space.theater.theater)
                                    # print(battle_space.effect_value)
                                    battle_space.theater.move_track_marker_strategic(theaters, battle_space.effect_value, button.theater, turn)
                                    # print(battle_space.theater.theater)
                                    # print(battle_space.effect)
                                    # print(battle_space.effect_value)
                                    strategic = False
                                    # available_list.remove(battle_space)
                                    break
                            else:
                                print('pick a theater')
                        # new campaign points here
                        # occupied_list = []
                        # for item in space.campaign.spaces:
                        #     occupied_list.append(item.occupied)
                        # if all(occupied_list):
                        #     print('All campaign spaces full')
                        #     space.campaign.available = False
                        #     board.campaign_victory_points(space.campaign, space.theater)

                        
                        if not available_list and not strategic:
                            for i in range(2):
                                game_board.propaganda(turn)
                            turn, played_space, run = end_turn(turn, played_space, game_board, axis_hand, allied_hand, run)






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
    print('axis victory points:', game_board.axis_victory_points)
    print('allied victory points:', game_board.allied_victory_points)
    for v in theaters.values():
        print(f'{v.theater} is available {v.available}')
    print(turn)


if __name__ == '__main__':
    main()



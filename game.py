import os
import pygame
from gameboard import GameBoard, BattleSpace, Theater, Campaign
from tokens import Token
from manage_tokens import PlayerHand, TokenBags
from button import Button

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 900
ESPRESSO = (75, 56, 42) # table top color

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blitzkrieg!')
font = pygame.font.SysFont('times new roman', 20)
board = pygame.image.load(os.path.join('images', 'blitzkrieg_game_board_italian.jpg'))
board = pygame.transform.scale_by(board, 2)
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # need for creating transparent rect
clock = pygame.time.Clock()


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

for campaign in campaigns:
    campaigns[campaign].add_spaces_to_campaign(game_board)

for theater in theaters:
    theaters[theater].add_campaigns_to_theater(campaigns)

bags = TokenBags()
allied_hand = PlayerHand(bags.allied_token_bag, 'allied')
axis_hand = PlayerHand(bags.axis_token_bag, 'axis')

begin_turn_button = Button()
    
def end_turn(turn, played_space, game_board, axis_hand, allied_hand):
    result = None
    if turn == 'axis':
        game_board.industrial_production(axis_hand)
        if check_for_victory_availabilty(game_board, allied_hand.hand_list):
            turn = 'allied'
        else:
            result = 'axis: options'

    elif turn == 'allied':
        # check for winning on points
        winner = check_for_victory_points(game_board)
        if winner == 'axis':
            result = 'axis: points'

        elif winner == 'allies':
            result = 'allied: points'

        else:
            game_board.industrial_production(allied_hand)
            if check_for_victory_availabilty(game_board, axis_hand.hand_list):
                turn = 'axis'
            else:
                result = 'allied: options'


    print(f'{turn.title()} commander\'s turn')
    between_turns = True
    return turn, played_space, between_turns, result

def check_for_victory_points(game_board):
    winner = None
    if game_board.axis_victory_points >= 25 or game_board.allied_victory_points >= 25:
        if game_board.axis_victory_points > game_board.allied_victory_points:
            winner = 'axis'
        else:
            winner = 'allies'

    return winner

def check_for_victory_availabilty(game_board, hand):
    available_list = []
    available_move = True

    for space in game_board.battle_spaces:
        if not space.occupied and space.theater.available and space.campaign.available:
            available_list.append(space)

    for token in hand:
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

    return available_move

def text_on_screen(message, x, y):
        text = font.render(message, True, 'white')
        text_rect = text.get_rect()
        text_rect.x = x
        text_rect.y = y
        screen.blit(text, text_rect)

def list_tokens_last_turn(placed_tokens, played_spaces, show_tokens, turn):
    for token, space in zip(reversed(placed_tokens), reversed(played_spaces)):
        if token.side and token.side != turn:
            if not token.effect:
                if space.theater.theater == 'west_europe':
                    last_played_text = f'{token.unit.title()} {token.value} on a {space.effect.title()} space in Western Europe.'
                elif space.theater.theater == 'pacific':
                    last_played_text = f'{token.unit.title()} {token.value} on a {space.effect.title()} space in the Pacific.'
                elif space.theater.theater == 'east_europe':
                    last_played_text = f'{token.unit.title()} {token.value} on a {space.effect.title()} space in Eastern Europe.'
                elif space.theater.theater == 'africa':
                    last_played_text = f'{token.unit.title()} {token.value} on a {space.effect.title()} space in Africa and the Middle East.'
                elif space.theater.theater == 'asia':
                    last_played_text = f'{token.unit.title()} {token.value} on a {space.effect.title()} space in Southeast Asia.'
            else:
                if token.effect == 'task_force':
                    if space.theater.theater == 'west_europe':
                        last_played_text = f'Task Force {token.unit.title()} {token.value} on a {space.effect.title()} space in Western Europe.'
                    elif space.theater.theater == 'pacific':
                        last_played_text = f'Task Force {token.unit.title()} {token.value} on a {space.effect.title()} space in the Pacific.'
                    elif space.theater.theater == 'east_europe':
                        last_played_text = f'Task Force {token.unit.title()} {token.value} on a {space.effect.title()} space in Eastern Europe.'
                    elif space.theater.theater == 'africa':
                        last_played_text = f'Task Force {token.unit.title()} {token.value} on a {space.effect.title()} space in Africa and the Middle East.'
                    elif space.theater.theater == 'asia':
                        last_played_text = f'Task Force {token.unit.title()} {token.value} on a {space.effect.title()} space in Southeast Asia.'
                else:
                    if space.theater.theater == 'west_europe':
                        last_played_text = f'{token.effect.title()} {token.unit.title()} {token.value} on a {space.effect.title()} space in Western Europe.'
                    elif space.theater.theater == 'pacific':
                        last_played_text = f'{token.effect.title()} {token.unit.title()} {token.value} on a {space.effect.title()} space in the Pacific.'
                    elif space.theater.theater == 'east_europe':
                        last_played_text = f'{token.effect.title()} {token.unit.title()} {token.value} on a {space.effect.title()} space in Eastern Europe.'
                    elif space.theater.theater == 'africa':
                        last_played_text = f'{token.effect.title()} {token.unit.title()} {token.value} on a {space.effect.title()} space in Africa and the Middle East.'
                    elif space.theater.theater == 'asia':
                        last_played_text = f'{token.effect.title()} {token.unit.title()} {token.value} on a {space.effect.title()} space in Southeast Asia.'
            show_tokens.append(last_played_text)
        else:
            break
    return show_tokens


def main():
    run = True
    played_space = None
    turn = 'axis'
    between_turns = True
    print(f'{turn.title()} commander\'s turn')
    print('axis bag size', len(bags.axis_token_bag))
    blitz = False
    task_force = False
    closed_theater = False
    strategic = False
    result = None
    closed_theater_action = None
    show_tokens = []
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
        if result:
            if result == 'axis: options':
                axis_options_text = 'Axis forces win the war. Allied commander out of options.'
                text_on_screen(axis_options_text, 10, 770)
            elif result == 'axis: points':
                axis_points_text = f'Axis forces win the war on victory points: {game_board.axis_victory_points} - {game_board.allied_victory_points}.'
                text_on_screen(axis_points_text, 10, 770)
            elif result == 'allied: options':
                allied_options_text = 'Allied forces win the war. Axis commander out of options.'
                text_on_screen(allied_options_text, 10, 770)
            elif result == 'allied: points':
                allied_options_text = f'Allied forces win the war on victory points: {game_board.allied_victory_points} - {game_board.axis_victory_points}.'
                text_on_screen(allied_options_text, 10, 770)

        if between_turns and not result and not closed_theater:
            begin_turn_button.draw(screen, turn)
            if len(game_board.placed_tokens) > 1:
                if turn == 'axis':
                    text_on_screen('Units deployed by Allied commander:', 10, 770)

                else:
                    text_on_screen('Units deployed by Axis commander:', 10, 770)
                show_tokens = list_tokens_last_turn(game_board.placed_tokens, game_board.played_spaces, show_tokens, turn)

            for i, text in enumerate(reversed(show_tokens)):
                text_on_screen(text, 10, 790+20*i)

            show_tokens = []

        elif not between_turns and not result and not closed_theater:
            turn_text = f'{turn.title()} commander, deploy a unit'
            text_on_screen(turn_text, 10, 770)

            if turn == 'axis' :
                for token in axis_hand.hand_list:
                    token.draw(screen)
            else:
                for token in allied_hand.hand_list:
                    token.draw(screen)

        if strategic:
            strategic_text = 'Played strategic advantage. Click on a theater.'
            text_on_screen(strategic_text, 650, 770)
            
        if blitz and not strategic:
            blitz_text = 'Blitzed the enemy. Play another token.'
            text_on_screen(blitz_text, 700, 770)

        if closed_theater and not strategic:
            closed_theater_text = 'Theater closed - select all other battle spaces (except blank or strategic advantage).'
            text_on_screen(closed_theater_text, 10, 770)

        if closed_theater and closed_theater_action and not strategic:
            if closed_theater_action == 'propaganda':
                closed_theater_action_text = 'Propaganda earned you victory points!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'production':
                closed_theater_action_text = 'New unit available!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'imp_prduction':
                closed_theater_action_text = '2 new units available!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'bombing':
                closed_theater_action_text = 'You bombed an opponent\'s unit!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'research':
                closed_theater_action_text = 'Researched a special unit!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'imp_research':
                closed_theater_action_text = 'Researched 2 new special units!'
                text_on_screen(closed_theater_action_text, 700, 770)
            elif closed_theater_action == 'res_industry':
                closed_theater_action_text = 'New special unit available!'
                text_on_screen(closed_theater_action_text, 700, 770)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # print(pos)

                if not between_turns and not closed_theater:
                    if turn == 'allied':
                        for token in allied_hand.hand_list:
                            token.clicked_token(pos, game_board)
                    elif turn == 'axis':
                        for token in axis_hand.hand_list:
                            token.clicked_token(pos, game_board)        
            
            elif event.type == pygame.MOUSEMOTION:
                if not between_turns and not closed_theater:
                    if turn == 'allied':
                        for token in allied_hand.hand_list:
                            token.move_token(event)
                    elif turn == 'axis':
                        for token in axis_hand.hand_list:
                            token.move_token(event)


            elif event.type == pygame.MOUSEBUTTONUP:

                # closes if game over and click
                if result:
                    run = False

                if closed_theater_action:
                    closed_theater_action = None

                if begin_turn_button.rect.collidepoint(pos) and between_turns:
                    between_turns = False

                elif turn == 'axis' and not between_turns: 
                    for token in axis_hand.hand_list:
                        if token.moving:
                            played_space, closed_theater, available_list = token.place_token(game_board, axis_hand, allied_hand, bags.research_bag, bags.axis_token_bag, bags.allied_token_bag, theaters, turn)
                            if game_board.placed_tokens[-1].effect == 'blitz' and not closed_theater:
                                blitz = True

                            else:
                                blitz = False

                            if game_board.placed_tokens[-1].effect == 'task_force':
                                task_force = True

                            else:
                                task_force = False

                            break

                    if played_space and not task_force and not closed_theater:
                        if played_space.effect == 'strategic': 
                            strategic = True                           
                            for button in game_board.theater_buttons:
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater and theaters[button.theater].available:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    played_space = None
                                    strategic = False
                                    if not blitz:
                                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)                                     
                                    
                                    break
                                
                        else:
                            if not blitz and not closed_theater:
                                turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)
                                played_space = None

                    elif played_space and not closed_theater:
                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)
                    if closed_theater:
                        if played_space:
                            if played_space.effect == 'strategic':   
                                strategic = True                      
                                for button in game_board.theater_buttons:
                                    if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater and theaters[button.theater].available:
                                        played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                        played_space = None   
                                        strategic = False                               
                                        break
                                
                        for battle_space in available_list:
                            if battle_space.rect.collidepoint(pos) and not strategic:
                                available_list, strategic = game_board.execute_closed_theater_spaces(battle_space, turn, available_list, axis_hand, allied_hand, bags.axis_token_bag, bags.allied_token_bag, bags.research_bag, strategic)
                                closed_theater_action = battle_space.effect
                                occupied_list = []
                                for space in battle_space.campaign.spaces:
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)
                                if all(occupied_list):
                                    for i in range(battle_space.campaign.victory_points):
                                        game_board.propaganda(turn)

                        if strategic:
                            for button in game_board.theater_buttons: 
                                if button.rect.collidepoint(pos) and (button.theater != battle_space.theater.theater and theaters[button.theater].available) and strategic:
                                    battle_space.theater.move_track_marker_strategic(theaters, battle_space.effect_value, button.theater, turn)
                                    strategic = False
                                    break

                        if not available_list and not strategic:
                            closed_theater = False
                            for i in range(2):
                                game_board.propaganda(turn)
                            turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)                        
                    
                    # ends turn if hand is empty
                    if not closed_theater and not strategic and not axis_hand.hand_list:
                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)

                elif turn == 'allied' and not between_turns:
                    for token in allied_hand.hand_list:
                        if token.moving:
                            played_space, closed_theater, available_list = token.place_token(game_board, allied_hand, axis_hand, bags.research_bag, bags.allied_token_bag, bags.axis_token_bag, theaters, turn)
                            if game_board.placed_tokens[-1].effect == 'blitz' and not closed_theater:
                                blitz = True

                            else:
                                blitz = False

                            if game_board.placed_tokens[-1].effect == 'task_force':
                                task_force = True

                            else:
                                task_force = False

                            break

                    if played_space and not task_force and not closed_theater:
                        if played_space.effect == 'strategic':
                            strategic = True
                            for button in game_board.theater_buttons:
                                if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater and theaters[button.theater].available:
                                    played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                    played_space = None
                                    strategic = False
                                    if not blitz:
                                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)
                                    
                                    break
                                
                        else:
                            if not blitz and not closed_theater:
                                turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)
                                played_space = None

                    elif played_space and not closed_theater:
                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)
                    
                    if closed_theater:
                        if played_space:
                            if played_space.effect == 'strategic':
                                strategic = True
                                for button in game_board.theater_buttons:
                                    if button.rect.collidepoint(pos) and button.theater != played_space.theater.theater and theaters[button.theater].available:
                                        played_space.theater.move_track_marker_strategic(theaters, played_space.effect_value, button.theater, turn)
                                        played_space = None 
                                        strategic = False                                                       
                                        break                               
           
                        for battle_space in available_list:
                            if battle_space.rect.collidepoint(pos) and not strategic:
                                available_list, strategic = game_board.execute_closed_theater_spaces(battle_space, turn, available_list, allied_hand, axis_hand, bags.allied_token_bag, bags.axis_token_bag, bags.research_bag, strategic)
                                closed_theater_action = battle_space.effect
                                occupied_list = []
                                for space in battle_space.campaign.spaces:
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)

                                if all(occupied_list):
                                    for i in range(battle_space.campaign.victory_points):
                                        game_board.propaganda(turn)

                        if strategic:
                            for button in game_board.theater_buttons: 
                                if button.rect.collidepoint(pos) and (button.theater != battle_space.theater.theater and theaters[button.theater].available) and strategic:
                                    battle_space.theater.move_track_marker_strategic(theaters, battle_space.effect_value, button.theater, turn)
                                    strategic = False
                                    break

                        if not available_list and not strategic:
                            closed_theater = False
                            for i in range(2):
                                game_board.propaganda(turn)
                            turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)

                    # ends turn if hand is empty
                    if not closed_theater and not strategic and not axis_hand.hand_list:
                        turn, played_space, between_turns, result = end_turn(turn, played_space, game_board, axis_hand, allied_hand)


        pygame.display.flip()

        clock.tick(60)

    print('axis victory points:', game_board.axis_victory_points)
    print('allied victory points:', game_board.allied_victory_points)





if __name__ == '__main__':
    main()



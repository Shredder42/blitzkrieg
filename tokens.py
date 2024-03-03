import os
import pygame


class Token:
    ''' these are the game pieces'''
    def __init__(self, side, unit, value, token_image, effect = None, special = False):
        self.side = side
        self.unit = unit
        self.value = value      
        self.token_image = token_image
        self.effect = effect
        self.special = special
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.original_x = None
        self.original_y = None
        self.moving = False
        self.placed = False

    def load_image(self):
        image = pygame.image.load(os.path.join('images', self.token_image))
        image = pygame.transform.scale(image, (50, 50))
        return image
    
    def draw(self, surface):
        return surface.blit(self.image, self.rect)
    
    def token_starting_location(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
   
    def clicked_token(self, pos, board):
        if self.rect.collidepoint(pos):
            if not self.placed:
                self.moving = True
            if self.effect == 'spy':
                last_token = board.placed_tokens[-1]
                self.unit = last_token.unit
                self.value = last_token.value
                self.effect = last_token.effect
                print('Prepare to deploy the spy!')
                print('Spy unit type:', last_token.unit)
                print('Spy value:', last_token.value)
                print('Spy effect:', last_token.effect)

    def move_token(self, event):
        if self.moving:
            self.rect.move_ip(event.rel)

    def match_type_and_unit(self, space):
        if (self.unit == 'army' and space.type in ('land', 'both')) or \
        (self.unit == 'navy' and space.type in ('sea', 'both')) or \
        self.unit == 'airforce':
            return True

        else:
            return False

    def place_token(self, board, player_hand, opponent_hand, research_bag, player_bag, opponent_bag, theaters, turn):
        available_list = []
        closed_theater = False
        played_space = None
        for space in board.battle_spaces:
            if (self.rect.collidepoint(space.rect.center) and not board.placed_tokens[-1].effect == 'blitz' and not \
            space.occupied and space.theater.available  and \
            ((space.campaign.available and self.match_type_and_unit(space)) or \
            self.effect == 'scientist')) or \
            (self.rect.collidepoint(space.rect.center) and board.placed_tokens[-1].effect == 'blitz' and not \
            space.occupied and space.theater.available and space.theater == board.played_spaces[-1].theater and \
            ((space.campaign.available and self.match_type_and_unit(space)) or \
            self.effect == 'scientist')):
                self.rect.center = space.rect.center
                space.occupied = True
                space.occupied_by = self
                player_hand.hand_list.remove(self)
                self.placed = True
                board.played_spaces.append(space)
                board.placed_tokens.append(self)
                space.theater.adjust_unit_count(self, turn)
                space.theater.move_track_marker(self.value, turn)

                if self.effect == 'bombing':
                    board.bombing(opponent_hand, opponent_bag)
                elif self.effect == 'nuclear':
                    space.theater.move_track_marker_nuclear(theaters, turn)
                elif self.effect == 'admiral':
                    if turn == 'axis':
                        space.theater.move_track_marker(space.theater.axis_navy_count - 1, turn)
                    elif turn == 'allied':
                        space.theater.move_track_marker(space.theater.allied_navy_count - 1, turn)
                elif self.effect == 'general':
                    if turn == 'axis':
                        space.theater.move_track_marker(space.theater.axis_army_count - 1, turn)
                    elif turn == 'allied':
                        space.theater.move_track_marker(space.theater.allied_army_count - 1, turn)
                # battle space effects
                if self.effect != 'task_force':
                    if space.effect == 'propaganda':
                        for i in range(space.effect_value):
                            board.propaganda(turn)
                    elif space.effect == 'production':
                        board.industrial_production(player_hand)
                    elif space.effect == 'imp_production':
                        for i in range(space.effect_value):
                            board.industrial_production(player_hand)
                    elif space.effect == 'tactical':
                        board.tactical_advantage(space.theater, space.effect_value, turn)
                    elif space.effect == 'bombing':
                        board.bombing(opponent_hand, opponent_bag)
                    elif space.effect == 'research':
                        board.research(player_bag, research_bag, turn)
                    elif space.effect == 'imp_research':
                        for i in range(space.effect_value):
                            board.research(player_bag, research_bag, turn)
                    elif space.effect == 'res_industry':
                        board.research_industry(player_hand, research_bag, turn)

                played_space = space
                camp = space.campaign.spaces
                occupied_list = []
                for item in camp:
                    occupied_list.append(item.occupied)

                if all(occupied_list):
                    space.campaign.available = False
                    board.campaign_victory_points(space.campaign, space.theater)

                    try:
                        space.theater.campaigns[space.theater.campaigns.index(space.campaign) + 1].available = True
                    except IndexError:
                        space.theater.available = False

                # closing theater               
                if (abs(space.theater.theater_score) >= 14 and space.theater.theater in ('west_europe', 'pacific', 'east_europe')):
                    closed_theater = True
                    if space.theater.available:
                        for campaign in space.theater.campaigns:
                            for space in campaign.spaces:
                                if not space.occupied and space.effect != 'blank' and space.effect != 'tactical':
                                    available_list.append(space)
                                # this will automatically give victory pts if only spaces remaining in campaign are blank or tactical
                                elif not space.occupied and (space.effect == 'blank' or space.effect != 'tactical'):
                                    space.occupied = True
                                    occupied_list = []
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)
                                    if all(occupied_list):
                                        for i in range(space.campaign.victory_points):
                                            board.propaganda(turn)
                        space.theater.available = False

                elif (abs(space.theater.theater_score) >= 11 and space.theater.theater in ('africa', 'asia')):
                    closed_theater = True
                    if space.theater.available:
                        for campaign in space.theater.campaigns:
                            for space in campaign.spaces:
                                if not space.occupied and space.effect != 'blank' and space.effect != 'tactical':
                                    available_list.append(space)
                                elif not space.occupied and (space.effect == 'blank' or space.effect != 'tactical'):
                                    space.occupied = True
                                    occupied_list = [] # this will automaticall give victory pts if only spaces remaining in campaign are blank or tactical
                                    for item in space.campaign.spaces:
                                        occupied_list.append(item.occupied)
                                    if all(occupied_list):
                                        for i in range(space.campaign.victory_points):
                                            board.propaganda(turn)
                        space.theater.available = False

                break

        else:
            self.rect.x = self.original_x
            self.rect.y = self.original_y
            played_space = None

        self.moving = False

        return played_space, closed_theater, available_list


if __name__ == '__main__':
    token1 = Token('allied', 'army', 1, 10, 10, 'allied_army_1.png')
    print(token1.moving)
        

        

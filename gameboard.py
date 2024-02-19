import os
import pygame
import random
'''
types of battle spaces are:
    - industrial production (production)
    - bombing
    - research
    - tactical advantage (tactical)
    - strategic advantage (strategic)
    - propoganda
    - improved industrial production (imp_production)
    - research industry (res_industry)
    - improved research (imp_research)

campaigns are:
    - west_europe
    - pacific
    - east_europe
    - africa
    - asia
'''
class TheaterButton:
    def __init__(self, x, y, width, height, theater):
        self.x = x
        self. y = y
        self.width = width
        self.height = height
        self.theater = theater
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.armed = False

    def draw(self, surface):
        theater_button = pygame.draw.rect(surface, (255, 255, 255, 0), self.rect)
        return theater_button

class BattleSpace:
    ''' these are the spaces on the game board '''
    def __init__(self, x, y, effect, effect_value, type, theater, campaign):
        self.x = x
        self.y = y
        self.effect = effect
        self.effect_value = effect_value
        self.type = type
        self.theater = theater
        self.campaign = campaign
        self.occupied = False
        self.occupied_by = None
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, surface):
        # creates transparent rect
        invisible_rect = pygame.draw.rect(surface, (255, 255, 255, 0), self.rect) 
        return invisible_rect

class Campaign:
    ''' manages campaigns and initializes battle spaces '''
    def __init__(self, campaign, victory_points, available = False):
        self.campaign = campaign
        self.victory_points = victory_points
        self.available = available
        self.complete = False
        self.spaces = []
        # self.battle_spaces = self.create_battle_spaces2()

    def add_spaces_to_campaign(self, game_board):
        if self.campaign == 'northern_west_europe':
            for space in game_board.battle_spaces[:3]:
                self.spaces.append(space)
        elif self.campaign == 'central_west_europe':
            for space in game_board.battle_spaces[3:6]:
                self.spaces.append(space)
        elif self.campaign == 'southern_west_europe':
            for space in game_board.battle_spaces[6:9]:
                self.spaces.append(space)
        elif self.campaign == 'northern_pacific':
            for space in game_board.battle_spaces[9:11]:
                self.spaces.append(space)
        elif self.campaign == 'central_pacific':
            for space in game_board.battle_spaces[11:15]:
                self.spaces.append(space)
        elif self.campaign == 'southern_pacific':
            for space in game_board.battle_spaces[15:18]:
                self.spaces.append(space)
        elif self.campaign == 'northern_east_europe':
            for space in game_board.battle_spaces[18:20]:
                self.spaces.append(space)
        elif self.campaign == 'central_east_europe':
            for space in game_board.battle_spaces[20:23]:
                self.spaces.append(space)
        elif self.campaign == 'southern_east_europe':
            for space in game_board.battle_spaces[23:28]:
                self.spaces.append(space)
        elif self.campaign == 'northern_africa':
            for space in game_board.battle_spaces[28:32]:
                self.spaces.append(space)
        elif self.campaign == 'southern_africa':
            for space in game_board.battle_spaces[32:35]:
                self.spaces.append(space)
        elif self.campaign == 'northern_asia':
            for space in game_board.battle_spaces[35:38]:
                self.spaces.append(space)
        elif self.campaign == 'southern_asia':
            for space in game_board.battle_spaces[38:]:
                self.spaces.append(space)
    # def create_battle_spaces2(self):
    #     spaces = []
    #     if self.campaign == 'west_europe_1':
    #         spaces.append(BattleSpace2(196, 207, 'production', 1, 'sea'))
    #         spaces.append(BattleSpace2(258, 207, 'research', 1, 'land')        self.track_markers)
    #         spaces.append(BattleSpace2(320, 207, 'propaganda', 1,  'both'))
    #     return spaces
    # def close_campaign(self, game_board, turn):
    #     occupied_list = []
    #     for space in self.spaces:
    #         occupied_list.append(space.occupied)
    #     if all(occupied_list):
    #         for i in range(self.victory_points):
    #             game_board.propaganda(turn)





class Theater:
    '''manages theaters and initializes campaigns '''
    def __init__(self, theater, score_track_x, score_track_y):
        self.theater = theater
        self.available = True
        self.complete = False
        self.campaigns = []
        self.score_track_x = score_track_x
        self.score_track_y = score_track_y
        self.theater_score = 0
        self.allied_army_count = 0
        self.allied_navy_count = 0
        self.axis_army_count = 0
        self.axis_navy_count = 0

    def add_campaigns_to_theater(self, campaigns):
        if self.theater == 'west_europe':
            campaign_list = [campaigns['northern_west_europe'], campaigns['central_west_europe'], campaigns['southern_west_europe']]
            for campaign in campaign_list:
                self.campaigns.append(campaign)
        elif self.theater == 'pacific':
            campaign_list = [campaigns['northern_pacific'], campaigns['central_pacific'], campaigns['southern_pacific']]
            for campaign in campaign_list:
                self.campaigns.append(campaign)
        elif self.theater == 'east_europe':
            campaign_list = [campaigns['northern_east_europe'], campaigns['central_east_europe'], campaigns['southern_east_europe']]
            for campaign in campaign_list:
                self.campaigns.append(campaign)
        elif self.theater == 'africa':
            campaign_list = [campaigns['northern_africa'], campaigns['southern_africa']]
            for campaign in campaign_list:
                self.campaigns.append(campaign)
        elif self.theater == 'asia':
            campaign_list = [campaigns['northern_asia'], campaigns['southern_asia']]
            for campaign in campaign_list:
                self.campaigns.append(campaign)

    def draw_track_marker(self, surface):
        track_marker = pygame.draw.circle(surface, (0, 0, 0), (self.score_track_x, self.score_track_y), 5, 0)
        return track_marker
        
    def move_track_marker(self, value, turn):
        # self.theater_score += token_value
        if self.theater_score > -14 and self.theater_score < 14:
            for i in range(value):
                if turn == 'axis':
                    self.theater_score += 1
                    if self.theater in ('west_europe', 'pacific', 'east_europe'):
                        if self.theater_score < -9:
                            self.score_track_y -= 20
                        elif self.theater_score <= 10:
                            self.score_track_x += 20
                        elif self.theater_score <= 14:
                            self.score_track_y += 20
                        # if self.theater_score == 14:
                        #     self.available = False # closes theathers
                    elif self.theater in ('africa', 'asia'):
                        if self.theater_score <= -9:
                            self.score_track_y -= 20
                        elif self.theater_score <= 9:
                            self.score_track_x += 20
                        elif self.theater_score >= 10:
                            self.score_track_y += 20
                        if self.theater_score == 11:
                            self.available = False # closes theather
                elif turn == 'allied':
                    self.theater_score -= 1
                    if self.theater in ('west_europe', 'pacific', 'east_europe'):
                        if self.theater_score > 9:
                            self.score_track_y -= 20
                        elif self.theater_score >= -10:
                            self.score_track_x -= 20
                        elif self.theater_score >= -14:
                            self.score_track_y += 20
                        # if self.theater_score == -14:
                        #     self.available = False # closes theather
                    elif self.theater in ('africa', 'asia'):
                        if self.theater_score >= 9:
                            self.score_track_y -= 20    
                        elif self.theater_score >= -9:
                            self.score_track_x -= 20
                        elif self.theater_score <= -10:
                            self.score_track_y += 20
                        if self.theater_score == -11:
                            self.available = False # closes theather

        print('theater score:', self.theater_score)

    def move_track_marker_nuclear(self, theaters, turn):
        print(type(theaters))
        for i in range(2):
            if turn == 'axis':
                for k, v in theaters.items():                
                    if k != self.theater:
                        if k in ('west_europe', 'pacific', 'east_europe'):
                            if v.theater_score >= -12 and v.theater_score <= 13:
                                v.theater_score -= 1
                                if v.theater_score <= -11:
                                    v.score_track_y += 20
                                elif v.theater_score <= 9:
                                    v.score_track_x -= 20
                                elif v.theater_score <= 12:
                                    v.score_track_y -= 20
                            
                        if k in ('africa', 'asia'):
                            if v.theater_score >= -9 and v.theater_score <= 10:
                                v.theater_score -= 1
                                if v.theater_score == -10:
                                    v.score_track_y += 20
                                elif v.theater_score <= 8:
                                    v.score_track_x -= 20
                                elif v.theater_score == 9:
                                    v.score_track_y -= 20

                    print(k, v.theater_score)

            elif turn == 'allied':
                for k, v in theaters.items():                
                    if k != self.theater:
                        if k in ('west_europe', 'pacific', 'east_europe'):
                            if v.theater_score >= -13 and v.theater_score <= 12:
                                v.theater_score += 1
                                if v.theater_score >= 11:
                                    v.score_track_y += 20
                                elif v.theater_score >= -9:
                                    v.score_track_x += 20
                                elif v.theater_score >= -12:
                                    v.score_track_y -= 20

                        if k in ('africa', 'asia'):
                            if v.theater_score >= -10 and v.theater_score <= 9:
                                v.theater_score += 1
                                if v.theater_score == 10:
                                    v.score_track_y += 20
                                elif v.theater_score >= -8:
                                    v.score_track_x += 20
                                elif v.theater_score == -9:
                                    v.score_track_y -= 20
                    print(k, v.theater_score)
    
    def move_track_marker_strategic(self, theaters, space_value, selected_theater, turn):
        print('ran move track marker strategic')
        for k, v in theaters.items():   
            if k != self.theater and k == selected_theater:
                for i in range(space_value):
                    if turn == 'axis':
                        if k in ('west_europe', 'pacific', 'east_europe'):
                            if v.theater_score >= -13 and v.theater_score <= 12:
                                v.theater_score += 1
                                if v.theater_score >= 11:
                                    v.score_track_y += 20 
                                elif v.theater_score >= -9:
                                    v.score_track_x += 20
                                elif v.theater_score >= -12:
                                    v.score_track_y -= 20
                        elif k in ('africa', 'asia'):
                            if v.theater_score >= -10 and v.theater_score <= 9:
                                v.theater_score += 1
                                if v.theater_score == 10:
                                    v.score_track_y += 20
                                elif v.theater_score >= -8:
                                    v.score_track_x += 20  
                                elif v.theater_score == -9:
                                    v.score_track_y -= 20
                    elif turn == 'allied':
                        if k in ('west_europe', 'pacific', 'east_europe'):
                            if v.theater_score >= -12 and v.theater_score <= 13:
                                v.theater_score -= 1
                                if v.theater_score <= -11:
                                    v.score_track_y += 20
                                elif v.theater_score <= 9:
                                    v.score_track_x -= 20
                                elif v.theater_score <= 13:
                                    v.score_track_y += 20
                        elif k in ('africa', 'asia'):
                            if v.theater_score >= -9 and v.theater_score <= 10:
                                v.theater_score -= 1
                                if v.theater_score == -10:
                                    v.score_track_y += 20
                                elif v.theater_score <= 8:
                                    v.score_track_x -= 20
                                elif v.theater_score <= 9:
                                    v.score_track_y -= 20

    def adjust_unit_count(self, token, turn):
        if not token.special:
            if token.unit == 'airforce': 
                if turn == 'allied':
                    self.allied_army_count += 1
                    self.allied_navy_count += 1
                elif turn == 'axis':
                    self.axis_army_count += 1
                    self.axis_navy_count += 1
            elif token.unit == 'army':
                if turn == 'allied':
                    self.allied_army_count += 1
                elif turn == 'axis':
                    self.axis_army_count += 1
            elif token.unit == 'navy':
                if turn == 'allied':
                    self.allied_navy_count += 1
                elif turn == 'axis':
                    self.axis_navy_count += 1



class GameBoard:
    ''' manages game board and initializes the theaters '''
    def __init__(self, theaters, campaigns):
        self.theaters = theaters
        self.campaigns = campaigns
        self.battle_spaces = self.create_battle_spaces()
        self.theater_buttons = self.create_theater_buttons()
        self.placed_tokens = []
        self.axis_victory_points = 0
        self.axis_symbol = pygame.image.load(os.path.join('images', 'axis_symbol.jpg'))
        self.axis_symbol_rect = self.axis_symbol.get_rect()
        self.axis_symbol_rect = pygame.Rect(13, 58, 12, 12)
        self.allied_victory_points = 0
        self.allied_symbol = pygame.image.load(os.path.join('images', 'allied_symbol.jpg'))
        self.allied_symbol_rect = self.allied_symbol.get_rect()
        self.allied_symbol_rect = pygame.Rect(13, 70, 12, 12)


    def create_battle_spaces(self):
        spaces = []
        spaces.append(BattleSpace(196, 207, 'production', 1, 'sea', self.theaters['west_europe'], self.campaigns['northern_west_europe']))
        spaces.append(BattleSpace(258, 207, 'research', 1, 'land', self.theaters['west_europe'], self.campaigns['northern_west_europe']))
        spaces.append(BattleSpace(320, 207, 'propaganda', 1,  'both', self.theaters['west_europe'], self.campaigns['northern_west_europe']))
        spaces.append(BattleSpace(196, 269, 'bombing', 1, 'land', self.theaters['west_europe'], self.campaigns['central_west_europe']))
        spaces.append(BattleSpace(258, 269, 'production', 1, 'land', self.theaters['west_europe'], self.campaigns['central_west_europe']))
        spaces.append(BattleSpace(320, 269, 'blank', 0, 'both', self.theaters['west_europe'], self.campaigns['central_west_europe']))
        spaces.append(BattleSpace(196, 331, 'res_industry', 1, 'both', self.theaters['west_europe'], self.campaigns['southern_west_europe']))
        spaces.append(BattleSpace(258, 331, 'strategic', 3,  'land', self.theaters['west_europe'], self.campaigns['southern_west_europe']))
        spaces.append(BattleSpace(320, 331, 'blank', 0, 'both', self.theaters['west_europe'], self.campaigns['southern_west_europe']))
        spaces.append(BattleSpace(111, 475, 'bombing', 1, 'sea', self.theaters['pacific'], self.campaigns['northern_pacific']))
        spaces.append(BattleSpace(173, 475, 'research', 1, 'sea', self.theaters['pacific'], self.campaigns['northern_pacific']))
        spaces.append(BattleSpace(111, 537, 'imp_research', 2, 'sea', self.theaters['pacific'], self.campaigns['central_pacific'])) 
        spaces.append(BattleSpace(173, 537, 'production', 1, 'sea', self.theaters['pacific'], self.campaigns['central_pacific'])) 
        spaces.append(BattleSpace(235, 537, 'strategic', 2, 'sea', self.theaters['pacific'], self.campaigns['central_pacific'])) 
        spaces.append(BattleSpace(297, 537, 'blank', 0, 'both', self.theaters['pacific'], self.campaigns['central_pacific'])) 
        spaces.append(BattleSpace(111, 599, 'bombing', 1, 'sea', self.theaters['pacific'], self.campaigns['southern_pacific'])) 
        spaces.append(BattleSpace(173, 599, 'propaganda', 2, 'both', self.theaters['pacific'], self.campaigns['southern_pacific'])) 
        spaces.append(BattleSpace(235, 599, 'blank', 0, 'both', self.theaters['pacific'], self.campaigns['southern_pacific']))
        spaces.append(BattleSpace(669, 139, 'tactical', 1, 'land', self.theaters['east_europe'], self.campaigns['northern_east_europe']))
        spaces.append(BattleSpace(731, 139, 'production', 1, 'land', self.theaters['east_europe'], self.campaigns['northern_east_europe']))  
        spaces.append(BattleSpace(669, 201, 'propaganda', 1, 'land', self.theaters['east_europe'], self.campaigns['central_east_europe']))  
        spaces.append(BattleSpace(731, 201, 'imp_research', 2, 'land', self.theaters['east_europe'], self.campaigns['central_east_europe']))  
        spaces.append(BattleSpace(793, 201, 'blank', 0, 'both', self.theaters['east_europe'], self.campaigns['central_east_europe']))  
        spaces.append(BattleSpace(669, 263, 'bombing', 1, 'land', self.theaters['east_europe'], self.campaigns['southern_east_europe']))  
        spaces.append(BattleSpace(731, 263, 'tactical', 2, 'land', self.theaters['east_europe'], self.campaigns['southern_east_europe']))  
        spaces.append(BattleSpace(793, 263, 'strategic', 3, 'land', self.theaters['east_europe'], self.campaigns['southern_east_europe']))
        spaces.append(BattleSpace(855, 263, 'propaganda', 2, 'land', self.theaters['east_europe'], self.campaigns['southern_east_europe']))
        spaces.append(BattleSpace(917, 263, 'blank', 0, 'land', self.theaters['east_europe'], self.campaigns['southern_east_europe']))
        spaces.append(BattleSpace(579, 411, 'strategic', 3, 'land', self.theaters['africa'], self.campaigns['northern_africa']))
        spaces.append(BattleSpace(641, 411, 'tactical', 1, 'sea', self.theaters['africa'], self.campaigns['northern_africa']))
        spaces.append(BattleSpace(703, 411, 'research', 1, 'both', self.theaters['africa'], self.campaigns['northern_africa']))
        spaces.append(BattleSpace(765, 411, 'propaganda', 1, 'both', self.theaters['africa'], self.campaigns['northern_africa']))
        spaces.append(BattleSpace(579, 473, 'tactical', 2, 'land', self.theaters['africa'], self.campaigns['southern_africa']))
        spaces.append(BattleSpace(641, 473, 'imp_production', 2, 'sea', self.theaters['africa'], self.campaigns['southern_africa']))
        spaces.append(BattleSpace(703, 473, 'blank', 0, 'both', self.theaters['africa'], self.campaigns['southern_africa']))
        spaces.append(BattleSpace(725, 617, 'propaganda', 2, 'sea', self.theaters['asia'], self.campaigns['northern_asia']))
        spaces.append(BattleSpace(787, 617, 'propaganda', 1, 'both', self.theaters['asia'], self.campaigns['northern_asia']))
        spaces.append(BattleSpace(849, 617, 'strategic', 1, 'both', self.theaters['asia'], self.campaigns['northern_asia']))
        spaces.append(BattleSpace(725, 679, 'bombing', 1, 'sea', self.theaters['asia'], self.campaigns['southern_asia']))
        spaces.append(BattleSpace(787, 679, 'propaganda', 2, 'land', self.theaters['asia'], self.campaigns['southern_asia']))
        spaces.append(BattleSpace(849, 679, 'blank', 0, 'both', self.theaters['asia'], self.campaigns['southern_asia']))

        return spaces
    
    def create_theater_buttons(self):
        buttons = []
        buttons.append(TheaterButton(178, 136, 208, 25, 'west_europe'))
        buttons.append(TheaterButton(155, 403, 170, 25, 'pacific'))
        buttons.append(TheaterButton(725, 68, 182, 25, 'east_europe'))
        buttons.append(TheaterButton(600, 340, 235, 25, 'africa'))
        buttons.append(TheaterButton(730, 547, 175, 25, 'asia'))

        return buttons
    
    def draw_symbols(self, surface):
        surface.blit(self.allied_symbol, self.allied_symbol_rect)
        surface.blit(self.axis_symbol, self.axis_symbol_rect)

    def draw(self, surface):
        return surface.blit(self.image, self.rect)
    
    def propaganda(self, turn):
        if turn == 'axis':
            self.axis_victory_points += 1       
            if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                self.axis_symbol_rect.x += 28
            elif self.axis_victory_points == 16:
                self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)  
        elif turn == 'allied':
            self.allied_victory_points += 1       
            if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                self.allied_symbol_rect.x += 28
            elif self.allied_victory_points == 16:
                self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12)           

    def industrial_production(self, hand):
        hand.draw_new_token()

    def tactical_advantage(self, theater, value, turn):
        theater.move_track_marker(value, turn)

    def bombing(self, opponent_hand, opponent_bag):
        opponent_bag.append(opponent_hand.hand_list.pop(random.randrange(0, len(opponent_hand.hand_list))))
        random.shuffle(opponent_bag)
        print('ran bombing')

    def research(self, player_bag, research_bag):
        player_bag.append(research_bag.pop())
        random.shuffle(player_bag)
        random.shuffle(research_bag)

    def research_industry(self, hand, research_bag, turn):
        hand.hand_list.append(research_bag.pop())  
        if turn == 'axis':
            y = 840          
        elif turn == 'allied':
            y = 770
        for i, token in enumerate((hand.hand_list)):
            x = 50 + i * 60
            token.token_starting_location(x, y) 
        random.shuffle(research_bag) 
        print('rand res ind')

    def campaign_victory_points(self, campaign, theater):
        if theater.theater_score == 0:
            for i in range(campaign.victory_points):
                self.axis_victory_points += 1       
                if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                    self.axis_symbol_rect.x += 28
                elif self.axis_victory_points == 16:
                    self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)
                self.allied_victory_points += 1       
                if self.allied_victory_points <= 15 or self.axis_victory_points > 16:
                    self.allied_symbol_rect.x += 28
                elif self.allied_victory_points == 16:
                    self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12) 
        if theater.theater in ('west_europe', 'pacific', 'east_europe'):
            if theater.theater_score >= 1 and theater.theater_score <= 4:
                for i in range(campaign.victory_points):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)  
            elif theater.theater_score >= 5 and theater.theater_score <= 9:
                for i in range(campaign.victory_points + 1):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12) 
            elif theater.theater_score >= 10:
                for i in range(campaign.victory_points + 2):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)
            elif theater.theater_score >= -4 and theater.theater_score <= -1:
                for i in range(campaign.victory_points):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12)  
            elif theater.theater_score >= -9 and theater.theater_score <= -5:
                for i in range(campaign.victory_points + 1):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12) 
            elif theater.theater_score <= -10:
                for i in range(campaign.victory_points + 2):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12)  
        elif theater.theater in ('africa', 'asia'):
            if theater.theater_score >= 1 and theater.theater_score <= 3:
                for i in range(campaign.victory_points):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)  
            elif theater.theater_score >= 4 and theater.theater_score <= 7:
                for i in range(campaign.victory_points + 1):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12) 
            elif theater.theater_score >= 8:
                for i in range(campaign.victory_points + 2):
                    self.axis_victory_points += 1       
                    if self.axis_victory_points <= 15 or self.axis_victory_points > 16:
                        self.axis_symbol_rect.x += 28
                    elif self.axis_victory_points == 16:
                        self.axis_symbol_rect = pygame.Rect(41, 85, 12, 12)
            elif theater.theater_score >= -3 and theater.theater_score <= -1:
                for i in range(campaign.victory_points):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12)  
            elif theater.theater_score >= -7 and theater.theater_score <= -4:
                for i in range(campaign.victory_points + 1):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12) 
            elif theater.theater_score <= -8:
                for i in range(campaign.victory_points + 2):
                    self.allied_victory_points += 1       
                    if self.allied_victory_points <= 15 or self.allied_victory_points > 16:
                        self.allied_symbol_rect.x += 28
                    elif self.allied_victory_points == 16:
                        self.allied_symbol_rect = pygame.Rect(41, 97, 12, 12)
        print(f'axis {self.axis_victory_points}: allied {self.allied_victory_points}')






        
    # def create_theaters(self):
    #     theaters = {}
    #     theaters['west_europe'] = Theater('west_europe')
    #     theaters['pacific'] = Theater('pacific')
    #     theaters['east_europe'] = Theater('east_europe')
    #     theaters['africa'] = Theater('africa')
    #     theaters['asia'] = Theater('asia')
    #     return theaters

if __name__ == '__main__':
    # northern_west_europe = Campaign('northern_west_europe')
    west_europe = Theater('west_europe')
    # board = GameBoard()
    # print(board.battle_spaces[0].theater.available)
    # print(board.battle_spaces[0].theater.theater)
    # print(board.battle_spaces[0].campaign.available)
    # print(board.battle_spaces[0].campaign.campaign)
    print(Theater('east_europe').campaigns)
    # print(board.theaters['pacific'].theater)
    # print(board.theaters['pacific'].campaigns[1].complete)
    # print(board.theaters['west_europe'].campaigns['west_europe_1'].battle_spaces[0].effect)
    # print(board.theaters.keys())
    # for key in board.theaters.keys():
    #     print(key)
    # print(board.theaters['west_europe'].campaigns.keys())
    # for space in board.theaters['west_europe'].campaigns['west_europe_1'].battle_spaces:
    #     print(space)

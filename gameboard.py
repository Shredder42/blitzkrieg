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
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, surface):
        # creates transparent rect
        invisible_rect = pygame.draw.rect(surface, (255, 255, 255, 0), self.rect) 
        return invisible_rect

class Campaign:
    ''' manages campaigns and initializes battle spaces '''
    def __init__(self, campaign, rank, available = False):
        self.campaign = campaign
        self.rank = rank
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
        
    def move_track_marker(self, value):
        # self.theater_score += token_value
        for i in range(value):
            self.theater_score += 1
            if self.theater in ('west_europe', 'pacific', 'east_europe'):
                if self.theater_score <= 10:
                    self.score_track_x += 20
                elif self.theater_score <= 14:
                    self.score_track_y += 20
                if self.theater_score >= 14:
                    self.available = False
            if self.theater in ('africa', 'asia'):
                if self.theater_score <= 9:
                    self.score_track_x += 20
                elif self.theater_score <= 11:
                    self.score_track_y += 20
                if self.theater_score >= 11:
                    self.available = False
            
            




        # self.campaigns = self.create_campaigns()

    # def create_campaigns(self):
    #     campaigns = {}
    #     if self.theater in ('west_europe'):
    #         campaigns['west_europe_1'] = Campaign('west_europe_1')
    #         campaigns['west_europe_2'] = Campaign('west_europe_2')
    #         campaigns['west_europe_3'] = Campaign('west_europe_3')
    #     else: 
    #         campaigns[1] = Campaign(1)
    #         campaigns[2] = Campaign(2)
    #     return campaigns


class GameBoard:
    ''' manages game board and initializes the theaters '''
    def __init__(self, theaters, campaigns):
        self.theaters = theaters
        self.campaigns = campaigns
        self.battle_spaces = self.create_battle_spaces()
        self.placed_tokens = []

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

    def industrial_production(self, hand):
        hand.draw_new_token()

    def tactical_advantage(self, theater, value):
        theater.move_track_marker(value)

    def bombing(self, opponent_hand, bag):
            bag.append(opponent_hand.hand_list.pop(random.randint(0, len(opponent_hand.hand_list))))
            random.shuffle(bag)
        
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

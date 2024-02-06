import pygame
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
    
class GameBoard:
    ''' initializes the battle spaces and puts them on the board '''
    def __init__(self):
        self.battle_spaces = self.create_battle_spaces()

    def create_battle_spaces(self):
        spaces = []
        spaces.append(BattleSpace(196, 207, 'production', 1, 'sea', 'west_europe', 1))
        spaces.append(BattleSpace(258, 207, 'research', 1, 'land', 'west_europe', 1))
        spaces.append(BattleSpace(320, 207, 'propaganda', 1,  'both', 'west_europe', 1))
        spaces.append(BattleSpace(196, 269, 'bombing', 1, 'land', 'west_europe', 2))
        spaces.append(BattleSpace(258, 269, 'production', 1, 'land', 'west_europe', 2))
        spaces.append(BattleSpace(320, 269, 'blank', 0, 'sea', 'west_europe', 2))
        spaces.append(BattleSpace(196, 331, 'res_industry', 1, 'both', 'west_europe', 3))
        spaces.append(BattleSpace(258, 331, 'strategic', 3,  'land', 'west_europe', 3))
        spaces.append(BattleSpace(320, 331, 'blank', 0, 'both', 'west_europe', 3))
        spaces.append(BattleSpace(111, 475, 'bombing', 1, 'sea', 'pacific', 1))
        spaces.append(BattleSpace(173, 475, 'research', 1, 'sea', 'pacific', 1))
        spaces.append(BattleSpace(111, 537, 'imp_research', 2, 'sea', 'pacific', 2)) 
        spaces.append(BattleSpace(173, 537, 'production', 1, 'sea', 'pacific', 2)) 
        spaces.append(BattleSpace(235, 537, 'strategic', 2, 'sea', 'pacific', 2)) 
        spaces.append(BattleSpace(297, 537, 'blank', 0, 'sea', 'pacific', 2)) 
        spaces.append(BattleSpace(111, 599, 'bombing', 1, 'sea', 'pacific', 3)) 
        spaces.append(BattleSpace(173, 599, 'propaganda', 2, 'sea', 'pacific', 3)) 
        spaces.append(BattleSpace(235, 599, 'blank', 0, 'both', 'pacific', 3))
        spaces.append(BattleSpace(669, 139, 'tactical', 1, 'land', 'east_europe', 1))
        spaces.append(BattleSpace(731, 139, 'production', 1, 'land', 'east_europe', 1))  
        spaces.append(BattleSpace(669, 201, 'propaganda', 1, 'land', 'east_europe', 2))  
        spaces.append(BattleSpace(731, 201, 'imp_research', 2, 'land', 'east_europe', 2))  
        spaces.append(BattleSpace(793, 201, 'blank', 0, 'both', 'east_europe', 2))  
        spaces.append(BattleSpace(669, 263, 'bombing', 1, 'land', 'east_europe', 3))  
        spaces.append(BattleSpace(731, 263, 'tactical', 2, 'land', 'east_europe', 3))  
        spaces.append(BattleSpace(793, 263, 'strategic', 3, 'land', 'east_europe', 3))
        spaces.append(BattleSpace(855, 263, 'propaganda', 2, 'land', 'east_europe', 3))
        spaces.append(BattleSpace(917, 263, 'blank', 0, 'land', 'east_europe', 3))
        spaces.append(BattleSpace(579, 411, 'strategic', 3, 'land', 'africa', 1))
        spaces.append(BattleSpace(641, 411, 'tactical', 1, 'sea', 'africa', 1))
        spaces.append(BattleSpace(703, 411, 'research', 1, 'both', 'africa', 1))
        spaces.append(BattleSpace(765, 411, 'propaganda', 1, 'both', 'africa', 1))
        spaces.append(BattleSpace(579, 473, 'tactical', 2, 'land', 'africa', 2))
        spaces.append(BattleSpace(641, 473, 'imp_production', 2, 'sea', 'africa', 2))
        spaces.append(BattleSpace(703, 473, 'blank', 0, 'both', 'africa', 2))
        spaces.append(BattleSpace(725, 617, 'propaganda', 2, 'sea', 'asia', 1))
        spaces.append(BattleSpace(787, 617, 'propaganda', 1, 'both', 'asia', 1))
        spaces.append(BattleSpace(849, 617, 'strategic', 1, 'both', 'asia', 1))
        spaces.append(BattleSpace(725, 679, 'bombing', 1, 'sea', 'asia', 2))
        spaces.append(BattleSpace(787, 679, 'propaganda', 2, 'land', 'asia', 2))
        spaces.append(BattleSpace(849, 679, 'blank', 0, 'both', 'asia', 2))

        return spaces

if __name__ == '__main__':
    space1 = BattleSpace(196, 207, 'production', 'sea', 'west europe', 1)
    print(space1.type)
    print(space1.rect)



   

        
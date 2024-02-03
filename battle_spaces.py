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
'''

class BattleSpace:
    ''' these are the spaces on the game board '''
    def __init__(self, x, y, type, theater, campaign):
        self.x = x
        self.y = y
        self.type = type
        self.theater = theater
        self.campaign = campaign
        self.occupied = False

    def draw(self, surface):
        # creates transparent rect
        invisible_rect = pygame.draw.rect(surface, (255, 255, 255, 100), pygame.Rect(self.x, self.y, 50, 50)) 
        return invisible_rect

if __name__ == '__main__':
    space1 = BattleSpace(196, 207, 'production', 'west europe', 1)
    print(space1.type)

   

        
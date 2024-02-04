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
    def __init__(self, x, y, effect, type, theater, campaign):
        self.x = x
        self.y = y
        self.effect = effect
        self.type = type
        self.theater = theater
        self.campaign = campaign
        self.occupied = False
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, surface):
        # creates transparent rect
        invisible_rect = pygame.draw.rect(surface, (255, 255, 255, 0), self.rect) 
        return invisible_rect

if __name__ == '__main__':
    space1 = BattleSpace(196, 207, 'production', 'sea', 'west europe', 1)
    print(space1.type)
    print(space1.rect)

   

        
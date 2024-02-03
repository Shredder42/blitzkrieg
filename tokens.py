import os
import pygame

class AlliedToken:
    ''' these are the game pieces'''
    def __init__(self, x, y, token_image, value):
        # self.x = x
        # self.y = y
        self.value = value
        self.token_image = token_image
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_image(self):
        image = pygame.image.load(os.path.join('images', self.token_image))
        image = pygame.transform.scale(image, (50, 50))
        return image
    
    def draw(self, surface):
        return surface.blit(self.image, self.rect)


if __name__ == '__main__':
    token1 = AlliedToken(10, 10, 'allied_army_1.png', 1)
        

        

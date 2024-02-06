import os
import pygame


class Token:
    ''' these are the game pieces'''
    need to deal with the initial rect values
    def __init__(self, side, unit, value, x, y, token_image):
        self.side = side
        self.unit = unit
        self.value = value      
        self.token_image = token_image
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        self.moving = False

    def load_image(self):
        image = pygame.image.load(os.path.join('images', self.token_image))
        image = pygame.transform.scale(image, (50, 50))
        return image
    
    def draw(self, surface):
        return surface.blit(self.image, self.rect)
    
    def clicked_token(self, pos):
        if self.rect.collidepoint(pos):
            print('clicked on token')
            self.moving = True

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

    def place_token(self, space):
        if self.moving:
            if self.match_type_and_unit(space) and (self.rect.collidepoint(space.rect.center) and not space.occupied):
                self.rect.center = space.rect.center
                space.occupied = True
            else:
                self.rect.x = self.original_x
                self.rect.y = self.original_y

        self.moving = False


if __name__ == '__main__':
    token1 = Token('allied', 'army', 1, 10, 10, 'allied_army_1.png')
    print(token1.moving)
        

        

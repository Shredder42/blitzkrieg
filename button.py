import pygame
import pygame.font

pygame.font.init()

class Button:
    def __init__(self):
        self.width = 310
        self.height = 30
        self.button_color = (255, 255, 255) # white
        self.text_color = (0, 0, 0) # black
        self.rect = pygame.Rect(10, 719, self.width, self.height)
        self.font = pygame.font.SysFont('times new roman', 20)



    def draw(self, surface, turn):
        self.msg_image = self.font.render(f'{turn.title()} commander, click to give orders', True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        surface.fill(self.button_color, self.rect)
        surface.blit(self.msg_image, self.msg_image_rect)
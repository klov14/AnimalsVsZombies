import pygame
#import random
import os

from fileuploads import *
from constants import *


class Text(pygame.sprite.Sprite):
    shadow_offset = 3
    def __init__(self, text, font, text_color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(text, True, BLACK)
        self.image.blit(font.render(text, True, text_color), (-self.shadow_offset, -self.shadow_offset))
        self.rect = self.image.get_rect()

        # self.rect.x = pos[0]
        # self.rect.y = pos[1]
        (self.rect.x, self.rect.y) = pos

    def update(self):
        pass

class Button(pygame.sprite.Sprite):
    def __init__(self, text, font, pos, command):
        pygame.sprite.Sprite.__init__(self)

        self.text_hovered = Text(text, font, RED, pos)
        self.text_not_hovered = Text(text, font, WHITE, pos)
        # self.img_hovered = img_hovered
        # self.img_not_hovered = img_not_hovered

        self.image = self.text_not_hovered.image
        self.rect = self.text_not_hovered.image.get_rect()
        # self.rect.x = pos[0]
        # self.rect.y = pos[1]
        (self.rect.x, self.rect.y) = pos
        self.command = command
        self.hovered = False
        self.clicked = False

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                sound_menu_select.play()
                self.hovered = True
            self.image = self.text_hovered.image
            if pygame.mouse.get_pressed()[0]:
                if not self.clicked:
                    sound_click.play()
                    self.clicked = True
                self.command[0]([a for a in self.command[1:]])
        else:
            self.hovered = False
            self.clicked = False
            self.image = self.text_not_hovered.image




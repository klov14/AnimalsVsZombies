import pygame
#import random
import os

from constants import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

land_img = pygame.image.load(os.path.join(img_folder, 'land.png')).convert()
# land_img = pygame.transform.scale(land_img, (150, 150))

spawner_img = pygame.image.load(os.path.join(img_folder, 'spawner.png')).convert()

# units
UNIT_SIZE = (75, 75)
unit_g_0_img = pygame.image.load(os.path.join(img_folder, 'unit-g-0.png')).convert_alpha()
unit_g_0_img = pygame.transform.scale(unit_g_0_img, UNIT_SIZE)

unit_g_1_img = pygame.image.load(os.path.join(img_folder, 'unit-g-1.png')).convert_alpha()
unit_g_1_img = pygame.transform.scale(unit_g_1_img, UNIT_SIZE)

# enemy

enemy_folder = os.path.join(img_folder, 'enemy')

enemy_appear_folder = os.path.join(enemy_folder, 'appear')
enemy_attack_folder = os.path.join(enemy_folder, 'attack')
enemy_die_folder = os.path.join(enemy_folder, 'die')
enemy_idle_folder = os.path.join(enemy_folder, 'idle')
enemy_walk_folder = os.path.join(enemy_folder, 'walk')

ENEMY_SIZE = (90, 90)

enemy_appear_animation = [pygame.image.load(os.path.join(enemy_appear_folder, ('appear_' + str(x) + '.png'))) for x in range(1,11)]
for a in range(len(enemy_appear_animation)):
    enemy_appear_animation[a] = pygame.transform.scale(enemy_appear_animation[a], ENEMY_SIZE)

enemy_attack_animation = [pygame.image.load(os.path.join(enemy_attack_folder, ('attack_' + str(x) + '.png'))) for x in range(1, 9)]
for a in range(len(enemy_attack_animation)):
    enemy_attack_animation[a] = pygame.transform.scale(enemy_attack_animation[a], ENEMY_SIZE)

enemy_die_animation = [pygame.image.load(os.path.join(enemy_die_folder, ('die_' + str(x) + '.png'))) for x in range(1, 9)]
for a in range(len(enemy_die_animation)):
    enemy_die_animation[a] = pygame.transform.scale(enemy_die_animation[a], ENEMY_SIZE)

enemy_idle_animation = [pygame.image.load(os.path.join(enemy_idle_folder, ('idle_' + str(x) + '.png'))) for x in range(1, 7)]
for a in range(len(enemy_idle_animation)):
    enemy_idle_animation[a] = pygame.transform.scale(enemy_idle_animation[a], ENEMY_SIZE)

enemy_walk_animation = [pygame.image.load(os.path.join(enemy_walk_folder, ('walk_' + str(x) + '.png'))) for x in range(1, 9)]
for a in range(len(enemy_walk_animation)):
    enemy_walk_animation[a] = pygame.transform.scale(enemy_walk_animation[a], ENEMY_SIZE)

bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet.png')).convert()
bullet_img.set_colorkey(BLACK)


bg_folder = os.path.join(img_folder, 'bg')

main_menu_bg = pygame.image.load(os.path.join(bg_folder, 'main-menu-background.jpg')).convert()
main_menu_bg = pygame.transform.scale(main_menu_bg, (WIDTH, HEIGHT))

game_bg = pygame.image.load(os.path.join(bg_folder, 'game-background.jfif')).convert()
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))


music_folder = os.path.join(game_folder, 'music')

sound_menu_select = pygame.mixer.Sound(os.path.join(music_folder, 'select.wav'))
sound_menu_select.set_volume(0.05)

sound_click = pygame.mixer.Sound(os.path.join(music_folder, 'click.wav'))

shoot_sound = pygame.mixer.Sound(os.path.join(music_folder, 'shoot.wav'))
shoot_sound.set_volume(0.5)

hit_sound = pygame.mixer.Sound(os.path.join(music_folder, 'hit.wav'))
hit_sound.set_volume(1)

death_sound = pygame.mixer.Sound(os.path.join(music_folder, 'death.wav'))
death_sound.set_volume(0.7)

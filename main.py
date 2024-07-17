import pygame
#import random
import os

# https://stackoverflow.com/questions/18273722/pygame-sound-delay/18513365
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

from constants import *
from fileuploads import *
from sprites import *
from gameLogic import *


### GAME FUNCTIONS ###

GAME_STATE = "Main menu" # Main menu | Game
GAME_IS_RUNNING = True

def game_state_change(args):
    global GAME_STATE
    GAME_STATE = args[0]

def game_quit(args):
    global GAME_IS_RUNNING
    GAME_IS_RUNNING = False

def change_difficulty(args):
    global DIFFICULTY
    DIFFICULTY = args[0]

def mainMenu():
    global GAME_STATE
    global GAME_IS_RUNNING

    pygame.mixer.music.load(os.path.join(music_folder, 'main-theme.mp3'))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    main_menu_sprites = pygame.sprite.Group()

    font = pygame.font.SysFont(None, 125)

    start_button = Button('START', font, (WIDTH // 3, HEIGHT // 3), (game_state_change, "Game"))
    start_button.add(main_menu_sprites)

    font = pygame.font.SysFont(None, 75)

    exit_button = Button('EXIT', font, (WIDTH // 3 * 1.27, HEIGHT // 3 * 2), (game_quit,))
    exit_button.add(main_menu_sprites)

    font = pygame.font.SysFont(None, 55)

    difficulty_text = Text('Difficulty:', font, WHITE, (WIDTH // 3 * 2.2, HEIGHT // 8 * 1.45))
    difficulty_text.add(main_menu_sprites)


    font = pygame.font.SysFont(None, 45)
    difficulty_easy_button = Button('Easy', font, (WIDTH // 3 * 2.5, HEIGHT // 8 * 2), (change_difficulty, 1))
    difficulty_easy_button.add(main_menu_sprites)

    difficulty_normal_button = Button('Normal', font, (WIDTH // 3 * 2.5, HEIGHT // 8 * 2.6), (change_difficulty, 2))
    difficulty_normal_button.add(main_menu_sprites)

    difficulty_hard_button = Button('Hard', font, (WIDTH // 3 * 2.5, HEIGHT // 8 * 3.2), (change_difficulty, 3))
    difficulty_hard_button.add(main_menu_sprites)

    while GAME_STATE == "Main menu" and GAME_IS_RUNNING:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit([])

        main_menu_sprites.update()
        # DRAWING
        # screen.fill(BLACK)
        screen.blit(main_menu_bg, (0, 0))
        main_menu_sprites.draw(screen)
        pygame.display.update()

def game():
    global GAME_STATE
    global GAME_IS_RUNNING
    
    time_to_win = 10 * 1000
    game_start = pygame.time.get_ticks()

    pygame.mixer.music.load(os.path.join(music_folder, 'game-theme.mp3'))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

    player_group = pygame.sprite.Group()
    land_group = pygame.sprite.Group()
    units_group = pygame.sprite.Group()
    fire_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    road_num = 4
    road_len = 7
    field_offset = 15
    field_x = HEIGHT - field_offset - road_num * land_img.get_rect().h
    field = Field(road_num, road_len, (field_offset, field_x), DIFFICULTY)
    for road in field.roads:
        land_group.add(road.lands)

    player = Player(DIFFICULTY, field, fire_group, units_group)
    player.add(player_group)

    font = pygame.font.SysFont(None, 65)
    exit_buttton = Button('Menu', font, (WIDTH // 12 * 10, HEIGHT // 50), (game_state_change, "Main menu"))
    exit_buttton.add(player_group)

    while GAME_IS_RUNNING and GAME_STATE == 'Game':
        clock.tick(FPS)

        now = pygame.time.get_ticks()
        if now >= game_start + time_to_win:
            game_state_change(["Win"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit([])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for land in land_group.sprites():
                    res = land.check_and_resolve_click(event.pos, event.button, player)
                    if res is not None:
                        res.add(units_group)


        for unit in units_group.sprites():
            if "is_ready_to_shoot" in dir(unit):
                if unit.is_ready_to_shoot():
                    fire_group.add(unit.shoot())

        for enemy in enemy_group.sprites():
            if enemy.win:
                game_state_change(["Lost"])

        if player.is_ready_to_spawn():
            enemy_group.add(player.spawn_enemy())

        land_group.update()
        player_group.update()
        units_group.update()
        fire_group.update()
        enemy_group.update()

        screen.blit(game_bg, (0, 0))

        land_group.draw(screen)
        player_group.draw(screen)
        units_group.draw(screen)
        fire_group.draw(screen)
        enemy_group.draw(screen)
        pygame.display.update()

    land_group.empty()
    player_group.empty()
    units_group.empty()
    fire_group.empty()
    enemy_group.empty()
    
def lost_screen():

    pygame.mixer.music.load(os.path.join(music_folder, 'lost.wav'))
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(0)

    font = pygame.font.SysFont(None, 125)

    you_lost_text = Text('You lost!', font, WHITE, (WIDTH // 4 + 20, HEIGHT // 2.5 - 20))

    text_group = pygame.sprite.Group()
    you_lost_text.add(text_group)
    

    screen.blit(main_menu_bg, (0, 0))
    text_group.draw(screen)

    pygame.display.update()

    pygame.time.delay(4500)

    game_state_change(["Main menu"])

def win_screen():

    pygame.mixer.music.load(os.path.join(music_folder, 'win.mp3'))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(0)

    font = pygame.font.SysFont(None, 125)

    you_lost_text = Text('You won!', font, WHITE, (WIDTH // 4 + 20, HEIGHT // 2.5 - 20))

    text_group = pygame.sprite.Group()
    you_lost_text.add(text_group)
    

    screen.blit(main_menu_bg, (0, 0))
    text_group.draw(screen)

    pygame.display.update()

    pygame.time.delay(4500)

    game_state_change(["Main menu"])

def main():
    while GAME_IS_RUNNING:
        if GAME_STATE == "Main menu":
            mainMenu()
        if GAME_STATE == "Game":
            game()
        if GAME_STATE == "Lost":
            lost_screen()
        if GAME_STATE == "Win":
            win_screen()
    pygame.quit()

if __name__ == "__main__":
    main()


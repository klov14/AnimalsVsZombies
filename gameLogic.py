import pygame
import random
import os


from constants import *
from fileuploads import *
from sprites import *


class Land(pygame.sprite.Sprite):

    unit = None
    image = land_img
    difficulty = 1

    def __init__(self, pos, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.difficulty = difficulty

    # call this on click event,
    # if click was on it and it has a place
    # it returns the unit object
    # def check_click(self, mouse_pos, mouse_button, player):
    #     if self.has_unit:
    #         return None
    #     if self.rect.collidepoint(mouse_pos):
    #         if mouse_button == 1: # left click
    #             res = player.try_buy(0)
    #             if res is not None:
    #                 self.has_unit = True
    #             return res
    #         elif mouse_button == 3: # right click
    #             res = player.try_buy(1)
    #             if res is not None:
    #                 self.has_unit = True
    #             return res
    #         return None

    # if self.unit (as constructor) exists, then initiate it
    # and replace with instance
    def initUnit(self, difficulty):
        if self.unit is None:
            return
        self.unit = self.unit(self.rect.center, difficulty)
        self.unit.parent = self

    # call this on click event,
    # if click was on it and it has a place
    # it returns the unit object
    def check_and_resolve_click(self, mouse_pos, mouse_button, player):
        if self.unit is not None:
            return None
        if self.rect.collidepoint(mouse_pos):
            if mouse_button == 1: # left click
                self.unit = player.try_buy(0)
                self.initUnit(self.difficulty)
                return self.unit
            elif mouse_button == 3: # right click
                self.unit = player.try_buy(1)
                self.initUnit(self.difficulty)
                return self.unit
            return None

class Spawner(Land):
    image = spawner_img
    difficulty = 1

    def __init__(self, pos, difficulty):
        # pygame.sprite.Sprite.__init__(self)
        Land.__init__(self, pos, difficulty)
        self.difficulty = difficulty
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def check_and_resolve_click(self, mouse_pos, mouse_button, player):
        return None

class Unit(pygame.sprite.Sprite):
    hp = 100
    dmg = 35

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class GuardianStayer(Unit):
    image = unit_g_0_img
    difficulty = 1

    def __init__(self, pos, difficulty):
        Unit.__init__(self)

        self.difficulty = difficulty

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if self.hp <= 0:
            #! sound!
            self.parent.unit = None
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = bullet_img
    speed = 15
    dmg = 30

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()


class GuardianShooter(Unit):
    image = unit_g_1_img
    bullet_offset = 20
    time_to_shoot = 2000
    last_shoot_time = 0
    ready_to_shoot = False

    difficulty = 1

    def __init__(self, pos, difficulty):
        Unit.__init__(self)
        self.difficulty = difficulty
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_shoot_time = pygame.time.get_ticks()

    def shoot(self):
        new_pos = (self.rect.center[0] + 15, self.rect.center[1])
        bullet = Bullet(new_pos)
        self.ready_to_shoot = False
        self.last_shoot_time = pygame.time.get_ticks()
        shoot_sound.play()
        return bullet

    def is_ready_to_shoot(self):
        return self.ready_to_shoot


    def update(self):
        now = pygame.time.get_ticks()
        if now >= self.last_shoot_time + self.time_to_shoot:
            self.ready_to_shoot = True
        if self.hp <= 0:
            #! sound!
            self.parent.unit = None
            self.kill()
            
class Enemy(Unit):

    difficulty = 1
    speed = 1
    dmg = 15 * difficulty

    last_melee_time = 0
    melee_delay = 1000

    is_dead = False
    is_awake = False
    is_attacking = False
    # is_moving = False
    # animation_clock = 100
    animation = enemy_appear_animation
    image = enemy_appear_animation[9]
    cur_anim_idx = 9
    pos = (0, 0)

    inner_pulse = 0
    inner_pulse_max = 3

    fire_group = None
    units_group = None

    def __init__(self, pos, fire_group, units_group, difficulty):
        Unit.__init__(self)

        self.win = False

        self.difficulty = difficulty
        self.speed *= self.difficulty

        self.dmg = 15 * self.difficulty

        self.last_melee_time = 0

        self.fire_group = fire_group
        self.units_group = units_group

        self.appear()

        # self.rect.x, self.rect.y = pos
        self.rect.center = pos


    def appear(self):
        self.image = enemy_appear_animation[0]
        self.animation = enemy_appear_animation
        self.cur_anim_idx = 0
        self.rect = self.image.get_rect()

    def die(self):
        self.is_dead = True
        self.image = enemy_die_animation[0]
        self.animation = enemy_die_animation
        self.cur_anim_idx = 0
        pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def attack(self):
        self.is_attacking = True
        self.animation = enemy_attack_animation
        self.image = enemy_attack_animation[0]
        self.cur_anim_idx = 0
        pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):

        if self.rect.x < 15:
            self.win = True

        if self.hp <= 0 and not self.is_dead:
            death_sound.play()
            self.die()

        bullet_collided = pygame.sprite.spritecollideany(self, self.fire_group)
        if bullet_collided is not None:
            self.hp -= bullet_collided.dmg // self.difficulty
            hit_sound.play()
            bullet_collided.kill()

        unit_collided = pygame.sprite.spritecollideany(self, self.units_group)
        if unit_collided is not None and not self.is_dead:
            if not self.is_attacking:
                self.attack()
            now = pygame.time.get_ticks()
            if now >= self.last_melee_time + self.melee_delay:
                self.last_melee_time = now
                self.hp -= unit_collided.dmg // self.difficulty
                hit_sound.play()
                unit_collided.hp -= self.dmg * self.difficulty
        elif self.is_attacking:
            self.is_attacking = False
            if not self.is_dead:
                self.animation = enemy_walk_animation

        #animations
        self.inner_pulse += 1
        if self.is_awake and not self.is_dead and not self.is_attacking:
            self.rect.x -= self.speed
        self.pos = self.rect.center
        if self.cur_anim_idx + 1 >= len(self.animation): # if end of animation
            if self.animation == enemy_appear_animation:
                self.is_awake = True
                self.animation = enemy_walk_animation
            if self.animation == enemy_die_animation:
                self.kill()
            self.cur_anim_idx = 0
        else:
            if self.inner_pulse >= self.inner_pulse_max:
                self.inner_pulse = 0
                self.cur_anim_idx += 1
                self.image = self.animation[self.cur_anim_idx]
                self.rect = self.image.get_rect()
                self.rect.center = self.pos

class Road():
    lands = []
    difficulty = 1

    def __init__(self, land_num, start_pos, difficulty):
        self.lands = []
        self.difficulty = difficulty
        offset = 0
        for _ in range(land_num):
            self.lands.append(Land((offset + start_pos[0], start_pos[1]), difficulty))
            offset += land_img.get_rect().w
        self.lands.append(Spawner((offset + start_pos[0], start_pos[1]), difficulty))

    def __del__(self):
        del self.lands

class Field():
    roads = []
    difficulty = 1

    def __init__(self, roadNum, land_num, start_pos, difficulty):
        self.roads = []
        self.difficulty = difficulty
        offset = 0
        for _ in range(roadNum):
            self.roads.append(Road(land_num, (start_pos[0], start_pos[1] + offset), difficulty))
            offset += land_img.get_rect().h

    def __del__(self):
        del self.roads


class Player(pygame.sprite.Sprite):
    money = 80
    last_moneyup_time = 0
    money_delay = 1000
    money_raise = 15
    font = pygame.font.SysFont(None, 75)
    pos = (5, 5)
    difficulty = 1

    last_spawn_time = 0
    spawn_delay = 3000 // difficulty

    ready_to_spawn = False

    field = None

    fire_group = None
    units_group = None


    shop = [(15, GuardianStayer), (25, GuardianShooter)]

    def __init__(self, difficulty, field, fire_group, units_group):
        pygame.sprite.Sprite.__init__(self)
        
        self.difficulty = difficulty
        # self.money_raise = self.money_raise // self.difficulty
        self.spawn_delay = 6000 // difficulty

        money_text = Text('Money: ' + str(self.money), self.font, YELLOW, self.pos)
        self.image = money_text.image
        self.rect = money_text.rect
        self.last_moneyup_time = pygame.time.get_ticks()
        self.ready_to_spawn = False

        self.field = field

        self.fire_group = fire_group
        self.units_group = units_group


    def money_set(self, new_money_amount):
        self.money = new_money_amount
        money_new_text = Text('Money: ' + str(self.money), self.font, YELLOW, self.pos)
        self.image = money_new_text.image
        self.rect = money_new_text.rect

    def spawn_enemy(self):
        if self.ready_to_spawn == False:
            return None
        self.ready_to_spawn = False
        road_to_spawn = random.randint(0, len(self.field.roads) - 1)
        pos = self.field.roads[road_to_spawn].lands[-1].rect.center
        # print("Total roads:" + str(len(self.field.roads)))
        # for e in self.field.roads:
        #     print("----NEW ROAD----")
        #     print("TOTAL LANDS: " + str(len(e.lands)))
        #     # for i in e.lands:
        #     #     print(i.rect)
        return Enemy(pos, self.fire_group, self.units_group, self.difficulty)

    def is_ready_to_spawn(self):
        return self.ready_to_spawn

    def update(self):
        now = pygame.time.get_ticks()
        if now >= self.money_delay + self.last_moneyup_time:
            self.money_set(self.money + self.money_raise)
            self.last_moneyup_time = now
        if now >= self.spawn_delay + self.last_spawn_time:
            self.ready_to_spawn = True
            self.last_spawn_time = now

    # call this when attempt to buy a unit
    # if player has enough money for that unit
    # it will return the unit object
    def try_buy(self, unit_id):
        price = self.shop[unit_id][0]
        if price > self.money:
            return None
        else:
            self.money_set(self.money - price)
            sound_click.play()
            return self.shop[unit_id][1]


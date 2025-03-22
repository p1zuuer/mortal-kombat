import pygame
import os
import sys



pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 600
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lvl = 'game'

from load import *


class FON:
    def __init__(self):
        self.timer = 0
        self.frame = 0
        self.image = fon_image

    def update(self):
        self.timer += 2
        sc.blit(self.image[self.frame], (0, 0))
        if self.timer / FPS > 0.1:
            if self.frame == len(self.image) - 1:
                self.frame = 0
            else:
                self.frame += 1
            self.timer = 0


fon = FON()


class Player_1(pygame.sprite.Sprite):
    def __init__(self, image_lists):
        super().__init__()
        self.image_list = image_lists
        self.image = self.image_list['idle'][0]
        self.current_list_image = self.image_list['idle']
        self.rect = self.image.get_rect()
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.frame = 0
        self.timer_anime = 0
        self.dir = "right"
        self.hp = 100
        self.jump_step = -20
        self.is_jumping = False
        self.flag_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (200, 380)
        self.hp_bar = "blue"
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask_outline()
        self.mask_list = []
    def move(self, key):
        if key[pygame.K_d]:
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[pygame.K_a]:
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False

    def jump(self, key):
        if key[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
        if self.is_jumping:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.is_jumping = False
                self.jump_step = -20

    def attack(self, key):
        if key[pygame.K_e] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_idle = False
            self.anime_run = False
            self.flag_damage = True

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = self.image_list['idle']
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0

        if self.anime_idle:
            self.current_list_image = self.image_list['idle']
        elif self.anime_run:
            self.current_list_image = self.image_list['run']
        elif self.anime_atk:
            self.current_list_image = self.image_list['atk']

        if self.dir == "right":
            self.image = self.current_list_image[self.frame]
        else:
            self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)

    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (0, 0, 600 * self.hp / 100, 50))

    def update(self, player_2):
        if self.rect.center[0] - player_2.rect.center[0] < 0:
            self.dir = "right"
        else:
            self.dir = "left"
        key = pygame.key.get_pressed()
        self.move(key)
        self.jump(key)
        self.attack(key)
        self.animation()
        self.draw_hp_bar()

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline=self.mask_outline()
        self.mask_list = []
        for i in  self.mask_outline:
            self.mask_list.append((i[0]+ self.rect.x,i[1]+self.rect.y))

        if self.flag_damage == True:
            if len(set(self.mask_list)&set(player_2.mask_list)) > 0:

                player_2.hp -=10
                self.flag_damage = False
            if self.hp == 0:
                self.kill()


class Player_2(pygame.sprite.Sprite):
    def __init__(self, image_lists):
        super().__init__()
        self.image_list = image_lists
        self.image = self.image_list['idle'][0]
        self.current_list_image = self.image_list['idle']
        self.rect = self.image.get_rect()
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.frame = 0
        self.timer_anime = 0
        self.dir = "right"
        self.hp = 100
        self.jump_step = -20
        self.is_jumping = False
        self.flag_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (1000, 380)
        self.hp_bar = "red"
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask_outline()
        self.mask_list = []

    def move(self, key):
        if key[pygame.K_l]:
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[pygame.K_j]:
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False

    def jump(self, key):
        if key[pygame.K_u] and not self.is_jumping:
            self.is_jumping = True
        if self.is_jumping:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.is_jumping = False
                self.jump_step = -20

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = player_2_idle_image
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0

        if self.anime_idle:
            self.current_list_image = self.image_list['idle']
        elif self.anime_run:
            self.current_list_image = self.image_list['run']
        elif self.anime_atk:
            self.current_list_image = self.image_list['atk']
        try:
            if self.dir == "left":
                self.image = self.current_list_image[self.frame]
            else:
                self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)
        except:
            self.frame = 0

    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (600, 0, 600 * self.hp / 100, 50))

    def attack(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_o] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_idle = False
            self.anime_run = False
            self.flag_damage = True

    def update(self):
        key = pygame.key.get_pressed()
        self.move(key)
        self.jump(key)
        self.attack()
        self.animation()
        self.draw_hp_bar()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask_outline()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))

        if self.flag_damage == True:
            if len(set(self.mask_list) & set(player_1.mask_list)) > 0:

                player_1.hp -= 10
                self.flag_damage = False
            if self.hp == 0:
                self.kill()


class Player_3(pygame.sprite.Sprite):
    def __init__(self, image_lists):
        super().__init__()
        self.image_list = image_lists
        self.image = self.image_list['idle'][0]
        self.current_list_image = self.image_list['idle']
        self.rect = self.image.get_rect()
        self.anime_idle = True
        self.anime_run = False
        self.anime_atk = False
        self.frame = 0
        self.timer_anime = 0
        self.dir = "right"
        self.hp = 100
        self.jump_step = -20
        self.is_jumping = False
        self.flag_damage = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (1000, 380)
        self.hp_bar = "red"
    def move(self, key):
        if key[pygame.K_l]:
            self.rect.x += 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        elif key[pygame.K_j]:
            self.rect.x -= 2
            self.anime_idle = False
            if not self.anime_atk:
                self.anime_run = True
        else:
            if not self.anime_atk:
                self.anime_idle = True
            self.anime_run = False

    def jump(self, key):
        if key[pygame.K_u] and not self.is_jumping:
            self.is_jumping = True
        if self.is_jumping:
            if self.jump_step <= 20:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.is_jumping = False
                self.jump_step = -20

    def animation(self):
        self.timer_anime += 2
        if self.timer_anime / FPS > 0.1:
            if self.frame == len(self.current_list_image) - 1:
                self.frame = 0
                if self.anime_atk:
                    self.current_list_image = player_2_idle_image
                    self.anime_atk = False
                    self.anime_idle = True
            else:
                self.frame += 1
            self.timer_anime = 0

        if self.anime_idle:
            self.current_list_image = self.image_list['idle']
        elif self.anime_run:
            self.current_list_image = self.image_list['run']
        elif self.anime_atk:
            self.current_list_image = self.image_list['atk']
        try:
            if self.dir == "left":
                self.image = self.current_list_image[self.frame]
            else:
                self.image = pygame.transform.flip(self.current_list_image[self.frame], True, False)
        except:
            self.frame = 0

    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (600, 0, 600 * self.hp / 100, 50))

    def attack(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_o] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_idle = False
            self.anime_run = False
            self.flag_damage = True

    def update(self):
        key = pygame.key.get_pressed()
        self.move(key)
        self.jump(key)
        self.attack()
        self.animation()
        self.draw_hp_bar()


def game():
    sc.fill("grey")
    fon.update()
    player_1_group.update(player_2)
    player_1_group.draw(sc)
    player_2_group.update()
    player_2_group.draw(sc)
    pygame.display.update()


def resatart():
    global fon, player_1_group, player_2_group, player_3_group, player_4_group, player_1, player_2, player_3, player_4


player_1_group = pygame.sprite.Group()
player_1 = Player_1({'idle': player_1_idle_image, 'run': player_1_run_image, 'atk': player_1_attack1_image})
player_1_group.add(player_1)

player_2_group = pygame.sprite.Group()
player_2 = Player_2({'idle': player_2_idle_image, 'run': player_2_run_image, 'atk': player_2_attack_image})
player_2_group.add(player_2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == 'game':
        game()
    clock.tick(FPS)

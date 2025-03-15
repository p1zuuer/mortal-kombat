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
def game():
    sc.fill("grey")
    fon.update()
    pygame.display.update()

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
        self.rect.center = (500, 380)
        self.hp_bar = "blue"
        self.key = pygame.key.get_pressed()

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
                    self.current_list_image = player_1_idle_image
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
        self.rect.center = (600, 380)
        self.hp_bar = "blue"
        self.key = pygame.key.get_pressed()

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
    def draw_hp_bar(self):
        pygame.draw.rect(sc, self.hp_bar, (0, 0, 600 * self.hp / 100, 50))

    def attack(self, key):
        if key[pygame.K_e] and not self.anime_atk:
            self.frame = 0
            self.anime_atk = True
            self.anime_idle = False
            self.anime_run = False
            self.flag_damage = True

def restart():
    global player1_group, player2_group, fon
    player_1group = pygame.sprite.Group()
    player_1=Player_1({'idle':player_1_idle_image,'run':player_1_run_image})
    player_1_group.add((player_1))
    player_2_group = Player_2({'idle':player_2_idle_image})
    player_2_group.add(player_2)
    player2_group = pygame.sprite.Group()
    fon = FON()

restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl =='game':
       game()
    clock.tick(FPS)

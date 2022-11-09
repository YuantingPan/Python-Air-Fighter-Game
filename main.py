import pygame
import random
from pygame.locals import *
from sys import exit
import time


'''
    TBA: 
        - player hp (√)
        - scoreboard (√)
        - welcome and ending page (√)
        - docstring
    Optional:
        - buff
'''

background_img= 'pics/grey.jpeg'
mouse_img = 'pics/fighter_1.png'
# enemy_1_img = 'pics/fast_fighter.png'
# enemy_2_img = 'pics/fighter_2.png'
enemy_3_img = 'pics/fighter_3.png'
enemy_4_img = 'pics/fighter_4.png'
enemy_5_img = 'pics/fighter_5.png'
# explosion_img = 'pics/explosion.png'

win_size = (640,1000)
clock = pygame.time.Clock()
Score = 0
Start = False
End = False

class Enemy:
    def __init__(self, image, scale, speed, hp, screen, win = win_size, freq=1., score=100):
        self.object = pygame.image.load(image).convert_alpha()
        self.object = pygame.transform.flip(self.object,flip_x=False,flip_y=True)
        self.object = pygame.transform.scale(self.object, scale)
        self.scale = scale
        self.speed = speed
        self.win = win
        self.freq = freq
        self.xloc = random.random() * (self.win[0] - self.scale[0])
        self.yloc = -100 - random.random()*100 / self.freq
        self.screen = screen
        self.hp = hp
        self.full_health = hp
        self.score = score


    def reset(self):
        self.xloc = random.random() * (self.win[0] - self.scale[0])
        self.yloc = -100 - random.random()*100 / self.freq
        self.hp = self.full_health

    def move(self, clocktime):
        self.yloc += self.speed * clocktime/1000
        if self.yloc > self.win[1]:
            self.reset()

    def show(self, clocktime):
        if self.hp <= 0:
            global Score
            Score += self.score
            self.reset()
            return [-1000, -1000, 0]
        self.move(clocktime)
        self.screen.blit(self.object, (self.xloc, self.yloc))
        return [self.xloc, self.yloc, self.scale[0]]


class Bullet:
    def __init__(self, bullets, screen, clocktime, bullet_scale=3, bullet_speed = 400):
        self.bullets = bullets
        self.screen = screen
        self.bullet_scale = bullet_scale
        self.clocktime = clocktime
        self.bullet_speed = bullet_speed

    def move(self):
        self.bullets = [b for b in self.bullets if b[1]>0]
        for bullet in self.bullets:
            pygame.draw.circle(self.screen, (0, 0, 0), bullet, self.bullet_scale, 0)
            bullet[1] -= self.bullet_speed * self.clocktime / 1000

def step(enemies, bullets, clocktime):
    E_loc = []
    for enemy in enemies:
        x,y,s = enemy.show(clocktime)
        E_loc.append([x,y,s])
    targets = [[x, x+s, y, y+s] for [x,y,s] in E_loc]
    for i in range(len(enemies)):
        target = targets[i]
        for bullet in bullets.bullets:
            if target[0] <= bullet[0] <= target[1] and target[2] <= bullet[1] <= target[3]:
                enemies[i].hp -= 1
                bullets.bullets.remove(bullet)
                break
    bullets.move()

def judge(enemies, bullets, clocktime):
    global End
    E_loc = []
    for enemy in enemies:
        x,y,s = enemy.show(clocktime)
        E_loc.append([x,y,s])
    targets = [[x, x+s, y, y+s] for [x,y,s] in E_loc]
    for i in range(len(enemies)):
        target = targets[i]
        for bullet in bullets.bullets:
            if target[0] <= bullet[0] <= target[1] and target[2] <= bullet[1] <= target[3]:
                End = True
                return End
    return End

def main():

    pygame.init()
    screen = pygame.display.set_mode(win_size, 0, 32)
    pygame.display.set_caption("Super Fighter Fight Premium Pro Plus ver 114.514")
    background = pygame.image.load(background_img).convert()
    mouse_cursor = pygame.image.load(mouse_img).convert_alpha()
    mouse_cursor = pygame.transform.scale(mouse_cursor, (75,75))
    enemy1 = Enemy(enemy_3_img, (60, 60), 200, 1, screen, win_size, score=100)
    enemy2 = Enemy(enemy_3_img, (60, 60), 250, 1, screen, win_size, score=100)
    enemy3 = Enemy(enemy_4_img, (80, 80), 150, 3, screen, win_size, score=300)
    enemy4 = Enemy(enemy_4_img, (80, 80), 250, 3, screen, win_size, freq=0.5, score=800)
    enemy5 = Enemy(enemy_5_img, (200, 200), 80, 8, screen, win_size, freq= 0.1, score=2500)
    enemy6 = Enemy(enemy_3_img, (60, 60), 300, 1, screen, win_size, score=300)
    enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]
    bullets = []  # position of bullets

    first = True
    prev_time = time.time()

    global Start
    global End
    global Score

    width = win_size[0]
    height = win_size[1]
    color_light = [120, 120, 120]
    color_dark = [90, 90, 90]
    bigfont = pygame.font.SysFont('Corbel', 35)
    smallfont = pygame.font.SysFont('Corbel', 20)
    funny_font = pygame.font.Font('freesansbold.ttf', 32)

    try:
        with open('logs/highest_score.txt', 'r') as f:
            Highest_score = int(f.read())
    except:
        Highest_score = 0

    while True:
        screen.blit(background, (0, 0))
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not Start:
                if width / 2 - 100 <= x <= width / 2 + 100 and height / 2 - 30 <= y <= height / 2 + 30:
                    Start = True
            if event.type == pygame.MOUSEBUTTONDOWN and End:
                if width / 2 - 100 <= x <= width / 2 + 100 and height / 2 +100 <= y <= height / 2 + 160:
                    End = False
                    Score = 0
                    main()  # try again!

        if End:
            if Score > Highest_score:
                with open('logs/highest_score.txt', 'w') as f:
                    f.write(str(Score))
                text = smallfont.render('New High Score! ', True, [0, 0, 0])
                screen.blit(text, (width / 2 - 60, height / 2 ))
            pygame.mouse.set_visible(True)
            text = bigfont.render('Game Over!', True, [0, 0, 0])
            screen.blit(text, (width / 2 - 80, height / 2 - 100))
            text = bigfont.render(f'Your Score: {Score}', True, [0, 0, 0])
            screen.blit(text, (width / 2 - 90, height / 2  - 50))
            if width / 2 - 100 <= x <= width / 2 + 100 and height / 2 +100 <= y <= height / 2 + 160:
                pygame.draw.rect(screen, color_dark, [width / 2 - 100, height / 2 +100, 200, 60])
            else:
                pygame.draw.rect(screen, color_light, [width / 2 - 100, height / 2 +100, 200, 60])
            text = bigfont.render('Try Again', True, [0, 0, 0])
            screen.blit(text, (width / 2 - 60, height / 2 + 115))
        else:
            if not Start:
                if width / 2 - 100 <= x <= width / 2 + 100 and height / 2 - 30 <= y <= height / 2 + 30:
                    pygame.draw.rect(screen, color_dark, [width / 2 - 100, height / 2 - 30, 200, 60])
                else:
                    pygame.draw.rect(screen, color_light, [width / 2 - 100, height / 2 - 30, 200, 60])
                text = bigfont.render('Start', True, [0,0,0])
                screen.blit(text, (width / 2 - 30, height / 2 - 15))
                text = smallfont.render(f'Highest Score: {Highest_score}', True, [0, 0, 0])
                screen.blit(text, (width / 2 - 80, height / 2 + 50))
            else:
                pygame.mouse.set_visible(False)
                screen.blit(mouse_cursor, (x - mouse_cursor.get_width() / 2, y - mouse_cursor.get_height() / 2))
                now_time = time.time()
                if first:
                    clock.tick()
                    first = False
                clocktime = clock.tick()
                if now_time - prev_time >= 0.3:
                    bullets.append([x,y - mouse_cursor.get_height() / 2])
                    prev_time = now_time
                bullet = Bullet(bullets, screen, clocktime)
                player = Bullet([[x,y]], screen, clocktime)
                judge(enemies, player, clocktime)
                step(enemies, bullet, clocktime)
                text_surface = funny_font.render(f'Score:{Score}', False, (0, 0, 0))
                screen.blit(text_surface, (10, 10))

        pygame.display.update()

if __name__ == "__main__":
    main()

import pygame
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)

pygame.mixer.music.play(-1)
# pygame.mixer.music.load('pictures/music.mp3')
# pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.play(-1)
boom_sound = pygame.mixer.Sound('sounds/boom.wav')
boom_sound.set_volume(0.4)

punch_sound = pygame.mixer.Sound('sounds/punch.mp3')
punch_sound.set_volume(0.4)

laser_sound = pygame.mixer.Sound('sounds/laser.mp3')
laser_sound.set_volume(0.15)

gun_sound = pygame.mixer.Sound('sounds/gun.mp3')
gun_sound.set_volume(0.3)

over_sound = pygame.mixer.Sound('sounds/game_over.mp3')
over_sound.set_volume(0.2)

win_sound = pygame.mixer.Sound('sounds/win.mp3')
win_sound.set_volume(0.3)

all_sprites = pygame.sprite.Group()

ship_group = pygame.sprite.Group()

fire_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

life_group = pygame.sprite.Group()

laser_group = pygame.sprite.Group()

boom_group = pygame.sprite.Group()

boom1_group = pygame.sprite.Group()

LIFE_AMOUNT = 3

ENEMY_AMOUNT = 4

BOSS_LIVES = 10


def load_image(name):
    fullname = f'pictures/{name}'
    image = pygame.image.load(fullname)
    return image


back = pygame.transform.scale(load_image('background.jpg'), (650, 790))
finish_back = pygame.transform.scale(load_image('end_background.jpg'), (690, 910))

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Life(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('life.png'), (60, 50))
    minus_life = pygame.transform.scale(load_image('minus_life.png'), (60, 50))

    def __init__(self, pos, row):
        super().__init__(all_sprites)
        self.image = Life.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.row = row
        self.add(life_group)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if LIFE_AMOUNT + 1 <= self.row:
            self.image = Life.minus_life


class Boom(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.timer = 0

        self.rows, self.columns = rows, columns

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = self.cur_frame + 1

        if self.cur_frame >= self.rows * self.columns - 1:
            self.rect.x = -100
            self.kill()

        self.image = self.frames[self.cur_frame]


class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(625, 730)
        self.setWindowTitle('Galaxy Warrior')

        self.pixmap = QPixmap('pictures/start_background.jpg')
        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 625, 730)
        self.back.setPixmap(self.pixmap)

        self.title = QLabel('Welcome to the "Galaxy Warrior"!', self)
        self.title.setGeometry(100, 90, 441, 41)
        self.title.setStyleSheet('font: 30pt Standard;')

        self.lvl1 = QPushButton('Level 1', self)
        self.lvl1.setGeometry(240, 210, 141, 51)
        self.lvl1.setStyleSheet('font: 30pt Standard; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);')

        self.lvl2 = QPushButton('Level 2', self)
        self.lvl2.setGeometry(240, 290, 141, 51)
        self.lvl2.setStyleSheet('font: 30pt Standard; background-color: rgb(0, 0, 255);')

        self.boss = QPushButton('BOSS', self)
        self.boss.setGeometry(240, 370, 141, 51)
        self.boss.setStyleSheet('font: 30pt Standard; color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);')

        self.manual = QPushButton('Manual', self)
        self.manual.setGeometry(240, 500, 141, 51)
        self.manual.setStyleSheet('font: 30pt Standard;')

        self.manual_page = Manual()

        self.lvl1.clicked.connect(self.level1)
        self.lvl2.clicked.connect(self.level2)
        self.boss.clicked.connect(self.boss_game)
        self.manual.clicked.connect(self.man)

    def man(self):
        self.manual_page.show()

    def level1(self):
        Level1()

    def level2(self):
        Level2()

    def boss_game(self):
        Level3()


class Level1:
    def __init__(self):
        super().__init__()
        self.sprites_init()
        self.main()

    def main(self):
        global LIFE_AMOUNT, all_sprites, ship_group, life_group, laser_group, boom_group, enemy_group, fire_group
        global boom1_group, ENEMY_AMOUNT

        LIFE_AMOUNT = 3

        ENEMY_AMOUNT = 3

        all_sprites = pygame.sprite.Group()
        ship_group = pygame.sprite.Group()
        life_group = pygame.sprite.Group()
        laser_group = pygame.sprite.Group()
        boom_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        boom1_group = pygame.sprite.Group()

        pygame.init()

        size = width, height = (690, 910)

        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Galaxy Warrior')

        my_font = pygame.font.SysFont('Standard', 40)
        score_txt = my_font.render('LEVEL 1', False, (255, 255, 255))

        k = 20
        self.surf = pygame.Surface((650, 790))
        pygame.mouse.set_visible(False)

        self.surf.blit(back, (0, 0))

        pygame.draw.line(self.surf, 'white', (0, 0), (649, 0), 1)
        pygame.draw.line(self.surf, 'white', (649, 0), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 789), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 0), (0, 789), 1)

        ship = Ship(all_sprites)

        Enemy(20, 170, time=30)
        Enemy(570, 100, direction=False, time=50)
        Enemy(300, 240, time=40)
        Life((590, 30), 1)
        Life((520, 30), 2)
        Life((450, 30), 3)

        fire_count = 100
        running = True
        while running:
            if ENEMY_AMOUNT <= 0:
                pygame.mixer.music.stop()
                win_sound.play()
                self.win()
                break
            if LIFE_AMOUNT <= 0:
                pygame.mixer.music.stop()
                over_sound.play()
                self.finish()
                break
            fire_count += 1
            all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEMOTION:
                    ship_group.update(event.pos, event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and fire_count >= 100:
                        gun_sound.play()
                        Fire((ship.rect.x, ship.rect.y))
                        fire_count = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and fire_count >= 100:
                    gun_sound.play()
                    Fire((ship.rect.x, ship.rect.y))
                    fire_count = 0

            self.screen.fill((0, 0, 100))
            self.screen.blit(self.surf, (k, 100))
            self.screen.blit(score_txt, (40, 45))
            all_sprites.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def finish(self):
        pygame.mouse.set_visible(True)

        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))

        draw_text(self.screen, 'GAME OVER!', 70, 340, 150, 'red')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def win(self):
        pygame.mouse.set_visible(True)

        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))
        draw_text(self.screen, 'LEVEL PASSED!', 70, 340, 150, 'green')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True

        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def sprites_init(self):
        img = pygame.transform.scale(load_image('life.png'), (60, 50))

        self.life1 = pygame.sprite.Sprite()
        self.life1.image = img
        self.life1.rect = self.life1.image.get_rect()
        self.life1.rect.x = 590
        self.life1.rect.y = 30

        self.life2 = pygame.sprite.Sprite()
        self.life2.image = img
        self.life2.rect = self.life2.image.get_rect()
        self.life2.rect.x = 520
        self.life2.rect.y = 30

        self.life3 = pygame.sprite.Sprite()
        self.life3.image = img
        self.life3.rect = self.life3.image.get_rect()
        self.life3.rect.x = 450
        self.life3.rect.y = 30

        ship = pygame.sprite.Sprite()
        ship.image = pygame.transform.scale(load_image('ship.png'), (100, 100))
        ship.rect = ship.image.get_rect()
        ship.rect.x = 300
        ship.rect.y = 750

        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.transform.scale(load_image('enemy.png'), (100, 100))
        enemy.rect = ship.image.get_rect()
        enemy.rect.x = 300
        enemy.rect.y = 300

        # all_sprites.add(self.life1)
        # all_sprites.add(self.life2)
        # all_sprites.add(self.life3)
        # all_sprites.add(ship)
        # all_sprites.add(enemy)


class Level2:
    def __init__(self):
        super().__init__()
        self.sprites_init()
        self.main()

    def main(self):
        global LIFE_AMOUNT, all_sprites, ship_group, life_group, laser_group, boom_group, enemy_group, fire_group
        global boom1_group, ENEMY_AMOUNT
        LIFE_AMOUNT = 3
        ENEMY_AMOUNT = 6

        all_sprites = pygame.sprite.Group()
        ship_group = pygame.sprite.Group()
        life_group = pygame.sprite.Group()
        laser_group = pygame.sprite.Group()
        boom_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        boom1_group = pygame.sprite.Group()
        pygame.init()

        size = width, height = (690, 910)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Galaxy Warrior')

        my_font = pygame.font.SysFont('Standard', 40)
        score_txt = my_font.render('LEVEL 2', False, (255, 255, 255))

        k = 20
        self.surf = pygame.Surface((650, 790))
        pygame.mouse.set_visible(False)

        self.surf.blit(back, (0, 0))
        pygame.draw.line(self.surf, 'white', (0, 0), (649, 0), 1)
        pygame.draw.line(self.surf, 'white', (649, 0), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 789), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 0), (0, 789), 1)

        ship = Ship(all_sprites)
        Enemy(20, 100, time=30, size=(90, 90))
        Enemy(60, 200, time=30, size=(70, 70))
        Enemy(100, 280, time=30, size=(50, 50))
        Enemy(140, 340, time=30, size=(50, 50))
        Enemy(180, 400, time=30, size=(40, 40))
        Enemy(220, 450, time=30, size=(40, 40))
        Life((590, 30), 1)
        Life((520, 30), 2)
        Life((450, 30), 3)
        fire_count = 100
        running = True
        while running:
            if ENEMY_AMOUNT <= 0:
                pygame.mixer.music.stop()
                win_sound.play()
                self.win()
                break
            if LIFE_AMOUNT <= 0:
                pygame.mixer.music.stop()
                over_sound.play()
                self.finish()
                break
            fire_count += 1
            all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEMOTION:
                    ship_group.update(event.pos, event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and fire_count >= 100:
                        gun_sound.play()
                        Fire((ship.rect.x, ship.rect.y))
                        fire_count = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and fire_count >= 100:
                    gun_sound.play()
                    Fire((ship.rect.x, ship.rect.y))
                    fire_count = 0

            self.screen.fill((0, 0, 100))
            self.screen.blit(self.surf, (k, 100))
            self.screen.blit(score_txt, (40, 45))
            all_sprites.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def finish(self):
        pygame.mouse.set_visible(True)
        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))
        draw_text(self.screen, 'GAME OVER!', 70, 340, 150, 'red')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def win(self):
        pygame.mouse.set_visible(True)
        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))
        draw_text(self.screen, 'LEVEL PASSED!', 70, 340, 150, 'green')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def sprites_init(self):
        img = pygame.transform.scale(load_image('life.png'), (60, 50))

        self.life1 = pygame.sprite.Sprite()
        self.life1.image = img
        self.life1.rect = self.life1.image.get_rect()
        self.life1.rect.x = 590
        self.life1.rect.y = 30

        self.life2 = pygame.sprite.Sprite()
        self.life2.image = img
        self.life2.rect = self.life2.image.get_rect()
        self.life2.rect.x = 520
        self.life2.rect.y = 30

        self.life3 = pygame.sprite.Sprite()
        self.life3.image = img
        self.life3.rect = self.life3.image.get_rect()
        self.life3.rect.x = 450
        self.life3.rect.y = 30

        ship = pygame.sprite.Sprite()
        ship.image = pygame.transform.scale(load_image('ship.png'), (100, 100))
        ship.rect = ship.image.get_rect()
        ship.rect.x = 300
        ship.rect.y = 750

        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.transform.scale(load_image('enemy.png'), (100, 100))
        enemy.rect = ship.image.get_rect()
        enemy.rect.x = 300
        enemy.rect.y = 300

        # all_sprites.add(self.life1)
        # all_sprites.add(self.life2)
        # all_sprites.add(self.life3)
        # all_sprites.add(ship)
        # all_sprites.add(enemy)


boss = None


class Level3:
    def __init__(self):
        super().__init__()
        self.sprites_init()
        self.main()

    def main(self):
        global LIFE_AMOUNT, all_sprites, ship_group, life_group, laser_group, boom_group, enemy_group, fire_group
        global boom1_group, ENEMY_AMOUNT, BOSS_LIVES
        LIFE_AMOUNT = 1
        ENEMY_AMOUNT = 10
        BOSS_LIVES = 15

        all_sprites = pygame.sprite.Group()
        ship_group = pygame.sprite.Group()
        life_group = pygame.sprite.Group()
        laser_group = pygame.sprite.Group()
        boom_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        boom1_group = pygame.sprite.Group()
        pygame.init()

        size = width, height = (690, 910)
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Galaxy Warrior')

        my_font = pygame.font.SysFont('Standard', 40)
        score_txt = my_font.render('BOSS LEVEL', False, (255, 255, 255))
        lives_txt = my_font.render(f'BOSS LIVES: {BOSS_LIVES}', False, 'red')

        k = 20
        self.surf = pygame.Surface((650, 790))
        pygame.mouse.set_visible(False)

        self.surf.blit(back, (0, 0))
        pygame.draw.line(self.surf, 'white', (0, 0), (649, 0), 1)
        pygame.draw.line(self.surf, 'white', (649, 0), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 789), (649, 789), 1)
        pygame.draw.line(self.surf, 'white', (0, 0), (0, 789), 1)

        ship = Ship(all_sprites)
        global boss
        boss = BossEnemy()
        Life((590, 30), 1)
        fire_count = 100
        running = True
        while running:
            lives_txt = my_font.render(f'BOSS LIVES: {BOSS_LIVES}', False, 'red')
            if BOSS_LIVES <= 0:
                pygame.mixer.music.stop()
                win_sound.play()
                self.win()
                break
            if LIFE_AMOUNT <= 0:
                pygame.mixer.music.stop()
                over_sound.play()
                self.finish()
                break
            fire_count += 1
            all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEMOTION:
                    ship_group.update(event.pos, event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and fire_count >= 100:
                        gun_sound.play()
                        FireBoss((ship.rect.x, ship.rect.y))
                        fire_count = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and fire_count >= 100:
                    gun_sound.play()
                    FireBoss((ship.rect.x, ship.rect.y))
                    fire_count = 0

            self.screen.fill((0, 0, 100))
            self.screen.blit(self.surf, (k, 100))
            self.screen.blit(score_txt, (40, 45))
            self.screen.blit(lives_txt, (250, 45))
            all_sprites.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def finish(self):
        pygame.mouse.set_visible(True)
        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))
        draw_text(self.screen, 'GAME OVER!', 70, 340, 150, 'red')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def win(self):
        pygame.mouse.set_visible(True)
        self.surf = pygame.Surface((690, 910))
        self.surf.blit(finish_back, (0, 0))
        self.screen.fill((0, 0, 100))
        self.screen.blit(self.surf, (0, 0))
        draw_text(self.screen, 'LEVEL PASSED!', 70, 340, 150, 'green')
        draw_text(self.screen, 'press any key to continue', 20, 350, 600, 'white')
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def sprites_init(self):
        img = pygame.transform.scale(load_image('life.png'), (60, 50))

        self.life1 = pygame.sprite.Sprite()
        self.life1.image = img
        self.life1.rect = self.life1.image.get_rect()
        self.life1.rect.x = 590
        self.life1.rect.y = 30

        self.life2 = pygame.sprite.Sprite()
        self.life2.image = img
        self.life2.rect = self.life2.image.get_rect()
        self.life2.rect.x = 520
        self.life2.rect.y = 30

        self.life3 = pygame.sprite.Sprite()
        self.life3.image = img
        self.life3.rect = self.life3.image.get_rect()
        self.life3.rect.x = 450
        self.life3.rect.y = 30

        ship = pygame.sprite.Sprite()
        ship.image = pygame.transform.scale(load_image('ship.png'), (100, 100))
        ship.rect = ship.image.get_rect()
        ship.rect.x = 300
        ship.rect.y = 750

        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.transform.scale(load_image('enemy.png'), (100, 100))
        enemy.rect = ship.image.get_rect()
        enemy.rect.x = 300
        enemy.rect.y = 300

        # all_sprites.add(self.life1)
        # all_sprites.add(self.life2)
        # all_sprites.add(self.life3)
        # all_sprites.add(ship)
        # all_sprites.add(enemy)


class Ship(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('ship.png'), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 750
        self.add(ship_group)

    def update(self, pos=(300, 750), *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if pos[0] < 70:
                self.rect.x = 20
            elif pos[0] >= 620:
                self.rect.x = 569
            else:
                self.rect.x = pos[0] - 50


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=True, time=100, size=(70, 70), speed=4):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('enemy.png'), size)
        self.rect = self.image.get_rect()
        self.timer = 0
        self.time = time
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.add(enemy_group)
        self.flag = direction
        self.dead = False
        self.speed = speed

    def update(self):
        if pygame.sprite.spritecollideany(self, fire_group) and self.dead is False:
            # Boom(load_image('boom.png'), 6, 5, self.rect.x, self.rect.y)
            boom_sound.play()
            global ENEMY_AMOUNT
            ENEMY_AMOUNT -= 1
            print(ENEMY_AMOUNT)
            qq = Boom(load_image('boom2.png'), 8, 4, self.rect.x - 40, self.rect.y - 40)
            qq.add(boom_group)
            self.rect.x = -100
            self.kill()
        self.timer += 1
        if self.timer >= self.time:
            laser_sound.play()
            Laser((self.rect.x + 60, self.rect.y))
            self.timer = 0
        if self.rect.x >= 670 - 90 and self.flag:
            self.flag = False
        elif self.rect.x <= 40 and self.flag is False:
            self.flag = True
        if self.flag:
            self.rect = self.rect.move(self.speed, 0)
        else:
            self.rect = self.rect.move(-self.speed, 0)


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('boss_enemy.png'), (640, 320))
        self.rect = self.image.get_rect()
        self.timer1 = 300
        self.timer2 = 0
        self.timer3 = 0
        self.rect.x = 35
        self.rect.y = 130
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False

    def update(self):
        self.timer1 += 1
        self.timer2 += 1
        self.timer3 += 1
        if self.timer1 >= 500:
            Enemy(50, 440, time=65, size=(60, 60), speed=4)
            Enemy(500, 510, time=75, size=(60, 60), direction=False, speed=4)
            self.timer1 = 0
        if self.timer2 >= 50:
            laser_sound.play()
            Laser((self.rect.x + 60, self.rect.y + 50))
            Laser((self.rect.x + 600, self.rect.y + 50))
            self.timer2 = 0
        if self.timer3 >= 150:
            laser_sound.play()
            Laser((self.rect.x + 335, self.rect.y + 180))
            self.timer3 = 0


class Fire(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('fire.png'), (25, 60))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Fire.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + 30
        self.rect.y = pos[1] - 60
        self.add(fire_group)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos=None, *args):
        # if args and '768-KeyDown' in str(args[0]) and pos:
        #     self.rect.x = pos[0] + 30
        #     self.rect.y = pos[1] - 60
        if pygame.sprite.spritecollideany(self, boom_group) or self.rect.y < 95:
            self.rect.x = -100
            self.kill()
        self.rect = self.rect.move(0, -8)


class FireBoss(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('fire.png'), (25, 60))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Fire.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + 30
        self.rect.y = pos[1] - 60
        self.add(fire_group)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos=None, *args):
        global boss
        if pygame.sprite.collide_mask(self, boss) or self.rect.y < 95:
            global BOSS_LIVES
            BOSS_LIVES -= 1
            qq = Boom(load_image('boom2.png'), 8, 4, self.rect.x - 70, self.rect.y - 60)
            qq.add(boom_group)
            boom_sound.play()
            self.rect.x = -100
            self.kill()

        if pygame.sprite.spritecollideany(self, boom_group) or self.rect.y < 95:
            self.rect.x = -100
            self.kill()
        self.rect = self.rect.move(0, -8)


class Laser(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('laser.png'), (8, 45))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Laser.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 30
        self.rect.y = pos[1] + 60
        self.add(laser_group)
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos=None, *args):
        # if args and '768-KeyDown' in str(args[0]) and pos:
        #     self.rect.x = pos[0] + 30
        #     self.rect.y = pos[1] - 60
        if pygame.sprite.spritecollideany(self, ship_group):
            punch_sound.play()
            qq = Boom(load_image('boom.png'), 6, 5, self.rect.x - 40, self.rect.y + 40)
            qq.add(boom1_group)
            self.rect.x = -100
            self.kill()
            global LIFE_AMOUNT
            LIFE_AMOUNT -= 1
        if self.rect.y > 830:
            self.rect.x = -100
            self.kill()
        self.rect = self.rect.move(0, 7)


class Manual(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(600, 400, 300, 300)
        self.setWindowTitle('Manual')
        self.label = QLabel(self)
        self.label.setGeometry(-15, 0, 420, 260)
        self.label.setText('''        RULES:

        You play for the space ship that has to 
        defend from a group of aliens.

        By moving your mouse horizontally you 
        can control the position of your ship.

        By pressing "SPACE" or 
        by right-clicking you can 
        shoot and destroy aliens. 

                                 Stay alive!''')
        self.label.setStyleSheet('font: 15pt Standard')

        self.close_btn = QPushButton('Close', self)
        self.close_btn.setGeometry(100, 250, 100, 40)
        self.close_btn.setStyleSheet('font: 20pt Standard')
        self.close_btn.clicked.connect(self.terminate)

    def terminate(self):
        self.close()


class FinishPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(625, 730)
        self.setWindowTitle('Galaxy Warrior')

        self.pixmap = QPixmap('pictures/end_background.jpg')
        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 625, 730)
        self.back.setPixmap(self.pixmap)

        self.title = QLabel('GAME OVER!', self)
        self.title.setGeometry(90, 50, 500, 65)
        self.title.setStyleSheet('font: 80pt Standard; color: rgb(255, 0, 0)')

        self.finish_btn = QPushButton('Quit', self)
        self.finish_btn.setGeometry(330, 600, 150, 70)
        self.finish_btn.setStyleSheet('font: 30pt Standard')

        self.restart_btn = QPushButton('Restart', self)
        self.restart_btn.setGeometry(150, 600, 150, 70)
        self.restart_btn.setStyleSheet('font: 30pt Standard')

        self.finish_btn.clicked.connect(self.finish)
        self.restart_btn.clicked.connect(self.restart_game)

    def finish(self):
        self.close()

    def restart_game(self):
        self.close()
        ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    ex.show()
    sys.exit(app.exec())

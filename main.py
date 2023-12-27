import pygame
import sys
import io
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton


def load_image(name):
    fullname = f'data/{name}'
    image = pygame.image.load(fullname)
    return image


start_template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>625</width>
    <height>730</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>100</x>
      <y>90</y>
      <width>441</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Welcome to the &quot;Galaxy Warrior&quot;</string>
    </property>
   </widget>
   <widget class="QPushButton" name="lvl1">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>210</y>
      <width>141</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Level1</string>
    </property>
   </widget>
   <widget class="QPushButton" name="lvl2">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>290</y>
      <width>141</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Level2</string>
    </property>
   </widget>
   <widget class="QPushButton" name="boss">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>370</y>
      <width>141</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>BOSS</string>
    </property>
   </widget>
   <widget class="QPushButton" name="manual">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>470</y>
      <width>141</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Manual</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>625</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>625</width>
    <height>730</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>220</x>
      <y>110</y>
      <width>181</width>
      <height>61</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>GAME OVER!</string>
    </property>
   </widget>
   <widget class="QPushButton" name="restart_btn">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>290</y>
      <width>221</width>
      <height>111</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Quit</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>625</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(start_template)
        uic.loadUi(f, self)

        self.manual_page = Manual()

        self.lvl1.clicked.connect(self.run)
        self.lvl2.clicked.connect(self.run)
        self.boss.clicked.connect(self.run)
        self.manual.clicked.connect(self.man)

    def run(self):
        self.close()
        self.start()

    def man(self):
        self.manual_page.show()

    def start(self):
        pygame.init()

        size = width, height = (690, 910)
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        pygame.display.set_caption('Bounce')

        all_sprites = pygame.sprite.Group()
        img = pygame.transform.scale(load_image('life.png'), (60, 50))

        life1 = pygame.sprite.Sprite()
        life1.image = img
        life1.rect = life1.image.get_rect()
        life1.rect.x = 590
        life1.rect.y = 30

        life2 = pygame.sprite.Sprite()
        life2.image = img
        life2.rect = life2.image.get_rect()
        life2.rect.x = 520
        life2.rect.y = 30

        life3 = pygame.sprite.Sprite()
        life3.image = img
        life3.rect = life3.image.get_rect()
        life3.rect.x = 450
        life3.rect.y = 30

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

        all_sprites.add(life1)
        all_sprites.add(life2)
        all_sprites.add(life3)
        all_sprites.add(ship)
        all_sprites.add(enemy)

        my_font = pygame.font.SysFont('Standard', 40)
        score_txt = my_font.render('SCORE:  0', False, (255, 255, 255))

        k = 20
        surf = pygame.Surface((650, 790))
        back = pygame.transform.scale(load_image('background.jpg'), (650, 790))

        surf.blit(back, (0, 0))
        pygame.draw.line(surf, 'white', (0, 0), (649, 0), 1)
        pygame.draw.line(surf, 'white', (649, 0), (649, 789), 1)
        pygame.draw.line(surf, 'white', (0, 789), (649, 789), 1)
        pygame.draw.line(surf, 'white', (0, 0), (0, 789), 1)

        screen.fill((0, 0, 30))
        screen.blit(surf, (k, 100))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            clock.tick(30)
            all_sprites.draw(screen)
            screen.blit(score_txt, (40, 45))
            pygame.display.flip()

        pygame.quit()


class Manual(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(600, 400, 300, 300)
        self.setWindowTitle('Manual')
        self.label = QLabel(self)
        self.label.setGeometry(0, 20, 400, 200)
        self.label.setText('''            THE RULES:
        
        You play for the space-ship that has to 
        defend from a group of asteroids.
        
        By moving your mouse horizontally you 
        can control the position of your ship.
        
        By pressing "SPACE" you can 
        shoot and destroy asteroids. 
        
        Stay alive!''')

        self.close_btn = QPushButton('Close', self)
        self.close_btn.setGeometry(100, 250, 100, 30)
        self.close_btn.clicked.connect(self.terminate)

    def terminate(self):
        self.close()


class FinishPage(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.restart_btn.clicked.connect(self.run)

    def run(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    ex.show()
    sys.exit(app.exec())

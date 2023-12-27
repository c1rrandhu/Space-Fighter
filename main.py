import pygame
import sys
import io
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

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

        self.lvl1.clicked.connect(self.run)

    def run(self):
        self.close()
        self.start()

    def start(self):
        pygame.init()
        board = Board(20, 30)
        size = width, height = (board.left * 2 + 5 * board.cell_size, board.top * 2 + 7 * board.cell_size)
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        pygame.display.set_caption('Bounce')
        board.render(screen)

        screen.fill((0, 0, 60))
        k = 10
        surf = pygame.Surface((width - k, height - k))
        surf.fill((0, 0, 60))
        pygame.draw.line(surf, 'white', (0, 0), (width - 2 * k, 0), 1)
        pygame.draw.line(surf, 'white', (width - 2 * k, 0), (width - 2 * k, height - 2 * k), 1)
        pygame.draw.line(surf, 'white', (0, height - 2 * k), (width - 2 * k, height - 2 * k), 1)
        pygame.draw.line(surf, 'white', (0, 0), (0, height - 2 * k), 1)
        screen.blit(surf, (k, k))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            clock.tick(30)
            pygame.display.flip()

        pygame.quit()


class FinishPage(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.restart_btn.clicked.connect(self.run)

    def run(self):
        self.close()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 50
        self.top = 50
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # рисование
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white', (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                                   self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
        return cell

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if (0 < mouse_pos[0] - self.left < self.width * self.cell_size and
                0 < mouse_pos[1] - self.top < self.height * self.cell_size):
            return ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    ex.show()
    sys.exit(app.exec())

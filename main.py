import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSystemTrayIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from snake import main as snake_main
from tictactoe import main as tictactoe_main

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


class GameCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("GameCenter")
        self.setFixedSize(400, 600)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(resource_path("icon.ico")))
        self.tray.setVisible(True)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        welcome_label = QLabel("Hello,\nGamer!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(welcome_label)
        
        snake_button = QPushButton("Змейка")
        snake_button.setFixedHeight(50)
        snake_button.setStyleSheet("font-size: 16px;")
        snake_button.clicked.connect(self.snake)
        
        tictactoe_button = QPushButton("Крестики-нолики")
        tictactoe_button.setFixedHeight(50)
        tictactoe_button.setStyleSheet("font-size: 16px;")
        tictactoe_button.clicked.connect(self.tictactoe)
        
        layout.addWidget(snake_button)
        layout.addWidget(tictactoe_button)

        layout.addStretch()
    
    def snake(self):
        pygame.font.init()
        snake_main()
    
    def tictactoe(self):
        pygame.font.init()
        tictactoe_main()


def main():
    app = QApplication(sys.argv)
    window = GameCenter()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted")
    except Exception as e:
        print("err: ", e)
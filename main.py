import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSystemTrayIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
import sys

from snake import main as snake_main

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
        
        game_button = QPushButton("Змейка")
        game_button.setFixedHeight(50)
        game_button.setStyleSheet("font-size: 16px;")
        game_button.clicked.connect(self.snake)
        layout.addWidget(game_button)
        
        layout.addStretch()
    
    def snake(self):
        snake_main()


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
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from UI.welcome import welcome_page

current_dir = os.getcwd()
print(current_dir)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Polis Pulse")
        self.resize(400, 300)
        self.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        
        self.stackedWidgets = QStackedWidget()
        
        self.welcome_page = welcome_page(self)
        
        self.stackedWidgets.addWidget(self.welcome_page)
        self.setCentralWidget(self.stackedWidgets)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
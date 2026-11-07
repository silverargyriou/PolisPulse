import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("It's working correctly.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
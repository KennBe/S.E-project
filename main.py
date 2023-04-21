from PyQt6.QtWidgets import QDialog, QApplication 
from PyQt6.uic import loadUi
import sys

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui", self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

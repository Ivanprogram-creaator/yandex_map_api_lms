import sys
from PyQt5.QtWidgets import QApplication
from main_window import Map

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Map()
    window.show()
    window.new_map()
    sys.exit(app.exec())

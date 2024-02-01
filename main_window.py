from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Map preview')
        self.setGeometry(100, 100, 1000, 500)
        self.show_pic()

    def show_pic(self):
        pic = QPixmap("map.png")
        pic_label = QLabel(self)
        pic_label.setGeometry(10, 10, pic.width(), pic.height())
        pic_label.setPixmap(pic)
        pic_label.show()

from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pic = None
        self.pic_label = None
        self.setWindowTitle('Map preview')
        self.setGeometry(100, 100, 1000, 500)
        self.show_pic()

    def show_pic(self):
        self.pic = QPixmap("map.png")
        self.pic_label = QLabel(self)
        self.pic_label.setGeometry(10, 10, self.pic.width(), self.pic.height())
        self.pic_label.setPixmap(self.pic)
        self.pic_label.show()

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_PageUp:
        #     print('Key_PageUp')
        # elif event.key() == Qt.Key_PageDown:    # Key_PageUp:
        #     print('PageDown')
        if event.key() == Qt.Key_PageUp:
            print(event.key())
            self.pic.scaledToWidth(self.pic.width() + self.pic.width() // 10)
            self.pic.scaledToHeight(self.pic.height() + self.pic.height() // 10)
            self.pic_label.setGeometry(10, 10, self.pic.width(), self.pic.height())
            self.pic_label.setPixmap(self.pic)
            self.pic_label.show()
        elif event.key() == Qt.Key_PageDown:
            print(event.key())
            self.pic_label.resize(self.pic.width() - self.pic.width() // 10,
                                  self.pic.height() - self.pic.height() // 10)

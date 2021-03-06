import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(900, 500)
        self.center()
        self.pictureTest = QLabel("选择图片", self)
        self.Result_Text = QTextEdit("结果说明", self)
        self.Result_Text.resize(300, 140)
        self.pictureTest.resize(100, 100)
        self.Result = QLabel("结果", self)
        self.Result.resize(100, 100)

        getPicture1 = QPushButton("选择图片", self)
        getPicture1.clicked.connect(self.openimage)

        parameter = QLabel('参数', self)
        process = QLabel('进度', self)
        learning_rate = QLabel('学习周期', self)
        learning_rate_text = QLineEdit(self)
        epoch = QLabel('Epoch', self)
        epoch_text = QLineEdit(self)
        gpu = QLabel('GPU', self)
        option = QComboBox(self)
        option.addItem('T')
        option.addItem('F')
        id = QLabel('ID', self)
        id_text = QLineEdit(self)
        ip_port = QLabel('IP:Port', self)
        ip_port_text = QLineEdit(self)
        change = QPushButton("=>", self)
        change.clicked.connect(self.change)

        getPicture1.move(430, 350)
        parameter.move(50, 180)
        learning_rate.move(80, 230)
        learning_rate_text.move(150, 230)
        epoch.move(80, 280)
        epoch_text.move(150, 280)
        gpu.move(80, 330)
        option.move(150, 330)
        id.move(80, 380)
        id_text.move(150, 380)
        ip_port.move(80, 430)
        ip_port_text.move(150, 430)
        change.move(570, 280)
        process.move(500, 30)
        self.pictureTest.move(430, 250)
        self.Result.move(700, 250)
        self.Result_Text.move(560, 350)
        self.setWindowTitle('Health')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png")
        jpg = QtGui.QPixmap(imgName).scaled(self.pictureTest.width(), self.pictureTest.height())
        self.pictureTest.setPixmap(jpg)

    def change(self):
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

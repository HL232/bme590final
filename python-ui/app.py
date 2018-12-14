import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import breeze_resources

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.show()

def set_theme():
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

if __name__ == "__main__":
    name = "X-Ray Image Processor"

    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.setApplicationDisplayName(name)

    window = MainWindow()
    app.exec_()
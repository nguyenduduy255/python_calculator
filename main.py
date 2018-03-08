from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import sys
from copy import deepcopy


class Widget(QWidget):
    keyPressed = pyqtSignal()
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.init_ui()

    def init_ui(self):
        self.entry = QLineEdit()
        self.buttons = []

        self.clear_button = QPushButton('CE', self)
        self.clear_button.clicked.connect(self.entry.clear)
        self.clear_last_char_button = QPushButton('C', self)
        self.clear_last_char_button.clicked.connect(self.clear_last_char)

        self.clear_layout = QHBoxLayout()
        self.clear_layout.addWidget(self.clear_button)
        self.clear_layout.addWidget(self.clear_last_char_button)

        self.equal_button = QPushButton('=')
        self.equal_button.clicked.connect(self.evaluate)
        self.hbox = []
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.entry)
        self.vbox.addLayout(self.clear_layout)
        n = 0
        for t in ('()', '123+', '456-', '789*', '0./'):
            self.hbox.append(QHBoxLayout())
            for i in t:
                button = QPushButton(i, self)
                button.clicked.connect(lambda state, x=i: self.entry.insert(x))
                self.buttons.append(button)
                self.hbox[n].addWidget(button)
            self.vbox.addLayout(self.hbox[n])
            n += 1

        self.hbox[3].addWidget(self.equal_button)

        self.setLayout(self.vbox)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_0:
            self.entry.insert('0')
        elif event.key() == Qt.Key_1:
            self.entry.insert('1')
        elif event.key() == Qt.Key_2:
            self.entry.insert('2')
        elif event.key() == Qt.Key_3:
            self.entry.insert('3')
        elif event.key() == Qt.Key_4:
            self.entry.insert('4')
        elif event.key() == Qt.Key_5:
            self.entry.insert('5')
        elif event.key() == Qt.Key_6:
            self.entry.insert('6')
        elif event.key() == Qt.Key_7:
            self.entry.insert('7')
        elif event.key() == Qt.Key_8:
            self.entry.insert('8')
        elif event.key() == Qt.Key_9:
            self.entry.insert('9')
        elif event.key() == Qt.Key_Plus:
            self.entry.insert('+')
        elif event.key() == Qt.Key_Minus:
            self.entry.insert('-')
        elif event.key() == Qt.Key_Asterisk:
            self.entry.insert('*')
        elif event.key() == Qt.Key_Slash:
            self.entry.insert('/')
        elif event.key() == Qt.Key_Period:
            self.entry.insert('.')
        elif event.key() == Qt.Key_ParenLeft:
            self.entry.insert('(')
        elif event.key() == Qt.Key_ParenRight:
            self.entry.insert(')')
        elif event.key() == Qt.Key_Backspace:
            self.clear_last_char()
        elif event.key() == Qt.Key_Enter:
            self.evaluate()

    def clear_last_char(self):
        t = self.entry.text()
        self.entry.clear()
        self.entry.setText(t[:-1])

    def evaluate(self):
        t = self.entry.text()
        t.replace('^', '**')
        result = round(eval(t), 9)
        if result // 1 == result:
            result = int(result)
        self.entry.clear()
        self.entry.setText(str(result))

class Main(QMainWindow):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.main_widget = Widget()
        self.setCentralWidget(self.main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

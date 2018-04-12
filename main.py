from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QAction,
                            QDialog, QDialogButtonBox, QLabel, QStackedLayout, QStackedWidget)
from PyQt5.QtCore import Qt
import sys
from enum import Enum
from functools import partial
from utility import clear_layout
from expression_evaluate import ExpressionEvaluator, TrigMode
from equation_solver import linear_solver, quad_solver

class ReplacingAnsMode(Enum):
    YES = 1
    NO = 0


class Trig(Enum):
    ARC = 1
    NOR = 0


class Button(QPushButton):
    def __init__(self, text, *a, key='', master=None, **kw):
        super().__init__(text, *a, **kw)
        self.init_button()
        if master is not None:
            self.clicked.connect(partial(master.insert, text + key))

    def init_button(self):
        self.setFixedSize(70, 45)
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)


class HBox(QHBoxLayout):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.init_ui()

    def init_ui(self):
        self.setSpacing(2)
        self.addStretch(0)


class NumDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # nice widget for get num
        self.entry = QLineEdit()
        layout.addWidget(self.entry)

        # text for default value
        self.text = QLabel('Default is 11')
        layout.addWidget(self.text)
        self.text.setStyleSheet('{color:#464945}')

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setWindowTitle('Round')

    # static method to create the dialog and return num
    @staticmethod
    def getNum(parent=None):
        dialog = NumDialog(parent)
        dialog.exec_()
        return dialog.entry.text()


class SolveEquationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QStackedLayout()
        self.start_widget = QWidget()
        self.start_layout = QVBoxLayout()

        self._21equation = QPushButton('2 variables linear equation')
        self._21equation.clicked.connect(partial(self.create_solving_widget, 2, 3, func='line'))
        self._31equation = QPushButton('3 variables linear equation')
        self._31equation.clicked.connect(partial(self.create_solving_widget, 3, 4, func='line'))
        self._12equation = QPushButton('1 variables quadratic equation')
        self._12equation.clicked.connect(partial(self.create_solving_widget, 1, 3, func='quad'))

        self.start_layout.addWidget(self._21equation)
        self.start_layout.addWidget(self._31equation)
        self.start_layout.addWidget(self._12equation)

        self.start_widget.setLayout(self.start_layout)
        self.layout.addWidget(self.start_widget)
        self.setLayout(self.layout)

    def create_solving_widget(self, row, column, func):
        self.solving_widget = QWidget()

        self.solving_layout = QVBoxLayout()

        return_button = Button('Return')
        return_button.clicked.connect(self.return_to_start_widget)
        self.solving_layout.addWidget(return_button)

        self.entries = []
        for i in range(row):
            self.entries.append(QHBoxLayout())
            for j in range(column):
                self.entries[i].addWidget(QLineEdit())
            self.solving_layout.addLayout(self.entries[i])

        result_hbox = QHBoxLayout()
        result_label = QLabel('Result')
        result_hbox.addWidget(result_label)
        self.result_num = []
        if func == 'quad':
            row = 2
        for i in range(row):
            self.result_num.append(QLabel())
            result_hbox.addWidget(self.result_num[i])
        self.solving_layout.addLayout(result_hbox)

        ok_button = Button('OK')
        ok_button.clicked.connect(partial(self.solve, func=func))
        self.solving_layout.addWidget(ok_button)

        self.solving_widget.setLayout(self.solving_layout)

        self.layout.addWidget(self.solving_widget)
        self.layout.setCurrentIndex(1)

    def return_to_start_widget(self):
        clear_layout(self.solving_layout)
        del self.solving_widget
        self.layout.removeWidget(self.layout.currentWidget())
        self.layout.setCurrentIndex(0)

    def solve(self, func):
        para = []
        for hbox in self.entries:
            for i in range(hbox.count()):
                para.append(int(hbox.itemAt(i).widget().text()))
        if func == 'line':
            result = linear_solver(*para)
        elif func == 'quad':
            result = quad_solver(*para)
        for i in range(len(self.result_num)):
            self.result_num[i].setText(str(round(result[i], 11)))

    @staticmethod
    def run(parent=None):
        w = SolveEquationWidget(parent)
        w.show()

class Widget(QWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.init_var()
        self.init_ui()

    def init_ui(self):
        self.entry = QLineEdit()
        self.entry.setReadOnly(True)
        self.entry.setFixedHeight(40)

        self.equal_button = Button('=')
        self.equal_button.clicked.connect(self.evaluate)

        self.change_trig_mode_button = Button('Rad')
        self.change_trig_mode_button.clicked.connect(self.change_trig_mode)

        self.shift_button = Button('Shift')
        self.shift_button.clicked.connect(self.change_arctrig)

        self.clear_button = Button('C')
        self.clear_all_button = Button('CE')
        self.clear_button.clicked.connect(self.clear_last_char)
        self.clear_all_button.clicked.connect(self.entry.clear)

        self.clear_hbox = HBox()
        self.clear_hbox.addWidget(self.clear_all_button)
        self.clear_hbox.addWidget(self.clear_button)

        self.number_hbox = self.create_hbox(('7', '8', '9'), ('4', '5', '6'), ('1', '2', '3'), ('0', '.', 'ans'))
        self.trig_hbox = self.create_hbox(('sin', 'cos', 'tan'), key='(')
        self.exponential_optor_hbox = self.create_hbox(('root', 'ln'), ('sqr', 'sqrt', 'log'), key='(')
        self.optor_hbox = self.create_hbox(('*', '/'), ('+', '-'))
        self.special_symbol_hbox = self.create_hbox(('!'), ('(', ')'))
        self.special_num_hbox = self.create_hbox(('pi', 'e'))

        # Exceptional button in above hbox
        self.special_symbol_hbox[0].insertWidget(1, Button(text='abs', key='(', master=self))
        self.exponential_optor_hbox[0].insertWidget(0, Button(text='^', master=self))

        self.hbox = [HBox() for i in range(8)]
        self.hbox[0].addLayout(self.clear_hbox)

        self.hbox[1].addWidget(self.change_trig_mode_button)
        self.hbox[1].addLayout(self.trig_hbox[0])
        self.hbox[1].addWidget(self.shift_button)

        self.hbox[2].addLayout(self.special_symbol_hbox[0])
        self.hbox[2].addLayout(self.exponential_optor_hbox[0])

        self.hbox[3].addLayout(self.special_symbol_hbox[1])
        self.hbox[3].addLayout(self.exponential_optor_hbox[1])

        self.hbox[4].addLayout(self.number_hbox[0])
        self.hbox[4].addLayout(self.optor_hbox[0])

        self.hbox[5].addLayout(self.number_hbox[1])
        self.hbox[5].addLayout(self.optor_hbox[1])

        self.hbox[6].addLayout(self.number_hbox[2])
        self.hbox[6].addLayout(self.special_num_hbox[0])

        self.hbox[7].addLayout(self.number_hbox[3])
        self.hbox[7].addWidget(Button(text='%', master=self))
        self.hbox[7].addWidget(self.equal_button)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.entry)
        for h in self.hbox:
            self.vbox.addLayout(h)

        self.vbox.setSpacing(2)
        self.vbox.addStretch(0)
        self.setLayout(self.vbox)

    def init_var(self):
        self.is_decimal = False
        self.is_mul = False
        self.eval = False
        self.replacing_ans_mode = ReplacingAnsMode.NO
        self.trig = Trig.NOR
        self.round_num = 11
        self.e = ExpressionEvaluator()

    def create_hbox(self, *token_list, key=''):
        hbox_list = [HBox() for i in range(len(token_list))]
        n = 0
        for i in token_list:
            for token in i:
                button = Button(text=token, key=key, master=self)
                hbox_list[n].addWidget(button)
            n += 1
        return hbox_list

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_0:
            self.insert('0')
        elif event.key() == Qt.Key_1:
            self.insert('1')
        elif event.key() == Qt.Key_2:
            self.insert('2')
        elif event.key() == Qt.Key_3:
            self.insert('3')
        elif event.key() == Qt.Key_4:
            self.insert('4')
        elif event.key() == Qt.Key_5:
            self.insert('5')
        elif event.key() == Qt.Key_6:
            self.insert('6')
        elif event.key() == Qt.Key_7:
            self.insert('7')
        elif event.key() == Qt.Key_8:
            self.insert('8')
        elif event.key() == Qt.Key_9:
            self.insert('9')
        elif event.key() == Qt.Key_Plus:
            self.insert('+')
        elif event.key() == Qt.Key_Minus:
            self.insert('-')
        elif event.key() == Qt.Key_Asterisk:
            self.insert('*')
        elif event.key() == Qt.Key_Slash:
            self.insert('/')
        elif event.key() == Qt.Key_Period:
            self.insert('.')
        elif event.key() == Qt.Key_ParenLeft:
            self.insert('(')
        elif event.key() == Qt.Key_ParenRight:
            self.insert(')')
        # For ^
        elif event.key() == 94:
            self.insert('^')
        elif event.key() == Qt.Key_Exclam:
            self.insert('!')
        elif event.key() == Qt.Key_Comma:
            self.insert(',')
        elif event.key() == Qt.Key_Backspace:
            self.clear_last_char()
        elif event.key() == Qt.Key_Enter:
            self.evaluate()

    def insert(self, key):
        if self.eval:
            if key not in '+-*/':
                self.entry.clear()
            self.eval = False
        elif not (self.is_decimal and key == '.') or (self.is_mul and key in ' * / '):
            if key == '.':
                self.is_decimal = True
            elif key in '+-*/':
                self.is_mul = True
                self.is_decimal = False
            else:
                self.is_mul = False
            if key == 'ans' and self.replacing_ans_mode == ReplacingAnsMode.YES:
                key = self.result
        self.entry.insert(key)

    def change_trig_mode(self):
        if self.e.trig_mode == TrigMode.RADIAN:
            self.e.trig_mode = TrigMode.DEGREE
            self.change_trig_mode_button.setText('Deg')
        else:
            self.e.trig_mode = TrigMode.RADIAN
            self.change_trig_mode_button.setText('Rad')

    def change_replacing_ans_mode(self):
        if self.replacing_ans_mode == ReplacingAnsMode.NO:
            self.replacing_ans_mode = ReplacingAnsMode.YES
        else:
            self.replacing_ans_mode = ReplacingAnsMode.NO

    def set_round_num(self):
        self.round_num = NumDialog.getNum(self)
        if self.round_num:
            self.round_num = int(self.round_num)
        else:
            self.round_num = 11

    def change_arctrig(self):
        if self.trig == Trig.NOR:
            for i in range(3):
                button = self.trig_hbox[0].itemAt(i + 1).widget()
                button.setText('arc' + button.text())
                self.trig = Trig.ARC
                self.reconnect(button.clicked, lambda state, x=button.text(): self.insert(x + '('))
        elif self.trig == Trig.ARC:
            for i in range(3):
                button = self.trig_hbox[0].itemAt(i + 1).widget()
                button.setText(button.text()[3:])
                self.trig = Trig.NOR
                self.reconnect(button.clicked, lambda state, x=button.text(): self.insert(x + '('))

    def reconnect(self, signal, newhandler=None, oldhandler=None):
        while True:
            try:
                if oldhandler is not None:
                    signal.disconnect(oldhandler)
                else:
                    signal.disconnect()
            except TypeError:
                break
        if newhandler is not None:
            signal.connect(newhandler)

    def clear_last_char(self):
        t = self.entry.text()
        self.entry.clear()
        self.entry.setText(t[:-1])

    def solve_equation(self):
        SolveEquationWidget.run()

    def evaluate(self):
        self.eval = True
        t = self.entry.text()
        self.result = str(round(self.e.parse(t), self.round_num))
        self.entry.clear()
        self.entry.setText(self.result)


class Main(QMainWindow):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.main_widget = Widget()
        self.init_ui()
        self.init_menu()
        self.setCentralWidget(self.main_widget)

    def init_ui(self):
        self.setWindowTitle('My First Calculator')

    def init_menu(self):
        menubar = self.menuBar()
        mode_menu = menubar.addMenu('Mode')
        replacing_ans_action = QAction('Replace Ans with specific number', self)
        replacing_ans_action.setCheckable(True)
        replacing_ans_action.triggered.connect(self.main_widget.change_replacing_ans_mode)

        setting_menu = menubar.addMenu('Setting')
        get_round_num_action = QAction('Round', self)
        get_round_num_action.triggered.connect(self.main_widget.set_round_num)

        equation_menu = menubar.addMenu('Equation')
        solve_equation_action = QAction('Solve equation', self)
        solve_equation_action.triggered.connect(self.main_widget.solve_equation)

        mode_menu.addAction(replacing_ans_action)
        setting_menu.addAction(get_round_num_action)
        equation_menu.addAction(solve_equation_action)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # main = Main()
    # main.show()
    SolveEquationWidget.run()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QApplication, QAction)
from widget import *


class Main(QMainWindow):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.main_widget = Widget()
        self.init_ui()
        self.init_menu()
        self.setCentralWidget(self.main_widget)

    def init_ui(self):
        self.setWindowTitle('My First Calculator')
        self.move(500, 200)

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
    main = Main()
    main.show()
    sys.exit(app.exec_())

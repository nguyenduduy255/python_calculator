from enum import Enum


class ReplacingAnsMode(Enum):
    YES = 1
    NO = 0


class Trig(Enum):
    ARC = 1
    NOR = 0


def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clear_layout(child.layout())

def change_font(widget, size=11):
    font = widget.font()
    font.setPointSize(size)
    widget.setFont(font)

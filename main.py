import random
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

ui_scale: int = 3

st = {
    f"{a} x {b}": {
        "expected": a * b,
        "score": 1,
        "answers": [],
        "answer-times": [],
        "a": a,
        "b": b,
    } for a in range(1, 10) for b in range(1, 10)}

runtime = {}


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text = "Hello, world!"

        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Drawing text')
        # self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        self.drawGrid(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10 * ui_scale))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def drawGrid(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(event.rect())

        def drawPoint(a, b):
            b = (9 - b)
            off_a = 20 * ui_scale if a < 5 else 24 * ui_scale
            off_b = 20 * ui_scale if b < 5 else 24 * ui_scale
            qp.drawRect(off_a + 16 * a * ui_scale, off_b + 16 * b * ui_scale, 8 * ui_scale, 8 * ui_scale)

        # qp.setPen(QColor(255, 255, 255))
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(64, 64, 64))

        for a in range(10):
            for b in range(10):
                drawPoint(a, b)

        # qp.setPen(QColor(200, 200, 200))
        # qp.setBrush(QColor(64, 64, 64))
        # for a in range(runtime['a']):
        #     drawPoint(a, -1)
        # for b in range(runtime['b']):
        #     drawPoint(-1, b)

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(128, 128, 128))

        for a in range(runtime['a']):
            for b in range(runtime['b']):
                drawPoint(a, b)

        if runtime['response_ok']:
            qp.setBrush(QColor(0, 120, 0))
        else:
            qp.setPen(QPen(QColor(100, 0, 0), 4))
            qp.setBrush(QBrush(Qt.NoBrush))

        for a in range(runtime['a']):
            for b in range(runtime['response'] // runtime['a']):
                drawPoint(a, b)
        for a in range(runtime['response'] % runtime['a']):
            drawPoint(a, runtime['response'] // runtime['a'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QApplication([])
    window = QWidget()
    window.setGeometry(300, 300, 600, 750)
    v_layout = QVBoxLayout()
    h_layout = QHBoxLayout()

    answer = QLineEdit('')
    answer.setValidator(QIntValidator())
    answer.setFont(QFont('Arial', 10 * ui_scale))

    lbl = QLabel('')
    lbl.setFont(QFont('Arial', 10 * ui_scale))
    info = QLabel('')
    info.setFont(QFont('Arial', 10 * ui_scale))
    ex = Example()

    runtime['counter'] = 0

    def next_one():
        current = random.choice(list(st.keys()))
        runtime.update(st[current])
        runtime['response'] = 0
        runtime['response_ok'] = False
        runtime['go'] = False

        lbl.setText(f'{current} = ')
        info.clear()
        info.setText(f"Hotovo: {runtime['counter']} příkladů")
        runtime['counter'] += 1
        ex.update()


    next_one()


    def ok_btn():
        if runtime['go']:
            runtime['go'] = False
            next_one()
            answer.clear()
            answer.setFocus()
        elif len(answer.text()) != 0:
            if int(answer.text()) == runtime["expected"]:
                runtime['go'] = True
                info.setText(f'{runtime["expected"]} ✓')
                runtime['response'] = int(answer.text())
                runtime['response_ok'] = True
            else:
                info.setText(f'Chybná odpověď: {answer.text()}')
                runtime['response'] = int(answer.text())
                runtime['response_ok'] = False
                answer.clear()
                answer.setFocus()

        ex.update()


    btn_ok = QPushButton('OK')
    btn_ok.clicked.connect(ok_btn)
    answer.returnPressed.connect(ok_btn)

    h_layout.addWidget(lbl)
    h_layout.addWidget(answer)
    v_layout.addLayout(h_layout)
    v_layout.addWidget(info, )
    v_layout.addWidget(btn_ok)
    v_layout.addWidget(ex, stretch=1)
    window.setLayout(v_layout)
    window.show()
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

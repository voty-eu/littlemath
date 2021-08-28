import random
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

st = {
    f"{a} x {b}": {
        "expected": a * b,
        "score": 1,
        "answers": [],
        "answer-times": [],
        "a": a,
        "b": b,
    } for a in range(1, 10) for b in range(1, 10)}


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
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def drawGrid(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(event.rect())

        def drawPoint(a, b):
            b = (9 - b)
            off_a = 20 if a < 5 else 24
            off_b = 20 if b < 5 else 24
            qp.drawRect(off_a + 16 * a, off_b + 16 * b, 8, 8)

        # qp.setPen(QColor(255, 255, 255))
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(64, 64, 64))

        for a in range(10):
            for b in range(10):
                drawPoint(a, b)

        # qp.setPen(QColor(200, 200, 200))
        # qp.setBrush(QColor(64, 64, 64))
        # for a in range(st['current']['a']):
        #     drawPoint(a, -1)
        # for b in range(st['current']['b']):
        #     drawPoint(-1, b)

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(128, 128, 128))

        for a in range(st['current']['a']):
            for b in range(st['current']['b']):
                drawPoint(a, b)

        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(QBrush(Qt.NoBrush))
        for a in range(st['current']['a']):
            for b in range(st['current']['response'] // st['current']['a']):
                drawPoint(a, b)
        for a in range(st['current']['response'] % st['current']['a']):
            drawPoint(a, st['current']['response'] // st['current']['a'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QApplication([])
    window = QWidget()
    window.setGeometry(300, 300, 300, 350)
    v_layout = QVBoxLayout()
    h_layout = QHBoxLayout()

    answer = QLineEdit('')
    answer.setValidator(QIntValidator())

    lbl = QLabel('')
    info = QLabel('')
    ex = Example()


    def next_one():
        current = random.choice(list(st.keys()))
        st['current'] = st[current]
        st['current']['response'] = 0
        lbl.setText(f'{current} = ')
        info.clear()
        ex.update()


    next_one()


    def ok_btn():
        if len(answer.text()) != 0:
            if int(answer.text()) == st["current"]["expected"]:
                next_one()
            else:
                info.setText(f'Chybná odpověď: {answer.text()}')
                st['current']['response'] = int(answer.text())

        ex.update()
        answer.clear()
        answer.setFocus()


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

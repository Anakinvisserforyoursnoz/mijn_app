import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Moderne Calculator")
        self.setGeometry(200, 200, 350, 500)

        self.layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setFont(QFont("Arial", 24))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(70)

        self.layout.addWidget(self.display)

        grid = QGridLayout()

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 18))
            button.setFixedSize(80, 80)

            if text == '=':
                button.clicked.connect(self.calculate)
            elif text == 'C':
                button.clicked.connect(self.clear)
            else:
                button.clicked.connect(self.button_clicked)

            grid.addWidget(button, row, col)

        self.layout.addLayout(grid)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }

            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 10px;
            }

            QPushButton {
                background-color: #3c3f41;
                color: white;
                border-radius: 15px;
            }

            QPushButton:hover {
                background-color: #505357;
            }
        """)

    def button_clicked(self):
        button = self.sender()
        self.display.setText(self.display.text() + button.text())

    def calculate(self):
        try:
            result = str(eval(self.display.text()))
            self.display.setText(result)
        except:
            self.display.setText("Error")

    def clear(self):
        self.display.clear()

app = QApplication(sys.argv)

window = Calculator()
window.show()

sys.exit(app.exec())

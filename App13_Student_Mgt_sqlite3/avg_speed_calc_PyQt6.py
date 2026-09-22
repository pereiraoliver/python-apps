import sys

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


class AvgSpeedCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        dist_label = QLabel("Distance (km):")
        self.dist_line_edit = QLineEdit()
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(["Metric (km)", "Metric (miles)"])
        hours_label = QLabel("Time(hours):")
        self.hours_line_edit = QLineEdit()
        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.calc_avg_speed)
        self.output_label = QLabel("")

        grid.addWidget(dist_label, 0, 0)
        grid.addWidget(self.dist_line_edit, 0, 1)
        grid.addWidget(hours_label, 1, 0)
        grid.addWidget(self.hours_line_edit, 1, 1)
        grid.addWidget(calc_button, 2, 0, 1, 3)
        grid.addWidget(self.output_label, 3, 0, 1, 2)
        grid.addWidget(self.dist_combo, 3, 2)

        self.setLayout(grid)

    def calc_avg_speed(self):
        if self.dist_combo.currentIndex() == 0:
            avg = float(self.dist_line_edit.text()) / float(self.hours_line_edit.text())
            self.output_label.setText(f"Average Speed: {avg:.2f} km/h")
        elif self.dist_combo.currentIndex() == 1:
            avg = (
                float(self.dist_line_edit.text())
                * 0.621371
                / float(self.hours_line_edit.text())
            )
            self.output_label.setText(f"Average Speed: {avg:.2f} mph")


app = QApplication(sys.argv)

window = AvgSpeedCalc()
window.show()

sys.exit(app.exec())

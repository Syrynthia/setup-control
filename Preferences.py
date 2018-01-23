from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (QWidget, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QPushButton)
#from ReadOdt import THRESH
import sys
import ui


class PreferencesDialog(QDialog):

    def __init__(self, threshold):
        self.threshold = threshold
        super(PreferencesDialog, self).__init__()
        self.setWindowTitle("Preferences")
        main_layout = QVBoxLayout()

        self.change_threshold()
        main_layout.addWidget(self.frame)

        self.setLayout(main_layout)

    def change_threshold(self):
        self.frame = QGroupBox("Threshold")
        thresh_layout = QGridLayout()
        thresh_layout.addWidget(QLabel("Current threshold [cm]: "), 0, 0)
        self.thresh_label = QLabel(str(self.threshold))
        thresh_layout.addWidget(self.thresh_label, 0, 1)
        thresh_layout.addWidget(QLabel("New value [cm]:"), 1, 0)

        self.textbox = QLineEdit(self)
        only_number = QDoubleValidator()
        self.textbox.setValidator(only_number)
        thresh_layout.addWidget(self.textbox, 1, 1)

        apply_button = QPushButton('Apply', self)
        apply_button.clicked.connect(self.apply)
        thresh_layout.addWidget(apply_button, 2, 0)

        self.frame.setLayout(thresh_layout)

    def apply(self):
        thresh = self.textbox.text()
        try:
            val = float(thresh)
            self.threshold = val
            self.thresh_label.setText(str(self.threshold))
        except ValueError:
            pass

    def get_threshold(self):
        return self.threshold


# if __name__ == '__main__':
#     app = ui.QApplication(sys.argv)
#     dialog = PreferencesDialog(0.3)
#     sys.exit(dialog.exec_())
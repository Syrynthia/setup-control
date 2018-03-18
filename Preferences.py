from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import (QWidget, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QPushButton,
                             QHBoxLayout)
#from ReadOdt import THRESH
import sys

from PyQt5.uic.properties import QtCore

import ui


class PreferencesDialog(QDialog):

    def __init__(self, threshold, correction, mean):
        self.threshold = threshold
        self.correction = correction
        self.mean = mean
        super(PreferencesDialog, self).__init__()
        self.setWindowTitle("Preferences")
        main_layout = QVBoxLayout()

        self.change_threshold()
        main_layout.addWidget(self.frame)

        self.change_correction_number()
        main_layout.addWidget(self.frame2)

        self.change_mean_number()
        main_layout.addWidget(self.frame3)

        self.create_buttons()
        main_layout.addWidget(self.buttons)

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

        self.frame.setLayout(thresh_layout)

    def change_correction_number(self):
        self.frame2 = QGroupBox("Number of sessions before the corrections were applied")
        thresh_layout = QGridLayout()
        thresh_layout.addWidget(QLabel("Current number: "), 0, 0)
        self.correction_label = QLabel(str(self.correction))
        thresh_layout.addWidget(self.correction_label, 0, 1)
        thresh_layout.addWidget(QLabel("New value:"), 1, 0)

        self.correction_textbox = QLineEdit(self)
        only_number = QIntValidator()
        self.correction_textbox.setValidator(only_number)
        thresh_layout.addWidget(self.correction_textbox, 1, 1)

        self.frame2.setLayout(thresh_layout)

    def change_mean_number(self):
        self.frame3 = QGroupBox("Number of sessions used to calculate the mean averages")
        thresh_layout = QGridLayout()
        thresh_layout.addWidget(QLabel("Current number: "), 0, 0)
        if self.mean == 0:
            self.mean_label = QLabel("All sessions")
        else:
            self.mean_label = QLabel(str(self.mean))
        thresh_layout.addWidget(self.mean_label, 0, 1)
        thresh_layout.addWidget(QLabel("New value:"), 1, 0)

        self.mean_textbox = QLineEdit(self)
        only_number = QIntValidator()
        self.mean_textbox.setValidator(only_number)
        thresh_layout.addWidget(self.mean_textbox, 1, 1)

        self.frame3.setLayout(thresh_layout)

    def create_buttons(self):
        self.buttons = QWidget()
        buttons_layout = QHBoxLayout()

        apply_button = QPushButton('Apply', self)
        apply_button.clicked.connect(self.apply)
        buttons_layout.addWidget(apply_button)

        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.ok)
        buttons_layout.addWidget(ok_button)

        self.buttons.setLayout(buttons_layout)

    def apply(self):
        thresh = self.textbox.text()
        if "," in thresh:
            thresh = thresh.replace(",", ".")
        try:
            val = float(thresh)
            self.threshold = val
            self.thresh_label.setText(str(self.threshold))
        except ValueError:
            pass

        cor = self.correction_textbox.text()
        try:
            val = int(cor)
            self.correction = val
            self.correction_label.setText(str(self.correction))
        except ValueError:
            pass

        mean = self.mean_textbox.text()
        try:
            val = int(mean)
            self.mean = val
            if val == 0:
                self.mean_label.setText("All sessions")
            else:
                self.mean_label.setText(str(self.mean))
        except ValueError:
            pass

    def ok(self):
        thresh = self.textbox.text()
        if "," in thresh:
            thresh = thresh.replace(",", ".")
        try:
            val = float(thresh)
            self.threshold = val
        except ValueError:
            pass

        cor = self.correction_textbox.text()
        try:
            val = int(cor)
            self.correction = val
        except ValueError:
            pass

        mean = self.mean_textbox.text()
        try:
            val = int(mean)
            self.mean = val
        except ValueError:
            pass

        self.close()

    def get_threshold(self):
        return self.threshold

    def get_correction_sessions(self):
        return self.correction

    def get_mean_sessions(self):
        return self.mean


# if __name__ == '__main__':
#     app = ui.QApplication(sys.argv)
#     dialog = PreferencesDialog(0.3, 2, 0)
#     sys.exit(dialog.exec_())
import sys

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTextEdit

import ui
from EnglishWidget import EnglishWidget
from PolishWidget import PolishWidget


class HelpWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        super(HelpWindow, self).__init__()
        self.help_widget = HelpWidget(self)
        self.setCentralWidget(self.help_widget)
        self.setWindowTitle("Help")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)


class HelpWidget(QWidget):

    def __init__(self, parent):
        super(HelpWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.main_img = QImage('images/wybor_wykresu.png', 'PNG').scaledToWidth(600)
        self.single_img = QImage('images/single_patient.png', 'PNG').scaledToWidth(600)
        self.pref_img = QImage('images/preferencje.png', 'PNG')

        self.create_tabs()

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def create_tabs(self):
        self.tabs = QTabWidget()

        self.english = EnglishWidget(self, self.main_img, self.single_img, self.pref_img)
        self.polski = PolishWidget(self, self.main_img, self.single_img, self.pref_img)

        self.tabs.addTab(self.english, "English")
        self.tabs.addTab(self.polski, "Polski")

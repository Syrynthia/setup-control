from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit,
                             QVBoxLayout, QAction, QApplication, QCheckBox)
from ReadOdt import read_table, calculate_avg_stdev

class MultiPatientsDialog(QDialog):

    def __init__(self, filez):
        self.table = []
        self.mean_table = []
        self.std_table = []
        for file in filez:
            self.table.append(read_table(file)[2])
        for i in range(0, len(self.table)):
            tmp = calculate_avg_stdev(self.table[i])
            self.mean_table.append(tmp[0])
            self.std_table.append([tmp[1]])

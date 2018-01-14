from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit,
                             QVBoxLayout, QAction, QApplication, QCheckBox)
import ReadOdt
import os


class MultiPatientsDialog(QDialog):

    def __init__(self, filez):
        super(MultiPatientsDialog, self).__init__()
        self.table = []
        self.mean_table = []
        self.std_table = []
        self.filenames = []
        for file in filez:
            self.table.append(ReadOdt.read_table(file)[2])
            self.filenames.append(os.path.split(file)[1])

        for i in range(0, len(self.table)):
            tmp = ReadOdt.calculate_avg_stdev(self.table[i])
            self.mean_table.append(tmp[0])
            self.std_table.append(tmp[1])
        mainLayout = QVBoxLayout()
        self.create_data()
        mainLayout.addWidget(self.resultFrame)
        self.setLayout(mainLayout)

    def create_data(self):

        self.resultFrame = QGroupBox("Data ")
        self.frameLayout = QGridLayout()

        self.frameLayout.addWidget(QLabel("Filename"), 0, 0)
        self.frameLayout.addWidget(QLabel("Mean vrt"), 0, 1)
        self.frameLayout.addWidget(QLabel("Mean lng"), 0, 2)
        self.frameLayout.addWidget(QLabel("Mean lat"), 0, 3)
        self.frameLayout.addWidget(QLabel("Mean rtn"), 0, 4)

        for row in range(0, len(self.mean_table)):
            self.frameLayout.addWidget(QLabel(self.filenames[row]), row + 1, 0)
            for col in range(0, len(self.mean_table[row])):
                tmp = str(self.mean_table[row][col]) + u"\u00B1" + str(self.std_table[row][col])
                self.frameLayout.addWidget(QLabel(tmp), row + 1, col+1)

        self.resultFrame.setLayout(self.frameLayout)
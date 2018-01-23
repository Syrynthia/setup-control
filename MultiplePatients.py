from PyQt5.QtWidgets import (QWidget, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QMenu, QMenuBar,
                             QTextEdit, QHBoxLayout, QScrollBar,
                             QVBoxLayout, QAction, QApplication, QCheckBox, QScrollArea)
import ReadOdt
import os
from PlotCanvas import PlotCanvas
from PyQt5.QtCore import Qt


class MultiPatientsDialog(QDialog):
    toplot = [[], [], [], []]
    vrt = []
    lng = []
    lat = []
    rtn = []

    def __init__(self, filez, threshold):
        super(MultiPatientsDialog, self).__init__()
        self.threshold = threshold
        self.table = []
        self.mean_table = []
        self.std_table = []
        self.filenames = []
        for file in filez:
            self.table.append(ReadOdt.read_table(file, self.threshold)[2])
            self.filenames.append(os.path.split(file)[1])

        for i in range(0, len(self.table)):
            tmp = ReadOdt.calculate_avg_stdev(self.table[i])
            self.mean_table.append(tmp[0])
            self.std_table.append(tmp[1])

        self.tables_to_separate()

        mainLayout = QVBoxLayout()
        self.create_data()
        mainLayout.addWidget(self.resultFrame)

        self.createPlotFrame()
        mainLayout.addWidget(self.plotFrame)

        self.setLayout(mainLayout)

    def create_data(self):

        self.resultFrame = QGroupBox("Data ")
        self.resultFrame.setMaximumHeight(400)
        self.data_print = QWidget()
        self.data_print.setMinimumWidth(400)
        #self.data_print.setFixedHeight(300)
        self.frameLayout = QGridLayout()
        self.main_frame = QHBoxLayout()

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

        self.data_print.setLayout(self.frameLayout)

        scroll = QScrollArea()
        scroll.setWidget(self.data_print)

        self.main_frame.addWidget(scroll)
        self.resultFrame.setLayout(self.main_frame)

    def tables_to_separate(self):
        print("Trying to do separate tables")
        for row in self.mean_table:
            self.vrt.append(row[0])
            self.lng.append(row[1])
            self.lat.append(row[2])
            self.rtn.append(row[3])


    def createPlotFrame(self):
        self.plotFrame = QGroupBox(" ")
        self.plotFrame.setStyleSheet("border:0;")
        self.plotLayout = QGridLayout()
        self.m = PlotCanvas(self, width=7, height=5)
        self.plotLayout.addWidget(self.m, 0, 0)

        self.checkboxes = QGroupBox("")
        self.checkboxes.setStyleSheet("border:0;")
        self.checkboxesLayout = QVBoxLayout()

        self.cbVrt = QCheckBox('Vertical', self)
        self.cbVrt.stateChanged.connect(self.drawVrt)
        cbLng = QCheckBox('Longitudinal', self)
        cbLng.stateChanged.connect(self.drawLng)
        cbLat = QCheckBox('Latitudinal', self)
        cbLat.stateChanged.connect(self.drawLat)
        cbRtn = QCheckBox('Rotational', self)
        cbRtn.stateChanged.connect(self.drawRtn)

        self.checkboxesLayout.addWidget(self.cbVrt)
        self.checkboxesLayout.addWidget(cbLng)
        self.checkboxesLayout.addWidget(cbLat)
        self.checkboxesLayout.addWidget(cbRtn)
        self.checkboxes.setLayout(self.checkboxesLayout)

        self.plotLayout.addWidget(self.checkboxes, 0, 1)
        self.plotFrame.setLayout(self.plotLayout)

    def drawVrt(self, state):
        if state == Qt.Checked:
            self.toplot[0] = self.vrt
            self.m.plotChecked(self.toplot, self.filenames)
        else:
            self.toplot[0] = []
            self.m.plotChecked(self.toplot, self.filenames)

    def drawLng(self, state):
        if state == Qt.Checked:
            self.toplot[1] = self.lng
            self.m.plotChecked(self.toplot, self.filenames)
        else:
            self.toplot[1] = []
            self.m.plotChecked(self.toplot, self.filenames)

    def drawLat(self, state):
        if state == Qt.Checked:
            self.toplot[2] = self.lat
            self.m.plotChecked(self.toplot, self.filenames)
        else:
            self.toplot[2] = []
            self.m.plotChecked(self.toplot, self.filenames)

    def drawRtn(self, state):
        if state == Qt.Checked:
            self.toplot[3] = self.rtn
            self.m.plotChecked(self.toplot, self.filenames)
        else:
            self.toplot[3] = []
            self.m.plotChecked(self.toplot, self.filenames)
